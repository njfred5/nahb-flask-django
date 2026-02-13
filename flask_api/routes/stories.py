from flask import Blueprint, request, jsonify
from models import Story, Page
from database import db

stories_bp = Blueprint("stories", __name__, url_prefix="/stories")

# ... your GET /stories endpoint here ...

# GET /stories/<id>
@stories_bp.get("/<int:story_id>")
def get_story(story_id):
    story = Story.query.get_or_404(story_id)
    return {
        "id": story.id,
        "title": story.title,
        "description": story.description,
        "status": story.status,
        "start_page_id": story.start_page_id
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
            "start_page_id": s.start_page_id
        }
        for s in stories
    ]

@stories_bp.post("")
def create_story():
    data = request.json

    story = Story(
        title=data.get("title"),
        description=data.get("description"),
        status=data.get("status", "draft")  # default = draft
    )

    db.session.add(story)
    db.session.commit()

    return {"message": "Story created", "story_id": story.id}, 201
@stories_bp.put("/<int:story_id>")
def update_story(story_id):
    story = Story.query.get_or_404(story_id)
    data = request.json

    story.title = data.get("title", story.title)
    story.description = data.get("description", story.description)
    story.status = data.get("status", story.status)
    story.start_page_id = data.get("start_page_id", story.start_page_id)

    db.session.commit()

    return {"message": "Story updated"}
@stories_bp.delete("/<int:story_id>")
def delete_story(story_id):
    story = Story.query.get_or_404(story_id)

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
