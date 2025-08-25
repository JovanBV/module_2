import redis
import json
from datetime import datetime

class CacheManager: 
    def __init__(self, host, port, password, *args, **kwargs):
        self.redis_client = redis.Redis(
            host=host,
            port=port,
            decode_responses=True,
            password=password,
            *args,
            **kwargs
        )
        connected_status = self.redis_client.ping()

        if connected_status:
            print("Connected to redis.")
        else:
            print("Not connected to redis.")

    def store_hashed_fruit(self, id, mapping, time_to_live=None):
        try:
            cache_key = f"fruits:{id}"
            self.redis_client.hset(name=cache_key, mapping=mapping)
            if time_to_live:
                self.redis_client.expire(cache_key, time_to_live)
        except redis.RedisError as error:
            print(f"Error storing hash: {error}")

    def store_hash(self, key, mapping, time_to_live=None):
        try:
            self.redis_client.hset(name=key, mapping=mapping)
            if time_to_live:
                self.redis_client.expire(key, time_to_live)
        except Exception as error:
            print("Error storing hash: ", error)

    def store_string(self, key, value, time_to_live=None):
        try:
            if time_to_live:
                self.redis_client.setex(key, time_to_live, value)
            else:
                self.redis_client.set(key, value)
        except redis.RedisError as error:
            print(f"Error storing string: {error}")

    def check_key(self, key):
        try:
            return self.redis_client.exists(key) == 1
        except redis.RedisError as error:
            print("Error: ", error)
            return False

    def get_all_similar_keys(self, key):
        try:
            keys = self.redis_client.keys(f"{key}:*")
            if not keys:
                return []
            
            pipe = self.redis_client.pipeline()
            for k in keys:
                pipe.hgetall(k)
            return pipe.execute()
        except Exception as error:
            print("Error retrieving all similar keys: ", error)

    def get_hash(self, key):
        try:
            return self.redis_client.hgetall(key)
        except Exception as error:
            print("Error getting hash: ", error)

    def delete_fruit(self, key):
        try:
            cache_key = f"fruits:{key}"
            return self.redis_client.delete(cache_key)
        except Exception as error:
            print("Error deleting key: ", error)

    def delete_key(self, key):
        try:
            return self.redis_client.delete(key)
        except Exception as error:
            print("Error deleting key: ", error)

    def _json_serializer(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        raise TypeError(f" {obj} not serializable")

    def set_json(self, key, value, time_to_live=None):
        try:
            json_value = json.dumps(value, default=self._json_serializer)
            if time_to_live:
                self.redis_client.setex(key, time_to_live, json_value)
            else:
                self.redis_client.set(key, json_value)
        except Exception as error:
            print(f"Error storing JSON: {error}")

    def get_json(self, key):
        try:
            value = self.redis_client.get(key)
            if value:
                return json.loads(value)
            return None
        except redis.RedisError as error:
            print(f"Error getting JSON: {error}")
            return None


cache_manager = CacheManager(
    host="redis-13476.c266.us-east-1-3.ec2.redns.redis-cloud.com",
    port=13476,
    password="3GbwCdhSMzHbKLvaMc3g7nxkg4Qfsugq"
)
