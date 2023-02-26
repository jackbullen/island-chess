from django.db import models

class ChessMove(models.Model):
    fen = models.CharField(max_length=256)
    san = models.CharField(max_length=16)
    move_number = models.IntegerField()

class ChessGame(models.Model):
    moves = models.ManyToManyField(ChessMove)
    result = models.CharField(max_length=16)