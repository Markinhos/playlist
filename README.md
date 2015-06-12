#Take a home code test

Hi there,

I have coded the backend part of the Playlist manager code test. In order to do so, I have used [Tornado] (http://tornado.readthedocs.org/en/latest/index.html) as a web framework. I know that the instructions stated to try to avoid third party libraries but I don't think I was expected to code the HTTP parsing!

The reasons why I chose this framework are:
 * Is a light framework, so it doesn't give a whole stack like Django does. It just provide the http routing and a simple templating system so I can show I organize and deal with the code.

 * It is not just a web framework but a server, and a asynchronous one. Considering that the playlist manager has to be used by millions of persons, this let answer the request in a non-blocking way.

Regarding the database I have used locally a mongodb instance, using [Motor] (https://motor.readthedocs.org/en/stable/index.html) as driver (which is asynchronous). If you don't have mongodb or you don't want to install it I have coded a fake db which stores in memory the data. When the application starts if it is not able to connect to mongodb it fallbacks to the fake database.

##Folders and code

The code is structured as a traditional MVC application. There are four folders:

- **templates**: Here are the templates used in the application.
    - Get: Shows a playlist and its content. Also has the search form and will display the search results.
    - List: Shows all the lists and the forms to create a new one.


- **controllers**: All the files that deal with the http request and responses. They have to call the model in order to manipulate or retrieve the data, and render the proper view. As the front end is not implemented no DELETE or PUT methods are going to be sent (as html form does only allow POST and GET), so it is a bit modified of what it is supposed to be a RESTful interface.
    - playlists: Deal with the CRUD actions for the Playlist model.
    - search: Deal with the search to the Spotify API.


- **models**: All the files that contains the logic and the interaction with the database or with external APIs.
     - playlist: Retrieve and modified documents of Playlist. The methods that modify an existing document are using the atomic modifiers from mongodb so there are no **concurrency** problems. That avoids two users adding a song, and the last one replacing the content of the first one.
     - search: Request data to external services. It has a simple cache that stores previous queries. In a real scenario you better use something like memcached or Redis.

- **database**: Database initialization and FakeDatabase compatible in this test with Motor api.

- **lib**: Implmentation of a LRU cache.

Additionally there is another folder:

- **tests**: Contains all the tests.
    - unit: All the unit tests.
        - playlist_model: Tests for the playlist model. All the dependencies are mocked.
        - search_model: Tests for the search model with mocked dependencies.
