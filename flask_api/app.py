from flask import Flask
from database import db

def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///stories.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    # Register blueprints
    from routes.stories import stories_bp
    from routes.pages import pages_bp
    from routes.choices import choices_bp

    app.register_blueprint(stories_bp)
    app.register_blueprint(pages_bp)
    app.register_blueprint(choices_bp)

    @app.route("/health")
    def health():
        return {"status": "ok"}

    return app


if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        db.create_all()
    app.run(debug=True)
