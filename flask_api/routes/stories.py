from flask import Blueprint, request, jsonify
from models import Story, Page
from database import db
from models import Story, Page, Choice



stories_bp = Blueprint("stories", __name__, url_prefix="/stories")

# ... your GET /stories endpoint here ...

# GET /stories/<id>
@stories_bp.get("/<int:story_id>")
def get_story(story_id):
    story = Story.query.get_or_404(story_id)
    pages = Page.query.filter_by(story_id=story.id).all()

    return {
        "id": story.id,
        "title": story.title,
        "description": story.description,
        "status": story.status,
        "start_page_id": story.start_page_id,
        "owner_id": story.owner_id,
        "pages": [
            {
                "id": p.id,
                "text": p.text,
                "is_ending": p.is_ending,
                "ending_label": p.ending_label
            }
            for p in pages
        ]
    }



# GET /stories/<id>/start
@stories_bp.get("/<int:story_id>/start")
def get_start_page(story_id):
    story = Story.query.get_or_404(story_id)

    if not story.start_page_id:
        return {"error": "Story has no start page yet"}, 400

    page = Page.query.get(story.start_page_id)

    return {
        "page_id": page.id,
        "text": page.text,
        "is_ending": page.is_ending,
        "ending_label": page.ending_label,
        "choices": [
            {
                "id": c.id,
                "text": c.text,
                "next_page_id": c.next_page_id
            }
            for c in page.choices
        ]
    }
@stories_bp.get("")
def list_stories():
    status = request.args.get("status")
    query = Story.query

    if status:
        query = query.filter_by(status=status)

    stories = query.all()

    return [
        {
            "id": s.id,
            "title": s.title,
            "description": s.description,
            "status": s.status,
            "start_page_id": s.start_page_id,
            "owner_id": s.owner_id,
        }
        for s in stories
    ]
@stories_bp.put("/pages/<int:page_id>")
def update_page(page_id):
    page = Page.query.get_or_404(page_id)
    data = request.json

    page.text = data.get("text", page.text)
    page.is_ending = data.get("is_ending", page.is_ending)
    page.ending_label = data.get("ending_label", page.ending_label)

    db.session.commit()

    return {"message": "Page updated"}, 200

@stories_bp.delete("/pages/<int:page_id>")
def delete_page(page_id):
    page = Page.query.get_or_404(page_id)

    db.session.delete(page)
    db.session.commit()

    return {"message": "Page deleted"}, 200

@stories_bp.post("")
def create_story():
    data = request.json

    # ⭐ REQUIRE owner_id
    owner_id = data.get("owner_id")
    if not owner_id:
        return {"error": "owner_id is required"}, 400

    story = Story(
        title=data.get("title"),
        description=data.get("description"),
        status=data.get("status", "draft"),
        owner_id=owner_id  # ⭐ STORE OWNER
    )

    db.session.add(story)
    db.session.commit()

    return {"message": "Story created", "story_id": story.id}, 201

@stories_bp.put("/<int:story_id>")
def update_story(story_id):
    story = Story.query.get_or_404(story_id)
    data = request.json

    # ⭐ REQUIRE owner_id in request
    request_owner_id = data.get("owner_id")
    if not request_owner_id:
        return {"error": "owner_id is required"}, 400

    # ⭐ CHECK OWNERSHIP
    if story.owner_id != request_owner_id:
        return {"error": "Forbidden: not your story"}, 403

    story.title = data.get("title", story.title)
    story.description = data.get("description", story.description)
    story.status = data.get("status", story.status)
    story.start_page_id = data.get("start_page_id", story.start_page_id)

    db.session.commit()

    return {"message": "Story updated"}

@stories_bp.delete("/<int:story_id>")
def delete_story(story_id):
    story = Story.query.get_or_404(story_id)
    data = request.json or {}

    # ⭐ REQUIRE owner_id
    request_owner_id = data.get("owner_id")
    if not request_owner_id:
        return {"error": "owner_id is required"}, 400

    # ⭐ CHECK OWNERSHIP
    if story.owner_id != request_owner_id:
        return {"error": "Forbidden: not your story"}, 403

    db.session.delete(story)
    db.session.commit()

    return {"message": "Story deleted"}


# POST /stories/<id>/pages
@stories_bp.post("/<int:story_id>/pages")
def create_page(story_id):
    story = Story.query.get_or_404(story_id)
    data = request.json

    page = Page(
        story_id=story.id,
        text=data.get("text"),
        is_ending=data.get("is_ending", False),
        ending_label=data.get("ending_label")
    )

    db.session.add(page)
    db.session.commit()

    # If this is the first page, set it as start_page
    if story.start_page_id is None:
        story.start_page_id = page.id
        db.session.commit()

    return {"message": "Page created", "page_id": page.id}, 201

@stories_bp.post("/pages/<int:page_id>/choices")
def create_choice(page_id):
    data = request.json

    choice = Choice(
        page_id=page_id,
        text=data.get("text"),
        next_page_id=data.get("next_page_id")
    )

    db.session.add(choice)
    db.session.commit()

    return {"message": "Choice created", "choice_id": choice.id}, 201

