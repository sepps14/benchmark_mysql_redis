import random

import redis

from app.service.service import DataStore

class RedisKV(DataStore):
    RESOURCE = 'things'

    @classmethod
    def from_dict(cls, data: dict):
        r = redis.Redis(host=data['HOST'], port=data['PORT'])
        return cls(r)
    
    def __init__(self, _redis):
        self._redis = _redis
    
    def get_count(self, profile_id: str):
        with self._redis.pipeline() as pipe:
            key = f'{RedisKV.RESOURCE}_{profile_id}'
            try:
                pipe.watch(key)
                current = pipe.get(key)
                if current is None:
                    next_val = random.randint(0,50)

                pipe.multi()
                pipe.set(key, next_val)
                pipe.execute()
            except Exception:
                print('uh oh?')
            finally:
                pipe.reset()

    def increment_count(self, profile_id: str):
        with self._redis.pipeline() as pipe:
            key = f'{RedisKV.RESOURCE}_{profile_id}'
            try:
                pipe.watch(key)
                current = pipe.get(key)
                if current is not None:
                    # values are always byte strings
                    next_val = int(current) + 1

                    pipe.multi()
                    pipe.set(key, next_val)
                    pipe.execute()
            except Exception as e:
                print(f'uh oh? {e}')
            finally:
                pipe.reset()

    def decrement_count(self, profile_id: str):
        with self._redis.pipeline() as pipe:
            key = f'{RedisKV.RESOURCE}_{profile_id}'
            try:
                pipe.watch(key)
                current = pipe.get(key)
                if current is not None:
                    # values are always byte strings
                    next_val = int(current) - 1

                    pipe.multi()
                    pipe.set(key, next_val)
                    pipe.execute()
            except Exception as e:
                print(f'uh oh? {e}')
            finally:
                pipe.reset()
