from django.db import models

class Genre(models.Model):
    name = models.CharField(max_length=100,primary_key=True)
    
    def __str__(self):
        return self.name

class Year(models.Model):
    date = models.IntegerField(primary_key=True)
    
    def __str__(self):
        return str(self.date)

class Score(models.Model):
    stars = models.IntegerField(primary_key=True)
    
    def __str__(self):
        return str(self.stars)

class Actor(models.Model):
    id = models.IntegerField(primary_key=True)
    fullName = models.CharField(max_length=100)
   
    def __str__(self):
        return self.fullName



class Movie(models.Model):
    title = models.CharField(max_length=200)
    trailer = models.TextField(max_length=1000)
    overview = models.TextField(max_length=1000, null=True, blank=True)
    year = models.ForeignKey(Year, on_delete=models.CASCADE, null=True, blank=True)
    director = models.CharField(max_length = 100, null=True, blank=True)
    cast = models.ManyToManyField(Actor, blank=True)
    cover = models.TextField(max_length=1000, null=True, blank=True)
    score = models.ForeignKey(Score, on_delete=models.CASCADE, null=True, blank=True)
    genre = models.ManyToManyField(Genre, blank=True)
    
    def __str__(self):
        return self.title