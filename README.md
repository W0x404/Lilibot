[![Social](https://img.shields.io/badge/Twitter-W0x404-blue.svg?style=flat-square)](http://www.twitter.com/W0x404)

# Lilibot
## Any release has been published yet /!\
![Version](https://img.shields.io/badge/Version-0.1-lightgrey.svg?style=flat-square) 
SQLi - SQLinjection bot. Not a botnet, not viral bot,  not a malware.
- Python 2.7
- Linux


Lilibot is a bot, crawling each web page in order to gather url. After collecting the url, the bot detects URLs containing a potential SQL injection.

First created to detect the vulnerabilities, the next goal is to use the robot to highlight the number of exploitable vulnerabilities.

In dev, any release has been published yet.

*Save time. Keep the control.*

# How to Install ?

##Set up a database (easy ~20 secs)
`create database lilibot;`

###Feed the database with scope table and sqli table.
`use lilibot;`
`create table scope ( host varchar(200), url varchar(200), unique (url));`
`create table sqli (url varchar(200));`

###Insert a url in the scope table.
`insert into scope values ("http://ianonavy.com", "http://ianonavy.com/files/urls.txt");`
This url provide a long list of websites. A good start.

##Download dependencies (easy ~40 secs)
`sudo apt-get update && apt-get install python-pip python-mysqldb && sudo pip install requesocks`

#Run the .py with option
* `--tor` Provide a connection throw Tor
* `--sqli` Allow vulnerable url detection
* `--sonly` Only dectect vulnerable dection. Any url will be added to the scope.

