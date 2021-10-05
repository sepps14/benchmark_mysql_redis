import json
import requests


HOST = 'localhost'
PORT = 5000
N = 1000


mysql_insert_times = 'mysql_insert_times.txt'
mysql_increment_times = 'mysql_increment_times.txt'

redis_insert_times = 'redis_insert_times.txt'
redis_increment_times = 'redis_increment_times.txt'


def get_request_time(service, resource_id, increment=False):
    resource_url = f'http://{HOST}:{PORT}/{service}/{resource_id}'
    if increment:
        resource_url = f'{resource_url}/increment'

    resp = requests.post(resource_url)
    data = json.loads(resp.text)
    return data['time']

##### Start by inserting
mysql_i = []
redis_i = []
for i in range(N):
    # inserts rows into mysql table `test`.`stats`
    # inserts key `things_{i}` into redis
    mysql_i.append(get_request_time('mysql', i))
    redis_i.append(get_request_time('redis', i))

with open(mysql_insert_times, 'w') as m_f, open(redis_insert_times, 'w') as r_f:
    for m, r in zip(mysql_i, redis_i):
        m_f.write(f'{m}\n')
        r_f.write(f'{r}\n')

mysql_inc = []
redis_inc = []
for i in range(N):
    # increment records in mysql table `test`.`stats`
    # increment values for `things_{i}` in redis
    mysql_inc.append(get_request_time('mysql', i, True))
    redis_inc.append(get_request_time('redis', i, True))

with open(mysql_increment_times, 'w') as m_f, open(redis_increment_times, 'w') as r_f:
    for m, r in zip(mysql_inc, redis_inc):
        m_f.write(f'{m}\n')
        r_f.write(f'{r}\n')
