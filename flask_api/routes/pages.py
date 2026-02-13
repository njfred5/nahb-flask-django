from flask import Blueprint, request, jsonify
from models import Story, Page, Choice
from database import db

pages_bp = Blueprint("pages", __name__, url_prefix="/pages")

# GET /pages/<id>  -> return page + choices
@pages_bp.get("/<int:page_id>")
def get_page(page_id):
    page = Page.query.get_or_404(page_id)

    return {
        "id": page.id,
        "story_id": page.story_id,
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

# UPDATE a page
@pages_bp.put("/<int:page_id>")
def update_page(page_id):
    page = Page.query.get_or_404(page_id)
    data = request.json

    page.text = data.get("text", page.text)
    page.is_ending = data.get("is_ending", page.is_ending)
    page.ending_label = data.get("ending_label", page.ending_label)
    page.story_id = data.get("story_id", page.story_id)

    db.session.commit()
    return {"message": "Page updated", "page_id": page.id}

@pages_bp.delete("/<int:page_id>")
def delete_page(page_id):
    page = Page.query.get_or_404(page_id)

    # delete choices first
    for c in page.choices:
        db.session.delete(c)

    db.session.delete(page)
    db.session.commit()
    return {"message": "Page deleted"}
