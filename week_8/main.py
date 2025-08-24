import redis

redis_client = redis.Redis(
    host= "redis-13476.c266.us-east-1-3.ec2.redns.redis-cloud.com",
    port= 13476,
    password= "3GbwCdhSMzHbKLvaMc3g7nxkg4Qfsugq"
)

connection_status = redis_client.ping()
if connection_status:
    print("Connected")
else:
    print("not connected")