from django.shortcuts import render
from .models import Genre, Year, Score, Actor, Movie
from django.contrib.auth.decorators import login_required
from .decorators import admin_required, videocorn_required

@login_required
@videocorn_required
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
@videocorn_required
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


from django.contrib.auth.models import User, Group
from django.contrib import messages 
from django.contrib.auth.hashers import make_password

@login_required
@admin_required
def users(request):

    #Obtenemos lista de usuarios
    user_list = User.objects.all().order_by('username')

    #Obtenemos peticion
    if request.method == "POST":

        # Añadir Usuario
        if request.POST['action'] == 'add':
            
            #Obtenemos los datos
            username = request.POST['username']

            #Si el usuario no existe, lo creamos
            if user_list.filter(username=username).count() == 0:
                email = request.POST['email']
                password = request.POST['password']
                first_name = request.POST['first_name']
                last_name = request.POST['last_name']

                #Hacemos el hash de la contraseña
                password_hash = make_password(password)
                
                #Creamos nuevo usuario
                u = User(username=username, email=email, password=password_hash, first_name=first_name, last_name=last_name)
                u.save()
                
                #Lo añadimos al grupo correspondiente
                group = Group.objects.get(name='usuario_videocorn') 
                group.user_set.add(u)

                #Creamos mensaje
                messages.success(request, 'El usuario ha sido creado satisfactoriamente.')

            else:
                #Creamos mensaje
                messages.error(request, 'El username introducido no se encuentra disponible.')

        # Modificar Usuario
        if request.POST['action'] == 'edit':
            
            #Obtenemos los datos
            username = request.POST['username']
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            email = request.POST['email']
            password = request.POST['password']

            #Buscamos el usuario
            u = user_list.filter(username=username)[0]
            
            #Modificamos usuario
            if email:
                u.email=email
            
            if password:
                #Hacemos el hash de la contraseña
                password_hash = make_password(password)
                u.password=password_hash
            
            if first_name:
                u.first_name=first_name
            
            if last_name:
                u.last_name=last_name
            
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


import http.client
import json

