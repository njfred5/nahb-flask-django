import requests

FLASK_API = "http://127.0.0.1:5000"

def get_stories():
    return requests.get(f"{FLASK_API}/stories?status=published").json()

def get_story(story_id):
    return requests.get(f"{FLASK_API}/stories/{story_id}").json()

def get_start_page(story_id):
    return requests.get(f"{FLASK_API}/stories/{story_id}/start").json()

def get_page(page_id):
    return requests.get(f"{FLASK_API}/pages/{page_id}").json()
