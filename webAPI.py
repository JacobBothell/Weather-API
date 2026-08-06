from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, status
import uvicorn

import json
import requests

from datetime import datetime

@asynccontextmanager
async def lifespan(app: FastAPI):
    '''
    Function will run first and last allowing for loading / checking info
    '''
    print("FastAPI Starting")
    if 'weather_api' in app.state:
        if 'url' not in app.state.weather_api:
            print("Weather API config missing URL")
            #should kill / fail script here
        if 'api_key' not in app.state.weather_api:
            print("Missing API key for weather API")
            #should kill / fail script here
    else:
        print("Weather API config missing")
        #should kill / fail script here

    #TODO: add check for cache invalidate time
    #TODO: add check for location api info

    yield
    print("FastAPI Stopping")

#Initialize Fast API instance
app = FastAPI(lifespan=lifespan)

def createLog(weather_data: dict, cache_hit: bool) -> bool:
    '''
    log user request to dictionary for later recall

    returns bool of success
    '''
    try:
        #TODO: there is more information about the request in weather_data that might be useful for api metrics but just keeping the weather data portion
        log = {"cache_hit":cache_hit, "response":weather_data.json()}
        app.state.request_logs[datetime.now()] = log
        return True
    except Exception as e:
        print(e)
        return False

def addToCache(weather_data: dict, location: str) -> bool:
    '''
    Adds weather api responses to internal cache

    returns bool of success
    '''
    try:
        app.state.weather_cache[location] = weather_data
        return True
    except Exception as e:
        print(e)
        return False

def getWeatherAPIData(location):
    '''
    reach out to the respective weather api to get fresh data

    currently written to support only api.weatherapi.com

    returns raw request response
    raises HTTP Exception error on bad response codes
    '''
    weather_data_response = requests.get(app.state.weather_api['url'], params={'key':app.state.weather_api['api_key'], 'q':location})
    if weather_data_response.status_code != 200:
        #TODO: add logs here about api failures
        #TODO: make these failures more explicit
        raise HTTPException(
            status_code=weather_data_response.status_code,
            detail=weather_data_response.text
        )

    addToCache(weather_data_response, location)
    return weather_data_response

@app.get('/weather/{location}')
def weatherAtLocation(location: str):
    '''
    Weather data retrieval endpoint

    Utlizes internal cache to reduce external API usage

    Logs user requests to internal memory 'db'
    '''
    #TODO: need to add some safeguards on the location input to avoid injection from outside users
    #check if location in cache
    cache_hit = False
    if location in app.state.weather_cache:
        weather_data_response = app.state.weather_cache[location]
        curr_time = datetime.now()
        cache_hit = True
        if weather_data_response.json()['current']['last_updated_epoch'] > curr_time.timestamp() + app.state.cache_max_age * 1000:
            weather_data_response = getWeatherAPIData(location)
    else:
        weather_data_response = getWeatherAPIData(location)


    createLog(weather_data_response, cache_hit)

    return weather_data_response.json()


@app.get('/requests')
def getRequestLogs():
    '''
    Returns json of user requests from memory 'db'
    '''
    return app.state.request_logs

def run_server():
    '''
    Runs the FastAPI server. This is for threading compatability.
    '''
    #start gateway interface
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level='debug')