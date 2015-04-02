# The Bart App
Tired of clicking a million buttons to check when your train departs?

This app allows you to open a browser and view departure times from your closest station.

## The Stack
The frontend is lightweight, using basic jQuery.

The backend is powered by [Django](http://www.djangoproject.com/), hosted on Amazon EC2, and runs:
1. gunicorn server
2. celery to asynchronously fetch data from BART API
3. supervisor to daemonize above processes
4. nginx to serve static files
5. postgresql

Click [here](http://52.11.27.205:9000/) to see the app, be sure to enable geolocation.

## TODO List
- Websockets to push updated times
- Prettify frontend
- GeoDjango for more efficient distance calculation
