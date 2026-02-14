from django.urls import path, include
from . import views

app_name = "stories"

urlpatterns = [
    path("", views.story_list, name="story_list"),
    path("<int:story_id>/", views.story_detail, name="story_detail"),
    path("<int:story_id>/play/", views.play_story, name="play_story"),
    path("page/<int:page_id>/", views.page_view, name="page_view"),
    path("stats/", views.stats, name="stats"),
    path("signup/", views.signup, name="signup"),
    path("create/", views.create_story_view, name="create_story"),
    path("<int:story_id>/edit/", views.edit_story_view, name="edit_story"),
    path("<int:story_id>/delete/", views.delete_story_view, name="delete_story"),
    path("<int:story_id>/pages/create/", views.create_page_view, name="create_page"),
    path("pages/<int:page_id>/choices/create/", views.create_choice_view, name="create_choice"),
    path("page/<int:page_id>/edit/", views.edit_page_view, name="edit_page"),
    path("my-stories/", views.my_stories, name="my_stories"),
    path("page/<int:page_id>/delete/", views.delete_page_view, name="delete_page")
]
