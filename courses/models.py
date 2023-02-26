from django.db import models

class Course(models.Model):
    name = models.CharField(max_length=30)
    player = models.CharField(max_length=6) # black or white

    class Meta:
        verbose_name = 'Course'
        verbose_name_plural = 'Courses'
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Chapter(models.Model):
    name = models.CharField(max_length=120)
    start_fen = models.CharField(max_length=100)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        verbose_name = 'Chapter'
        verbose_name_plural = 'Chapters'
        ordering = ['created_at']

    def __str__(self):
        return self.name

class Variation(models.Model):
    name = models.CharField(max_length=120)
    pgn = models.CharField(max_length=10000)
    end_fen = models.CharField(max_length=100)
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)    
    class Meta:
        verbose_name = 'Variation'
        verbose_name_plural = 'Variations'
        ordering = ['created_at']

    def __str__(self):
        return self.name

class Move(models.Model):
    variation = models.ForeignKey(Variation, on_delete=models.CASCADE)
    move_number = models.IntegerField()
    san = models.CharField(max_length=10)
    fen = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'Move'
        verbose_name_plural = 'Moves'
        ordering = ['variation']
    
    def __str__(self):
        return self.san


