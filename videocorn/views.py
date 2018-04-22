from django.shortcuts import render
from .models import Genre, Year, Score, Actor, Movie
from django.contrib.auth.decorators import login_required

@login_required(login_url="login/")
def home(request):
    """
    View function for home page of site.
    """
    # Generate counts of some of the main objects
    num_movies=Movie.objects.all().count()

    # Available books (status = 'a')
    num_movies_selected=Movie.objects.filter(title__exact='Coco').count()
    num_generos=Genre.objects.count()  # The 'all()' is implied by default.
    
    # Render the HTML template home.html with the data in the context variable
    return render(
        request,
        'videocorn/home.html',
        context={'num_movies':num_movies,'num_movies_selected':num_movies_selected,'num_generos':num_generos},
    )


