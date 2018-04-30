from django.db import models
from django.urls import reverse #Used to generate URLs by reversing the URL patterns
import uuid # Required for unique book instances

class Genre(models.Model):
    """
    Model representing a movie genre (e.g. Science Fiction, Drama).
    """
    name = models.CharField(max_length=100, help_text="Introduzca un genero cinematográfico (Comedia, Romance...)")
    
    def __str__(self):
        """
        String for representing the Model object (in Admin site etc.)
        """
        return self.name

class Year(models.Model):
    """
    Model representing a movie release year.
    """
    date = models.CharField(max_length=4, help_text="Introduzca el año de estreno")
    
    def __str__(self):
        """
        String for representing the Model object (in Admin site etc.)
        """
        return self.date

class Score(models.Model):
    """
    Model representing a movie score (1, 2, 3, 4 or 5).
    """
    stars = models.CharField(max_length=1, help_text="Introduzca la valoración")
    
    def __str__(self):
        """
        String for representing the Model object (in Admin site etc.)
        """
        return self.stars

class Actor(models.Model):
    """
    Model representing the name of an actor. 
    """
    firstName = models.CharField(max_length=100, help_text="Introduzca el nombre del actor")
    lastName = models.CharField(max_length=100, help_text="Introduzca el apellido del actor")
    
    def __str__(self):
        """
        String for representing the Model object (in Admin site etc.)
        """
        return '{0} {1}'.format(self.firstName ,self.lastName)



class Movie(models.Model):
    """
    Model representing a movie.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="ID unico de esta película.")
    title = models.CharField(max_length=200, help_text='Seleccione titulo de esta pelicula.')
    trailer = models.TextField(max_length=1000, help_text='Enter movie trailer URL')
    overview = models.TextField(max_length=1000, null=True, blank=True, help_text='Enter a brief summary of the movie')
    year = models.ManyToManyField(Year, blank=True, help_text='Seleccione el año de estreno de esta pelicula.')
    director = models.CharField(max_length = 100, null=True, blank=True, help_text='Seleccione el director de esta pelicula.')
    cast = models.ManyToManyField(Actor, blank=True, help_text='Seleccione los actores que parcitipan en esta pelicula.')
    cover = models.TextField(max_length=1000, null=True, blank=True, help_text='Enter movie cover URL')
    score = models.ManyToManyField(Score, blank=True, help_text='Seleccione una valoracion para esta pelicula.')
    genre = models.ManyToManyField(Genre, blank=True, help_text='Seleccione un genero para esta pelicula.')
    
    def __str__(self):
        """
        String for representing the Model object.
        """
        return self.title
    
    
    def get_absolute_url(self):
        """
        Returns the url to access a detail record for this book.
        """
        return reverse('movie-detail', args=[str(self.id)])