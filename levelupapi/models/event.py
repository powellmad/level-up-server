from django.db import models

class Event(models.Model):
    description = models.TextField()
    game = models.ForeignKey("Game", on_delete=models.CASCADE)
    date = models.DateTimeField()
    time = models.DateTimeField()
    organizer = models.ForeignKey("Gamer", on_delete=models.CASCADE)
