from flask import Blueprint, request
from models import Page, Choice
from database import db

choices_bp = Blueprint("choices", __name__, url_prefix="/choices")


# POST a choice
@choices_bp.post("/<int:page_id>")
def create_choice(page_id):
    page = Page.query.get_or_404(page_id)
    data = request.json

    choice = Choice(
        page_id=page.id,
        text=data.get("text"),
        next_page_id=data.get("next_page_id")
    )

    db.session.add(choice)
    db.session.commit()

    return {"message": "Choice created", "choice_id": choice.id}, 201


# UPDATE a choice
@choices_bp.put("/<int:choice_id>")
def update_choice(choice_id):
    choice = Choice.query.get_or_404(choice_id)
    data = request.json

    choice.text = data.get("text", choice.text)
    choice.next_page_id = data.get("next_page_id", choice.next_page_id)

    db.session.commit()
    return {"message": "Choice updated", "choice_id": choice.id}

# DELETE a choice
@choices_bp.delete("/<int:choice_id>")
def delete_choice(choice_id):
    choice = Choice.query.get_or_404(choice_id)
    db.session.delete(choice)
    db.session.commit()
    return {"message": "Choice deleted"}

