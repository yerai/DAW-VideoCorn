from django.shortcuts import render
from .models import Genre, Year, Score, Actor, Movie
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required

@login_required
def home(request):

    #Obtenemos los datos de la BD para el dropdown
    queryset_list = Movie.objects.all()
    year_list = Year.objects.all().order_by('date')
    genre_list = Genre.objects.all().order_by('name')
    score_list = Score.objects.all().order_by('stars')

    #Obtenemos los parametros de busqueda para filtrar
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

    # Valores a enviar al template
    context = {
        "movie_list" : queryset_list,
        "year_list" : year_list,
        "genre_list" : genre_list,
        "score_list" : score_list,
        "year" : year,
        "genre" : genre,
        "score" : score,
    }
    
    # Render
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


from .forms import UserForm
from django.contrib.auth.models import User
from django.contrib import messages 


@staff_member_required
def users(request):

    #Obtenemos lista de usuarios
    user_list = User.objects.all().order_by('username')

    #Obtenemos peticion
    if request.method == "POST":
        form = UserForm(request.POST)

        #Si el form es valido
        if form.is_valid():

            #Creamos mensaje
            messages.success(request, 'El usuario ha sido creado satisfactoriamente.')
            print(form.cleaned_data['username'])

            #Si la peticion es Add --> Creamos usuario
            if request.POST['action'] == 'add':
                User.objects.create_user(**form.cleaned_data)

            #Si la peticion es Edit --> actualizamos usuario
            if request.POST.get("action") == 'edit':
                print("jejeje")
                username = request.POST.get("username")
                User.objects.filter(username=username).update()
        
        #Si la peticion es Delete --> Eliminamos usuario
        if request.POST['action'] == 'delete':
            print("holi")
                

        
    else:
        form = UserForm() 

    # Contexto
    context = {
        "user_list" : user_list,
        "form" : form,
    }

    return render(
        request, 
        'videocorn/users.html',
        context,
    )