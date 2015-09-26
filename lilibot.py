#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  lilibot.py
#  
#  Copyright 2015 W. @W0x404
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  
import MySQLdb, subprocess, re, thread, requests, argparse
 
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    
 
class DB():
	"""
		Class usefull to manage database. Made by W. You should replace
		details by yours
	"""
	def __init__(self, args):
		print "Gathering database's details..."
		self.host = raw_input("Host: ") # replace it by raw_input if you want
		self.user = raw_input("User: ") # replace it by raw_input if you want
		self.password = raw_input("Password: ") # dangerous to write the password
		self.database = raw_input("Database: ") # replace it
		self.db = ""
		self.cursor = ""
		print "Database's details gathered..."
		self.connect() # auto connect. Perfect.
	   
	def connect(self):
		"""
			Function to test the connection to your database.
			1) build the database object.
			2) build the cursor
			3) no error, well connected. 
		"""
		print "Testing the connexion to the database...",
		try:
			self.db = MySQLdb.connect(self.host,self.user, self.password, self.database)
			self.cursor = self.db.cursor()
			print bcolors.OKGREEN + "Database well configured." + bcolors.ENDC
		except MySQLdb.Error, e:
			print bcolors.FAIL + "Mysql sent error(s): {}".format(e) + bcolors.ENDC
			exit(0)
   
	def query(self, sql, v=0, r=0):
		"""
			Best way to execute a query. Dont create insert or select
			function.
		"""
		try:
			# Execute the SQL command
			self.cursor.execute(sql)
			# Commit your changes in the database
			self.db.commit()
			# Fetch result
			data = self.cursor.fetchall()
			# v for a verbose mode
			if (v==1):
				print data
			# r for return mode
			if (r==1):
				return data
		   
		except MySQLdb.Error, e:
			# Rollback in case there is any error
			self.db.rollback()
			print bcolors.FAIL + "Mysql sent error(s): {}".format(e) + bcolors.ENDC
			
   
	def close(self):
		"""
			Don't forget to clean the database and the password.
		"""
		self.db.close()
		self.db = ""
		self.cursor = ""
		self.password = ""
 
class Carving():
	"""
		The carving creates a bot to carve raw web page. dont forget
		to insert a first url in the database.
		> insert into DATABASE value ("http://cyber-exploit.com","http://cyber-exploit.com");
	"""
	def __init__(self, database, args):
		self.database = database
		print bcolors.WARNING + "Creating carving bot...\n\n" + bcolors.ENDC,
		   
		while (1):
			self.url = ""
			self.rand_url()
			print bcolors.WARNING+"°"+ bcolors.ENDC + bcolors.UNDERLINE + "Carving "+self.url+ bcolors.ENDC
			self.raw_page = self.get_page(args)
			if args.sonly == True:
				self.carve_sqli()
			if args.sonly == False:
				self.carve_url()
			if args.sqli == True:
				self.carve_sqli()
 
	   
	def get_page(self, args):
		"""
			perform requests
		"""
		raw = ""
		sock_proxy = "localhost:9050"
		proxyDict = { "socks": sock_proxy }
		try:
			if args.tor == False:
				raw = requests.get(self.url, timeout=3)
			if args.tor == True:
				raw = requests.get(self.url, timeout=3, proxies=proxyDict)
			raw = raw.content
			return raw
		except:
			raw = ""
			pass
		
	   
	def carve_url(self):
		"""
			Regex to detect http url. https is not pertinent: too secure.
			Store the url.
		"""
		regex_url = ur"(http://[\.[\w_-][^\[\]<>\n \"\(\)]+]*)"
		regex_dn = ur"(http://[\.[\w_-]*)"
		
		try:
			urls = re.findall(regex_url, self.raw_page)
			urls = set(urls)
			
			url_dn = list()
			for e in urls:
				url_dn.append((re.findall(regex_dn,e), e))
			
			if (len(urls) > 0):
				print bcolors.HEADER +"Adding "+str(len(urls))+bcolors.ENDC+" to the scope. Duplicated url(s) will be ignored."
				#little weird but working fine.
				for e in url_dn:
					q = 'INSERT IGNORE INTO scope VALUES ("%s", "%s") ON DUPLICATE KEY UPDATE url = url;' % (e[0][0], e[1])
					self.database.query(q)
		except:
			pass
		   
	def carve_sqli(self):
		"""
			Regex to detect php url and store it.
		"""
		try:
			urls = re.findall('http://[\.[\w_-][^\[\]<>\n "]+.php\?[\w=&]*', self.raw_page)
			urls = set(urls)
			if (len(urls) > 0):
				print bcolors.OKBLUE + bcolors.BOLD + "Adding "+str(len(urls))+ bcolors.ENDC+" to the sqli table. Duplicated url(s) will be ignored."
				#little weird but working fine.
				for e in urls:
					self.database.query('INSERT IGNORE INTO sqli VALUES ("%s") ON DUPLICATE KEY UPDATE url = url;' % (e))
		except:
			pass
   
	def clean_url(self):
		"""
			Delete the url in the first version. Flag it the next.
		"""
		print "Deleting url ("+ self.url +")from the scope...\n"
		self.database.query('DELETE FROM scope WHERE url = "%s";' % (self.url))
		
		   
	def rand_url(self):
		"""
			Get a rand url for the carving. need 1 url in the database to work.
		"""
		self.url = self.database.query('SELECT url FROM scope ORDER BY RAND() LIMIT 1', r=1)[0][0]
	   
def main():
	parser = argparse.ArgumentParser(description='Start a bot to detect injectable url.')
	parser.add_argument('--tor', dest='tor', action='store_true', help='Provide connection with Tor.')
	parser.add_argument('--sqli', dest='sqli', action='store_true', help='Allow looking for sqli url.')
	parser.add_argument('--sonly', dest='sonly', action='store_true', help='Only looking for sqli url.')
	parser.add_argument('--debug', dest='debug', action='store_true', help='Debug display.')
	
	args = parser.parse_args()
	
	database = DB(args) # create the db
	thread.start_new_thread(Carving(database, args)) # create one thread.
	return 0
 
if __name__ == '__main__':
	main()
