from django.db import models

class Repertoire(models.Model):
    name = models.CharField(max_length=20)
    player = models.CharField(max_length=6) # black or white

    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return self.name

class Opening(models.Model):
    name = models.CharField(max_length=20)
    pgn = models.CharField(max_length=500)
    fen = models.CharField(max_length=100)
    repertoires = models.ManyToManyField(Repertoire)

    class Meta:
        verbose_name = 'Opening'
        verbose_name_plural = 'Openings'
        ordering = ['name']

    def __str__(self):
        return self.name


class Variation(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)
    pgn = models.CharField(max_length=1000)
    start_fen = models.CharField(max_length=100)
    end_fen = models.CharField(max_length=100, unique=True)
    opening = models.ForeignKey(Opening, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Variation'
        verbose_name_plural = 'Variations'
        ordering = ['name']

    def __str__(self):
        return self.name

class ChessGame(models.Model):
    event = models.CharField(max_length=100)
    site = models.CharField(max_length=100)
    date = models.CharField(max_length=20)
    round = models.CharField(max_length=3)
    white = models.CharField(max_length=50)
    black = models.CharField(max_length=50)
    result = models.CharField(max_length=10)
    white_elo = models.IntegerField(null=True, blank=True)
    black_elo = models.IntegerField(null=True, blank=True)
    eco = models.CharField(max_length=20)
    pgn = models.CharField(max_length=2000)
    variations = models.ManyToManyField(Variation)

    class Meta:
        verbose_name = 'Chess Game'
        verbose_name_plural = 'Chess Games'
        ordering = ['eco']

    def __str__(self):
        return self.white + " VS " + self.black+" ("+self.result+")"
    

class Move(models.Model):
    variations = models.ManyToManyField(Variation)
    move_number = models.IntegerField()
    san = models.CharField(max_length=10)
    fen = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'Move'
        verbose_name_plural = 'Moves'
        ordering = ['move_number']
    
    def __str__(self):
        return self.san


