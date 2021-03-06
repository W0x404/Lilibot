[![Social](https://img.shields.io/badge/Twitter-W0x404-blue.svg?style=flat-square)](http://www.twitter.com/W0x404)

# Lilibot
## Any release has been published yet /!\
![Version](https://img.shields.io/badge/Version-0.3-lightgrey.svg?style=flat-square)</br> 
SQLi - SQLinjection bot. Not a botnet, not viral bot,  not a malware.
- Python 2.7
- Linux

**Version 0.1:**First commit. The bot can scan.</br>
**Version 0.2:**The bot can scan through Tor.</br>
**Version 0.3:**Improving perf. Add option and documentation.</br>
**Version 0.4:**(in dev)Improving perf and insert function.</br>

**Version < 0.5:**
       The bot is not able to inject and exploit. Only scanning, probing, crawling.
       

Lilibot is a bot, crawling each web page in order to gather url. After collecting the url, the bot detects URLs containing a potential SQL injection.

First created to detect the vulnerabilities, the next goal is to use the robot to highlight the number of exploitable vulnerabilities.

In dev, any release has been published yet.

*Save time. Keep the control.*

# How to Install (easy ~60 secs)?
*Connect to your mysql server with your id.*

##Set up a database (easy ~20 secs)
`create database lilibot;`

###Feed the database with scope table and sqli table.
`use lilibot;`</br>
`create table sites ( ID int NOT NULL AUTO_INCREMENT, url varchar(200), unique (url), PRIMARY KEY (ID));`</br>
`create table sqli ( ID int NOT NULL AUTO_INCREMENT, url varchar(200), unique (url), PRIMARY KEY (ID));;`</br>

###Insert a url in the scope table.
`insert into sites (url) values ("http://ianonavy.com/files/urls.txt");`</br>
This url provide a long list of websites. A good start.

##Download dependencies (easy ~40 secs)
`sudo apt-get update && sudo apt-get install python-mysqldb` 

#Run the .py with options
* `--tor, -T`             Provide connection with Tor.
* `--sqli, -s`            Allow looking for sqli url.
* `--sonly, -S`           Only looking for sqli url.
* `--host HOST, -H HOST`  Database s host value.
* `--user USER, -u USER`  Database s user value.
* `--pass PASSWORD, -p PASSWORD`
* `--db DB, -d DB`  Database value.

Exemple : </br>
`python lilibot.py -H 192.168.0.1 -u lilibot -p password -d lilibot --sqli`


#Remote Access / User ( easy ~120 secs )
If you want to deploy **lilibot** as a master-slave API, you need to set the database on a standalone server and connect by remote access all bots.
So first, first, Connect to the mysql master server with your id.
Then:

##Create remote user
`use lilibot;`</br> 

`grant select, insert, update on lilibot.* to 'lilibot'@'localhost' identified by 'YOU_PASSWORD';`</br>
`grant select, insert, update on lilibot.* to 'lilibot'@'%' identified by 'YOU_PASSWORD';`</br>

`flush privileges;`</br>
##Allow remote connection

### Edit the my.cnf file
This file is used by mysql to conf the serv.
* If you are using Debian Linux file is located at `/etc/mysql/my.cnf` location.
* If you are using Red Hat Linux/Fedora/Centos Linux file is located at `/etc/my.cnf` location.
* If you are using FreeBSD you need to create a file `/var/db/mysql/my.cnf` location.

Change `bind-adress = 127.0.0.1` by </br>
       `bind-adress = YOUR_PUBLIC_IP`

After, do `sudo service mysql restart`.
###Test your connection with an other pc / slave.
`mysql -ulilibot -pYOUR_PASSWORD -hYOU.PULIC.IP.ADRESS -Dlilibot`