@login_required
@admin_required
def movies(request):

    #Obtenemos lista de peliculas
    movie_list = Movie.objects.all().order_by('title')

    #Obtenemos peticion
    if request.method == "POST":

        # Añadir Pelicula
        if request.POST['action'] == 'add':
            
            #Obtenemos los datos del formulario
            title = request.POST['title']
            trailer = request.POST['trailer']

            #Eliminamos espacios
            title = title.replace(" ", "%20")
  
            #Conexión y petición a la API
            conn = http.client.HTTPSConnection("api.themoviedb.org")
            payload = "{}"
            conn.request("GET", "/3/search/movie?include_adult=false&page=1&query="+title+"&language=es-ES&api_key=64b77a41bd17c700911e422a9cb047bb", payload)
           
            #Respuesta --> JSON
            res = conn.getresponse()
            data = res.read().decode('utf-8')
            themovie = json.loads(data)

            #Si la pelicula existe en la base de datos de la API
            if themovie['total_results'] != 0:
               
                #Obtenemos el titulo original
                title = themovie['results'][0]['title']

                #Comprobamos que la pelicula no existe en la base de datos
                if Movie.objects.all().filter(title__iexact=title).count() == 0:
                    overview = themovie['results'][0]['overview']
                    year = Year(date=themovie['results'][0]['release_date'][:4])#Cogemos solo el año
                    year.save()
                    cover = "https://image.tmdb.org/t/p/w1280" + themovie['results'][0]['poster_path']
                    score = Score(stars=int (round (((themovie['results'][0]['vote_average']*5)/10),0)))#Cambiamos a una puntuacion sobre 5
                    score.save()
                    genres = themovie['results'][0]['genre_ids'] #Lista de ids de los generos
                    
                    #Consulta de los generos
                    conn.request("GET", "/3/genre/movie/list?language=es-ES&api_key=64b77a41bd17c700911e422a9cb047bb", payload)
                    
                    #Respuesta --> JSON
                    res = conn.getresponse()
                    data = res.read().decode('utf-8')
                    themovie_genres = json.loads(data)

                    #Obtenemos los nombres de los generos
                    genre = []
                    for genre_database in themovie_genres['genres']:
                        if genre_database['id'] in genres: 
                            genre.append(Genre(name=genre_database['name']))
                            
                    #Consulta del CAST
                    id = themovie['results'][0]['id'] #id de la API
                    conn.request("GET", "/3/movie/"+ str(id) +"/credits?api_key=64b77a41bd17c700911e422a9cb047bb", payload)

                    #Respuesta -->JSON
                    res = conn.getresponse()
                    data = res.read().decode('utf-8')
                    themovie_cast= json.loads(data)

                    #Obtenemos el director
                    director = []
                    cast = []
                    if themovie_cast ['cast']:
                        director = themovie_cast['crew'][0]['name']
                        #Obtenemos el cast
                        for actor in themovie_cast['cast'][:4]:
                            cast.append(Actor(id=actor['id'],fullName=actor['name']))
                
                    #Creamos una nueva pelicula
                    m = Movie(title=title, trailer=trailer, overview=overview, year=year, director=director, cover=cover, score=score)
                    m.save()

                    #Asignamos generos
                    for g in genre:
                        g.save()
                        m.genre.add(g)
                
                    #Asignamos actores
                    for c in cast:
                        c.save()
                        m.cast.add(c)

                    #Creamos mensaje
                    messages.success(request, 'La pelicula ha sido añadida a la base de datos satisfactoriamente.')

                else: 
                    #Creamos mensaje
                    messages.error(request, 'La pelicula ya se encontraba en la base de datos, por lo que no ha sido necesario añadirla.')
            else: 
                #Creamos mensaje
                messages.error(request, 'La pelicula no se ha encontrado en la librería por lo que no ha sido posible añadirla.')

        
        if request.POST['action'] == 'edit':

            #Obtenemos los datos
            title = request.POST['title']
            trailer = request.POST['trailer']
            overview = request.POST['overview']
            year = request.POST['year']
            director = request.POST['director']
            cast = request.POST['cast']
            cover = request.POST['cover']
            score = request.POST['score']
            genre = request.POST['genre']

            #Buscamos la pelicula
            m = movie_list.filter(title=title)[0]

            #Modificamos la pelicula
            if trailer:
                m.trailer=trailer
            
            if overview:
                m.overview=overview
            
            if year:
                y = Year(date=year)
                y.save()
                m.year=y
            
            if director:
                m.director=director
            
            if cast:
                c = cast.split(',')
                for actor in c:
                    if Actor.objects.all().filter(fullName=actor).count() != 0:
                        m.actor=Actor.objects.all().filter(fullName=actor)[0]
                    else:
                        messages.error(request, 'El actor "' + actor + '" no se encuentra en la base de datos. Añadalo manualmente.')
                
            if cover: 
                m.cover=cover
            
            if score:
                s = Score(stars=score)
                s.save()
                m.score=s
            
            if genre:
                g = genre.split(',')
                for genero in g:
                    aux = Genre(name=genero)
                    aux.save()
                    m.genre.add(aux)
            
            m.save()

            #Creamos mensaje
            messages.success(request, 'La pelicula ha sido modificada satisfactoriamente.')

        # Eliminar Pelicula
        if request.POST['action'] == 'delete':
            #Obtenemos los datos
            title = request.POST['title']

            #Eliminamos usuario
            m = movie_list.filter(title=title)[0].delete()

            #Creamos mensaje
            messages.success(request, 'La película ha sido eliminada satisfactoriamente.')

    # Contexto
    context = {
        "movie_list" : movie_list,
    }

    return render(
        request, 
        'videocorn/movies.html',
        context,
    )