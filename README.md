Pulse check
===========

A system to send pulse check to urls and record metrics:

## `pulse_check.py`
A script that check response from URLs and whether they contain a certain regular expression. 
Then sends this information to a kafka topic.

## `write_metrics.py`
A script that listens to the kafka topic, reads the data from there, and then writes it to postgres
instances.

# Installation
1. Create a virtualenv with python 3.7 or above
2. Activate the virtualenv
3. Install the packages in `requirements.txt`
```
virtualenv env -p `which python3.8`
source env/bin/activate
pip install -r requirements.txt
``` 

# Configuration
All configuration is done under `settings.py`, configuration includes kafka configuration as postgres configuration.
Notice the schema used for the table is:
```
 id serial PRIMARY KEY,
 url varchar(200) not null,
 access_time decimal not null,
 start_time timestamp not null,
 status_code int,
 regex varchar(200),
 regex_found boolean
```
if a table exists with a different schema, that might cause an error.

Note: No ORM was used.

# Running

Check that kafka and postgres are running and the configuration in `settings.py` is correct. 

## Pulse checker
```
usage: python pulse_check.py [-h] [--urls URLS [URLS ...]] [--sleep SLEEP] [--regex REGEX]

pulse check

optional arguments:
  -h, --help            show this help message and exit
  --urls URLS [URLS ...]
                        URLs to check
  --sleep SLEEP, -s SLEEP
                        Seconds between checks
  --regex REGEX         Regular expression to check for in URL
```

for example:
```
python pulse_check.py --urls 'http://www.google.com' 'http://www.ynet.co.il' --regex 'itemtype'
```

## Metrics writers
```
python write_metrics.py
```
