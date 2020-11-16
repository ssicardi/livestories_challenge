# livestories_challenge

## Installing
`pip3 install requirements.txt`

## How to Run
`python3 manage.py runserver`

## Site
https://protected-brook-52969.herokuapp.com

## What it does

### Counting Events
- Make a call to /api/events/{EVENT_NAME}/ to count a single occurency of the event in the url and store it in the db

- Make a call to /api/events/{EVENT_NAME}/{NUM}/ to count a {NUM} occurencies of the event in the url and store them in the db

### Get Events from dates
Make a call to /api/events?start_date=YYYYMMDDHH&end_date=YYYYMMDD/ to get all the events in the time frame. Keep in mind:
	- Only start_date allows hours
	- The time frame includes the end date

### List all Events
Make a call to /api/events/unique/ to get a list of all events that ever happened, and a total count for each event

### Graph of events in a given date

Make a call to /api/events/histogram/{EVENT}/{YYYMMDD}/ in your web browser to get a graph of the amount of events on that given day, divided by hour