from django.db import models

# Create your models here.
class Play(models.Model):
    story_id = models.IntegerField()
    ending_page_id = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Story {self.story_id} ended at page {self.ending_page_id}"

class PlaySession(models.Model):
    session_id = models.CharField(max_length=255)
    story_id = models.IntegerField()
    current_page_id = models.IntegerField()
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Session {self.session_id} on story {self.story_id} at page {self.current_page_id}"
