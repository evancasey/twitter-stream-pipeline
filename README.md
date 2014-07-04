twitter-stream-pipeline
===========

Easily collect tweets off of the Twitter streaming API and store them in SQLite3. 

Setup
-----
Create a tokens.py file with your Twitter API tokens:
```python
CONSUMER_KEY = ''
CONSUMER_SECRET = ''
ACCESS_TOKEN = ''
ACCESS_TOKEN_SECRET = ''
```

Create a keywords.txt containing the words you'd like to query for
```
word1
word2
```

Running Locally
---------------

It's easy to start collecting tweets on your local machine
```bash
$ python runner.py -k keywords.txt -e your_email@gmail.com
```


Running on Digital Ocean
------------------------



Run:
```bash
$ 
```

