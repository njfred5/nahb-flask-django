from database import db

class Story(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(20), default="draft")
    start_page_id = db.Column(db.Integer, db.ForeignKey("page.id"))
    owner_id = db.Column(db.Integer, nullable=False)  

    pages = db.relationship(
        "Page",
        backref="story",
        cascade="all, delete",
        foreign_keys="Page.story_id"
    )



class Page(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    story_id = db.Column(db.Integer, db.ForeignKey("story.id"), nullable=False)
    text = db.Column(db.Text, nullable=False)
    is_ending = db.Column(db.Boolean, default=False)
    ending_label = db.Column(db.String(100), nullable=True)

    choices = db.relationship(
        "Choice",
        backref="page",
        cascade="all, delete",
        foreign_keys="Choice.page_id"
    )


class Choice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    page_id = db.Column(db.Integer, db.ForeignKey("page.id"), nullable=False)
    text = db.Column(db.String(200), nullable=False)
    next_page_id = db.Column(db.Integer, db.ForeignKey("page.id"))
