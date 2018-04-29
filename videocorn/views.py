from django.shortcuts import render
from .models import Genre, Year, Score, Actor, Movie
from django.contrib.auth.decorators import login_required

@login_required
def home(request):

    #Obtenemos de la BD
    queryset_list = Movie.objects.all()
    year_list = Year.objects.all().order_by('date')
    genre_list = Genre.objects.all().order_by('name')
    score_list = Score.objects.all().order_by('stars')

    #Obtenemos los parametros de busqueda
    title = request.GET.get("title")
    year = request.GET.get("year")
    genre = request.GET.get("genre")
    score = request.GET.get("score")

    #Filtramos
    if title:
        queryset_list = queryset_list.filter(title__icontains=title)
    if year:
        queryset_list = queryset_list.filter(year__date=year)
    if genre:
        queryset_list = queryset_list.filter(genre__name=genre)
    if score:
        queryset_list = queryset_list.filter(score__stars=score)

    # Contexto
    context = {
        "movie_list" : queryset_list,
        "year_list" : year_list,
        "genre_list" : genre_list,
        "score_list" : score_list,
        "year" : year,
        "genre" : genre,
        "score" : score,
    }
    # Render the HTML template home.html with the data in the context variable
    return render(
        request,
        'videocorn/home.html',
        context,
    )

@login_required
def movie(request,pk):
    
    # Obtenemos la pelicula, si no existe devolvemos error
    try:
        movie = Movie.objects.get(id=pk)
    except Movie.DoesNotExist:
        raise Http404("Movie does not exist")
    

    # Contexto
    context = {
        "movie" : movie,
    }

    # Render the HTML template movie.html with the data in the context variable
    return render(
        request,
        'videocorn/movie.html',
        context,
    )

