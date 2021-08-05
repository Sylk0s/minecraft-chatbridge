import redis
import json

configs = json.load(open("publisher/configs.json"))

r = redis.Redis(host=configs['host'], port=configs['port'], password=configs['pass'])
r.publish("messages", "message")