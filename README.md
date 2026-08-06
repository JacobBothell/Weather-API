# Weather-API
Example Python weather API using FastAPI, caching, request logs, and multithreading

# Run Instructions
### Python environment

This project was developed on Python 3.10.6, but I believe any Python 3 version should work

initialize a virtual environment `python -m venv .venv`

install required dependencies `pip install -r requirements.txt`

### env configuration

- copy example.env to .env
- fill out with api keys / user names
  - an api key for the weather data can be created by going to https://www.weatherapi.com/signup.aspx
  - the location API is currently not used

### Run Script

With your venv created above active run `python main.py`

this will start the server on `http://0.0.0.0:8000`

`CTRL+C` can be used to stop the application


# Future Improvements
- Implement and integrate the threaded caching strategy
- Potentially seperate threads out to seperate processes
- Add integration of time series DB (InfluxDB / Prometheus / MongoDB) or Elasticsearch for historical data
- Modify endpoints to enable utilization of external nginx / cloudflare caching
- Package project into Docker container
- Implement and integrate the 'Overloading' functionality for improved cache hits