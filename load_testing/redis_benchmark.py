import redis
import time


client = redis.Redis(

    host="localhost",

    port=6379
)

start = time.time()

for index in range(10000):

    client.set(

        f"key-{index}",

        "benchmark"
    )

end = time.time()

print(end - start)