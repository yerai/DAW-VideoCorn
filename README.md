<h1>Web Applications - VideoCorn</h1>

<h3>Goal</h3>
<p>The aim of this project is to implement a web application similar 
to an online video store. This platform will display multimedia information obtained both 
from Youtube and The Movie Database. <p>
  
![alt text](https://github.com/yerai/yerai.github.io/blob/master/images/video-corn.jpg?raw=true)
  

<h3>Non-functional requirements</h3>
<ul>
  <li>The server will be implemented using Django</li>
  <li>On the client side, HTML, CSS and Boostrap will be used</li>
  <li>The web application will need to have a Database</li>
  <li>All screens of the application should be responsive</li>
</ul>

<h3>Functional requirements</h3>
<ul>
  <li>Two user roles are needed
  <ul>
        <li>User: access media</li>
        <li>Admin: modifies and uploads media</li>
   </ul>
  </li>
  <li>All users will need to log in before using the application</li>
  <li>All users will be able to filter and search movies withing the application. This search functionality will need to use at least the name of the movie</li>
  <li>When a movie is selected, both its information and movie trailer will be shown</li>
  <li>Admin users will be able to create, update and delete users on the system</li>
  <li>Admin users will be able to create, update and delete movies on the system. To add new movies, only two fields should be required:
	<ul>
        <li>Title of the movie</li>
	      <li>Trailer video link</li>
  </ul>
  </li>
  <li>When a new movie is added, the system will retrieve all its information from The Movie Database and add it to the system. This will be done using The Movie Database's API</li>
</ul>
