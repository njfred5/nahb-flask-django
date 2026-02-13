from django.shortcuts import render, redirect
from .services import get_stories, get_story, get_start_page, get_page
from .models import Play
from django.db.models import Count
from .models import PlaySession
from django.utils.crypto import get_random_string


def story_list(request):
    query = request.GET.get("q", "").lower()
    stories = get_stories()

    # Only show published stories
    stories = [s for s in stories if s["status"] == "published"]

    # Search filter
    if query:
        stories = [s for s in stories if query in s["title"].lower()]

    return render(request, "stories/story_list.html", {"stories": stories})


def story_detail(request, story_id):
    story = get_story(story_id)

    # Resume autosave
    session_id = request.session.get("session_id")
    resume_page_id = None

    if session_id:
        try:
            session = PlaySession.objects.get(session_id=session_id, story_id=story_id)
            resume_page_id = session.current_page_id
        except PlaySession.DoesNotExist:
            pass

    return render(
        request,
        "stories/story_detail.html",
        {"story": story, "resume_page_id": resume_page_id},
    )


def play_story(request, story_id):
    story = get_story(story_id)

    # Draft protection unless preview=1
    preview = request.GET.get("preview") == "1"
    if story["status"] != "published" and not preview:
        return render(
            request, "stories/error.html", {"message": "This story is not published."}
        )

    # Session ID
    session_id = request.session.get("session_id")
    if not session_id:
        session_id = get_random_string(32)
        request.session["session_id"] = session_id

    # Resume if exists
    try:
        session = PlaySession.objects.get(session_id=session_id, story_id=story_id)
        return redirect("stories:page_view", page_id=session.current_page_id)
    except PlaySession.DoesNotExist:
        pass

    # Start new game
    start = get_start_page(story_id)
    PlaySession.objects.create(
        session_id=session_id, story_id=story_id, current_page_id=start["page_id"]
    )
    return redirect("stories:page_view", page_id=start["page_id"])


def stats(request):
    plays_per_story = Play.objects.values("story_id").annotate(count=Count("id"))
    endings_per_story = Play.objects.values("story_id", "ending_page_id").annotate(
        count=Count("id")
    )

    # Build totals
    totals = {item["story_id"]: item["count"] for item in plays_per_story}

    # Build percentages dict
    percentages = {}

    for item in endings_per_story:
        story_id = item["story_id"]
        ending_id = item["ending_page_id"]
        count = item["count"]
        total = totals.get(story_id, 1)

        if story_id not in percentages:
            percentages[story_id] = {}

        percentages[story_id][ending_id] = round((count / total) * 100, 2)

    return render(
        request,
        "stories/stats.html",
        {
            "plays_per_story": plays_per_story,
            "endings_per_story": endings_per_story,
            "percentages": percentages,   # ⭐ ADD THIS
        },
    )



def page_view(request, page_id):
    page = get_page(page_id)

    # Update autosave session
    session_id = request.session.get("session_id")
    if session_id:
        PlaySession.objects.update_or_create(
            session_id=session_id,
            story_id=page["story_id"],
            defaults={"current_page_id": page_id},
        )
    session_id = request.session.get("session_id")


    if not session_id:
        session_id = get_random_string(32)
        request.session["session_id"] = session_id

    # If ending → save Play + clear session
    if page["is_ending"]:
        Play.objects.create(story_id=page["story_id"], ending_page_id=page["id"])
        PlaySession.objects.filter(
            session_id=session_id, story_id=page["story_id"]
        ).delete()

        return render(request, "stories/ending.html", {"page": page})

    return render(request, "stories/page.html", {"page": page})
