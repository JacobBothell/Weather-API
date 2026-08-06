import threading
import queue
import time

from dotenv import load_dotenv
import os
import json

#import local packages
import webAPI
#import cacheWorker

config_file_name = 'config.json'

if __name__ == "__main__":
    #load env and config
    with open(config_file_name, 'r') as file:
        config = json.load(file)

    load_dotenv()
    config['weather_api']['api_key'] = os.getenv("WEATHER_API_KEY")
    config['location_api']['api_user'] = os.getenv("GEO_USERNAME")

    #create thread queues
    #add_to_cache_queue = queue.Queue()
    #cache_validation_queue = queue.Queue()

    #create 'public' data structures
    weather_cache = {}
    request_logs = {}

    #initialize cache
    #cache = cacheWorker.cacheWorker(add_to_cache_queue, cache_validation_queue, weather_cache, config['cache']['overload'])

    #initialize web api
    webAPI.app.state.weather_cache = weather_cache
    webAPI.app.state.request_logs = request_logs
    if 'weather_api' in config:
        webAPI.app.state.weather_api = config['weather_api']
    else:
        print("weather api information missing from config.json")
    #if 'location_api' in config:
    #    webAPI.app.state.location_api = config['location_api']
    #else:
    #    print("location api information missing from config.json")
    if 'cache' in config:
        if 'renew' in config['cache']:
            if 'renew_time' in config['cache']['renew']:
                webAPI.app.state.cache_max_age = config['cache']['renew']['renew_time']

    #create threads
    threads = []
    server_thread = threading.Thread(target=webAPI.run_server, daemon=True)
    threads.append(server_thread)
    #cache_thread = threading.Thread(target=cache.run, daemon=True)
    #threads.append(cache_thread)

    #start threads
    for thread in threads:
        thread.start()

    #wait for keyboard interrupt to exit
    try:
        while True:
            time.sleep(100)
    except KeyboardInterrupt:
        print("Keyboard Interrupt Received")

        #threads are daemons so they will exit
        #this could be done cleaner to perform tasks before shutdown
          # flush cache to disk
          # finish / close current requests
