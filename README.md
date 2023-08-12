# Webapp2/Strawberry GraphQL Example

## Set it up

```
$ python3 -m venv venv
$ . venv/bin/activate
venv $ pip install -r requirements.txt
```

## Run it

```
$ gunicorn app
[2023-08-12 15:21:43 -0700] [26266] [INFO] Starting gunicorn 21.2.0
[2023-08-12 15:21:43 -0700] [26266] [INFO] Listening at: http://127.0.0.1:8000 (26266)
[2023-08-12 15:21:43 -0700] [26266] [INFO] Using worker: sync
[2023-08-12 15:21:43 -0700] [26267] [INFO] Booting worker with pid: 26267
```

## Try it

Load up GraphiQL at [http://localhost:8000/graphql](http://localhost:8000/graphql).

<img src="https://github.com/rwatkins/webapp2_graphql/raw/main/graphiql.png">
