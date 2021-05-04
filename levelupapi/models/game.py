from django.db import models

class Game(models.Model):
    title = models.CharField(max_length=50)
    instructions = models.TextField()
    max_players = models.IntegerField()
    type = models.ForeignKey('GameType', on_delete=models.CASCADE) 