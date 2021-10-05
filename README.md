# startup

## data stores
Start redis and mysql with `docker compose up -d`

### bootstrap mysql table
```sh
❯ mysql --host 127.0.0.1 --port 3306 --user admin -pfoobar < db/bootstrap/bootstrap.sql
```

## app
```
❯ pyenv virtualenv 3.9.6 benchmark_redis_mysql
❯ pyenv activate benchmark_redis_mysql
❯ pip install -r requirements.txt
❯ pip install -e .
❯ FLASK_RUN_PORT=5000 FLASK_APP=app/server flask run
```


## Run benchmark
```
❯ pyenv activate benchmark_redis_mysql
❯ pip install -r benchmark/requirements.txt
❯ python benchmark/run.py
```

## Histogram
after running the benchmark
```
❯ python benchmark/histogram.py
```