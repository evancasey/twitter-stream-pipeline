twitter-stream-pipeline
======================

Easily collect tweets off of the Twitter streaming API and store them in SQLite3. 

Setup
-----
Create a `tokens.py` file with your Twitter API tokens:
```python
CONSUMER_KEY = ''
CONSUMER_SECRET = ''
ACCESS_TOKEN = ''
ACCESS_TOKEN_SECRET = ''
```
Create a `keywords.txt` containing the words you'd like to query for, separated by line:
```
word1
word2
```

Running Locally
---------------

Start collecting tweets on your local machine:
```bash
$ python runner.py -k keywords.txt -e your_email@gmail.com
```

Running on AWS
--------------

If you'd like to collect tweets on a remote machine, set up a free tier AWS EC2 instance [here](http://aws.amazon.com/ec2/).

On your EC2 instance, run:
```bash
$ sudo yum install git
$ git clone https://github.com/evancasey/twitter-stream-pipeline.git
$ cd twitter-stream-pipeline && pip install -r requirements.txt
```

Create your `tokens.py` and `keywords.txt` files and then kick off the runner as usual:
```bash
$ python runner.py -k keywords.txt -e you_email@gmail.com
```
