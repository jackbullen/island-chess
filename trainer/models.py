from django.db import models

class Repertoire(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    def __str__(self):
        return self.name

class Opening(models.Model):
    name = models.CharField(max_length=255)
    eco = models.CharField(max_length=6)
    repertoire = models.ForeignKey(Repertoire, on_delete=models.CASCADE)
    def __str__(self):
        return self.name

class Line(models.Model):
    name = models.CharField(max_length=255)
    opening = models.ForeignKey(Opening, on_delete=models.CASCADE)
    def __str__(self):
        return self.name

class Variation(models.Model):
    name = models.CharField(max_length=255)
    fen = models.TextField(max_length=100)
    pgn = models.TextField()
    line = models.ForeignKey(Line, on_delete=models.CASCADE)
    def __str__(self):
        return self.name
