from django.shortcuts import render
from .models import Genre, Year, Score, Actor, Movie
from django.contrib.auth.decorators import login_required
from .forms import SearchForm

@login_required
def home(request):

    #Obtenemos de la BD
    queryset_list = Movie.objects.all()

    #Obtenemos los parametros de busqueda
    title = request.GET.get("title")
    genre = request.GET.get("genre")
    score = request.GET.get("score")
    year = request.GET.get("year")

    year_list = list(Year.objects.all())
    hola = print(year)
    hola2 = string(hola)

    #Filtramos
    if title:
        queryset_list = queryset_list.filter(title__icontains=title)
    
    
    # Form
    form = SearchForm(request.GET)

    # Context
    context = {
        "movie_list" : queryset_list,
        "form" : form,
    }
    # Render the HTML template home.html with the data in the context variable
    return render(
        request,
        'videocorn/home.html',
        context,
    )


