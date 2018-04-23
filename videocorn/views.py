from django.shortcuts import render
from .models import Genre, Year, Score, Actor, Movie
from django.contrib.auth.decorators import login_required

@login_required
def home(request):

    #Obtenemos de la BD
    queryset_list = Movie.objects.all()
    genres = Genre.objects.all()
    scores = Score.objects.all()

    #Obtenemos los parametros de busqueda
    title = request.GET.get("title")
    genre = request.GET.get("genre")
    score = request.GET.get("score")
    

    #Filtramos
    if title:
        queryset_list = queryset_list.filter(title__icontains=title)
    
    


    # Generate counts of some of the main objects
    num_movies=Movie.objects.all().count()

    # Available books (status = 'a')
    num_movies_selected=Movie.objects.filter(title__exact='Coco').count()
    num_generos=Genre.objects.count()  # The 'all()' is implied by default.
    
    # Context
    context = {
        "movie_list" : queryset_list,
        "genre_list" : genres,
        "score_list" : scores,
    }
    # Render the HTML template home.html with the data in the context variable
    return render(
        request,
        'videocorn/home.html',
        context,
    )


