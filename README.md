# owlhacks-server

owlhacks-server is a REST API implemented using FastAPI.
It allows for live closed captioning using AssemblyAPI.
Must be paired with the [client side](https://github.com/jonathan-d-zhang/owlhacks-client).
We used Redis to keep track of the active rooms and store the transcript data.

# To use
```terminal
$ git clone https://github.com/jonathan-d-zhang/owlhacks-server.git
$ cd owlhacks-server
$ docker compose up
```

You will need to obtain your own API key to use the API, though.
