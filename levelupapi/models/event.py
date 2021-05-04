from django.db import models

class Event(models.Model):
    description = models.TextField()
    start_date = models.DateTimeField()
    game = models.ForeignKey("Game", on_delete=models.CASCADE)
    organizer = models.ForeignKey("Gamer", on_delete=models.CASCADE)
    attendees = models.ManyToManyField("Gamer", through="EventGamer", related_name="attending")