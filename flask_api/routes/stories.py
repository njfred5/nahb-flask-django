from flask import Blueprint, request
from models import Story
from database import db

stories_bp = Blueprint("stories", __name__, url_prefix="/stories")

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
