from django.urls import path
from . import views

app_name = "stories"

urlpatterns = [
    path("", views.story_list, name="story_list"),
    path("<int:story_id>/", views.story_detail, name="story_detail"),
    path("<int:story_id>/play/", views.play_story, name="play_story"),
    path("page/<int:page_id>/", views.page_view, name="page_view"),
    path("stats/", views.stats, name="stats"),
]
