from django.shortcuts import render, redirect
from django.db.models import Count
from django.utils.crypto import get_random_string
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .services import ( create_story, update_story, delete_story, create_page, create_choice, update_page, delete_page,  ) # ⭐ ADD THIS delete_page, # ⭐ AND THIS )
from .services import (
    get_stories,
    get_story,
    get_start_page,
    get_page,
    create_story,
    update_story,
    delete_story,
    create_page,
    create_choice,
)
from .models import Play, PlaySession


@login_required
def create_story_view(request):
    if not request.user.groups.filter(name="Author").exists():
        return HttpResponseForbidden("You are not an author.")

    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")

        data, status = create_story(title, description, request.user.id)

        if status == 201:
            return redirect("stories:story_detail", story_id=data["story_id"])
        else:
            return render(request, "error.html", {"message": data.get("error")})

    return render(request, "create_story.html")


@login_required
def edit_story_view(request, story_id):
    story = get_story(story_id)

    if not request.user.groups.filter(name="Author").exists():
        return HttpResponseForbidden("You are not an author.")

    if story["owner_id"] != request.user.id:
        return HttpResponseForbidden("This is not your story.")

    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")
        status = request.POST.get("status")

        data, status_code = update_story(
            story_id, title, description, status, request.user.id
        )

        if status_code == 200:
            return redirect("stories:story_detail", story_id=story_id)
        else:
            return render(request, "error.html", {"message": data.get("error")})

    return render(request, "edit_story.html", {"story": story})


@login_required
def delete_story_view(request, story_id):
    story = get_story(story_id)

    if not request.user.groups.filter(name="Author").exists():
        return HttpResponseForbidden("You are not an author.")

    if story["owner_id"] != request.user.id:
        return HttpResponseForbidden("This is not your story.")

    data, status_code = delete_story(story_id, request.user.id)

    if status_code == 200:
        return redirect("stories:story_list")
    else:
        return render(request, "error.html", {"message": data.get("error")})


@login_required
def create_page_view(request, story_id):
    story = get_story(story_id)

    if not request.user.groups.filter(name="Author").exists():
        return HttpResponseForbidden("You are not an author.")

    if story["owner_id"] != request.user.id:
        return HttpResponseForbidden("This is not your story.")

    if request.method == "POST":
        text = request.POST.get("text")
        is_ending = request.POST.get("is_ending") == "on"
        ending_label = request.POST.get("ending_label")

        data, status_code = create_page(
            story_id, text, is_ending, ending_label, request.user.id
        )

        if status_code == 201:
            return redirect("stories:story_detail", story_id=story_id)
        else:
            return render(request, "error.html", {"message": data.get("error")})

    return render(request, "create_page.html", {"story": story})


def story_list(request):
    query = request.GET.get("q", "").lower()
    stories = get_stories()

    # Only show published stories
    stories = [s for s in stories if s["status"] == "published"]

    # Search filter
    if query:
        stories = [s for s in stories if query in s["title"].lower()]

    return render(request, "story_list.html", {"stories": stories})


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
        "story_detail.html",
        {"story": story, "resume_page_id": resume_page_id},
    )


def play_story(request, story_id):
    story = get_story(story_id)

    # Draft protection unless preview=1
    preview = request.GET.get("preview") == "1"
    if story["status"] != "published" and not preview:
        return render(
            request, "error.html", {"message": "This story is not published."}
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

    if not start or "page_id" not in start:
        return render(
            request,
            "error.html",
            {"message": "This story has no pages yet. Add a page first."},
        )

    PlaySession.objects.create(
        session_id=session_id, story_id=story_id, current_page_id=start["page_id"]
    )

    return redirect("stories:page_view", page_id=start["page_id"])


def create_choice_view(request, page_id):
    if request.method == "POST":
        text = request.POST.get("text")
        next_page_id = request.POST.get("next_page_id")

        create_choice(page_id, text, next_page_id)

        return redirect("stories:page_view", page_id=page_id)

    story_pages = get_story(get_page(page_id)["story_id"])["pages"]

    return render(
        request, "create_choice.html", {"page_id": page_id, "pages": story_pages}
    )


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
        "stats.html",
        {
            "plays_per_story": plays_per_story,
            "endings_per_story": endings_per_story,
            "percentages": percentages,
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

    if not session_id:
        session_id = get_random_string(32)
        request.session["session_id"] = session_id

    # If ending → save Play + clear session
    if page["is_ending"]:
        Play.objects.create(story_id=page["story_id"], ending_page_id=page["id"])
        PlaySession.objects.filter(
            session_id=session_id, story_id=page["story_id"]
        ).delete()

        return render(request, "ending.html", {"page": page})

    return render(request, "page.html", {"page": page})


def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()

            # Default role: Reader
            reader_group, _ = Group.objects.get_or_create(name="Reader")
            user.groups.add(reader_group)

            login(request, user)
            return redirect("stories:story_list")
    else:
        form = UserCreationForm()

    return render(request, "signup.html", {"form": form})


@login_required
def my_stories(request):
    stories = [s for s in get_stories() if s["owner_id"] == request.user.id]
    return render(request, "my_stories.html", {"stories": stories})

@login_required
def delete_page_view(request, page_id):
    page = get_page(page_id)
    story = get_story(page["story_id"])

    if story["owner_id"] != request.user.id:
        return HttpResponseForbidden("This is not your story.")

    data, status = delete_page(page_id, request.user.id)

    if status == 200:
        return redirect("stories:story_detail", story_id=story["id"])
    else:
        return render(request, "error.html", {"message": data.get("error")})


@login_required
def edit_page_view(request, page_id):
    page = get_page(page_id)
    story = get_story(page["story_id"])

    if story["owner_id"] != request.user.id:
        return HttpResponseForbidden("This is not your story.")

    if request.method == "POST":
        text = request.POST.get("text")
        is_ending = request.POST.get("is_ending") == "on"
        ending_label = request.POST.get("ending_label")

        data, status = update_page(page_id, text, is_ending, ending_label, request.user.id)

        if status == 200:
            return redirect("stories:story_detail", story_id=story["id"])
        else:
            return render(request, "error.html", {"message": data.get("error")})

    return render(request, "page_edit.html", {"page": page})

