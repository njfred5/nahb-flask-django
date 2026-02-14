import requests

FLASK_API = "http://127.0.0.1:5000"
API_KEY = "flask123"

HEADERS = {
    "Content-Type": "application/json",
    "X-API-KEY": API_KEY
}

def create_story(title, description, user_id):
    payload = {
        "title": title,
        "description": description,
        "owner_id": user_id
    }
    r = requests.post(f"{FLASK_API}/stories", json=payload, headers=HEADERS)
    return r.json(), r.status_code


def update_story(story_id, title, description, status, user_id):
    payload = {
        "title": title,
        "description": description,
        "status": status,
        "owner_id": user_id
    }
    r = requests.put(f"{FLASK_API}/stories/{story_id}", json=payload, headers=HEADERS)
    return r.json(), r.status_code


def delete_story(story_id, user_id):
    payload = {"owner_id": user_id}
    r = requests.delete(f"{FLASK_API}/stories/{story_id}", json=payload, headers=HEADERS)
    return r.json(), r.status_code


def create_page(story_id, text, is_ending, ending_label, user_id):
    payload = {
        "text": text,
        "is_ending": is_ending,
        "ending_label": ending_label,
        "owner_id": user_id
    }
    r = requests.post(f"{FLASK_API}/stories/{story_id}/pages", json=payload, headers=HEADERS)
    return r.json(), r.status_code


def get_story(story_id):
    return requests.get(f"{FLASK_API}/stories/{story_id}", headers=HEADERS).json()


def get_stories():
    return requests.get(f"{FLASK_API}/stories", headers=HEADERS).json()


def get_start_page(story_id):
    return requests.get(f"{FLASK_API}/stories/{story_id}/start", headers=HEADERS).json()


def get_page(page_id):
    return requests.get(f"{FLASK_API}/pages/{page_id}", headers=HEADERS).json()

def update_page(page_id, text, is_ending, ending_label, user_id):
    payload = {
        "text": text,
        "is_ending": is_ending,
        "ending_label": ending_label,
    }
    r = requests.put(f"{FLASK_API}/stories/pages/{page_id}", json=payload, headers=HEADERS)
    return r.json(), r.status_code

def create_choice(page_id, text, next_page_id):
    payload = {
        "text": text,
        "next_page_id": next_page_id
    }
    r = requests.post(f"{FLASK_API}/stories/pages/{page_id}/choices", json=payload, headers=HEADERS)
    return r.json(), r.status_code

def delete_page(page_id, user_id):
    r = requests.delete(f"{FLASK_API}/stories/pages/{page_id}", headers=HEADERS)
    return r.json(), r.status_code
