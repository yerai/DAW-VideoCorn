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


from django.contrib.auth.models import User
from django.contrib import messages 

@staff_member_required
def users(request):

    #Obtenemos lista de usuarios
    user_list = User.objects.all().order_by('username')

    #Obtenemos peticion
    if request.method == "POST":

        # Añadir Usuario
        if request.POST['action'] == 'add':
            
            #Obtenemos los datos
            username = request.POST['username']
            email = request.POST['email']
            password = request.POST['password']
            
            #Creamos nuevo usuario
            u = User(username=username, email=email, password=password)
            u.save()

            #Creamos mensaje
            messages.success(request, 'El usuario ha sido creado satisfactoriamente.')

        # Modificar Usuario
        if request.POST['action'] == 'edit':
            
            #Obtenemos los datos
            username = request.POST['username']
            email = request.POST['email']
            password = request.POST['password']

            #Buscamos el usuario
            u = user_list.filter(username=username)[0]
            
            #Modificamos usuario
            if email:
                u.email=email
            
            if password:
                u.password=password
            
            u.save()

            #Creamos mensaje
            messages.success(request, 'El usuario ha sido modificado satisfactoriamente.')

        if request.POST['action'] == 'delete':
            #Obtenemos los datos
            username = request.POST['username']

            #Eliminamos usuario
            u = user_list.filter(username=username)[0].delete()

            #Creamos mensaje
            messages.success(request, 'El usuario ha sido eliminado satisfactoriamente.')

    # Contexto
    context = {
        "user_list" : user_list,
    }

    return render(
        request, 
        'videocorn/users.html',
        context,
    )