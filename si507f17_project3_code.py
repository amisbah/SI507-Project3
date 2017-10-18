from bs4 import BeautifulSoup
import unittest
import requests
import csv

#########
## Instr note: the outline comments will stay as suggestions, otherwise it's too difficult.
## Of course, it could be structured in an easier/neater way, and if a student decides to commit to that, that is OK.

## NOTE OF ADVICE:
## When you go to make your GitHub milestones, think pretty seriously about all the different parts and their requirements, and what you need to understand. Make sure you've asked your questions about Part 2 as much as you need to before Fall Break!


######### PART 0 #########

# Write your code for Part 0 here.
try:
	gallery_alttext = open("alttext.html",'r').read()
except:
	gallery_alttext = requests.get("http://newmantaylor.com/gallery.html").text
	f = open("alttext.html",'w')
	f.write(gallery_alttext)
	f.close()

soup = BeautifulSoup(gallery_alttext,'html.parser')

image_list = soup.find_all('img')

# for img in image_list:
# 	alttext = img.get('alt')
# 	if alttext == None:
# 		print("No alternative text provided!")
# 	else:
# 		print(alttext)

######### PART 1 #########

# Get the main page data...

# Try to get and cache main page data if not yet cached
# Result of a following try/except block should be that
# there exists a file nps_gov_data.html,
# and the html text saved in it is stored in a variable 
# that the rest of the program can access.

# We've provided comments to guide you through the complex try/except, but if you prefer to build up the code to 
# do this scraping and caching yourself, that is OK.

try:
	main_html = open("nps_gov_data.html",'r').read()
except:
	main_html = requests.get("https://www.nps.gov/index.htm").text
	f = open("nps_gov_data.html",'w')
	f.write(main_html)
	f.close()

# Get individual states' data...

# Result of a following try/except block should be that
# there exist 3 files -- arkansas_data.html, california_data.html, michigan_data.html
# and the HTML-formatted text stored in each one is available
# in a variable or data structure 
# that the rest of the program can access.

# TRY: 
# To open and read all 3 of the files

# But if you can't, EXCEPT:

# Create a BeautifulSoup instance of main page data 

soup = BeautifulSoup(main_html,'html.parser')

# Access the unordered list with the states' dropdown

state_dropdown = soup.find('ul',{'class':'dropdown-menu SearchBar-keywordSearch'})

# Get a list of all the li (list elements) from the unordered list, using the BeautifulSoup find_all method

state_list = state_dropdown.find_all('li')

# Use a list comprehension or accumulation to get all of the 'href' attributes of the 'a' tag objects in each li, 
# instead of the full li objects

state_list_links = []

for each in state_list:
	state_name = each.find('a')
	state_link = state_name.get('href')
	state_list_links.append(state_link)

# Filter the list of relative URLs you just got to include only the 3 you want: AR's, CA's, MI's, using the 
# accumulator pattern & conditional statements

three_states = []

for each in state_list_links:
	if 'ar' in each:
		three_states.append(each)
	if 'ca' in each:
		three_states.append(each)
	if 'mi' in each:
		three_states.append(each)

# Create 3 URLs to access data from by appending those 3 href values to the main part of the NPS url. Save each URL 
# in a variable.

## To figure out what URLs you want to get data from (as if you weren't told initially)...
# As seen if you debug on the actual site. e.g. Maine parks URL is "http://www.nps.gov/state/me/index.htm", Michigan's 
# is "http://www.nps.gov/state/mi/index.htm" -- so if you compare that to the values in those href attributes you just 
# got... how can you build the full URLs?

for each in three_states:
	if 'mi' in each:
		url_mi = "https://www.nps.gov{}".format(each)
	if 'ar' in each:
		url_ar = "https://www.nps.gov{}".format(each)
	if 'ca' in each:
		url_ca = "https://www.nps.gov{}".format(each)

# Finally, get the HTML data from each of these URLs, and save it in the variables you used in the try clause
# (Make sure they're the same variables you used in the try clause! Otherwise, all this code will run every time you 
# run the program!)


# And then, write each set of data to a file so this won't have to run again.

try:
	arkansas_html = open("arkansas_data.html",'r').read()
	california_html = open("california_data.html",'r').read()
	michigan_html = open("michigan_data.html",'r').read()
except:
	arkansas_html = requests.get(url_ar).text
	f_ar = open("arkansas_data.html",'w')
	f_ar.write(arkansas_html)
	f_ar.close()
	california_html = requests.get(url_ca).text
	f_ca = open('california_data.html','w')
	f_ca.write(california_html)
	f_ca.close()
	michigan_html = requests.get(url_mi).text
	f_mi = open('michigan_data.html','w')
	f_mi.write(michigan_html)
	f_mi.close()

######### PART 2 #########

## Before truly embarking on Part 2, we recommend you do a few things:

# - Create BeautifulSoup objects out of all the data you have access to in variables from Part 1
# - Do some investigation on those BeautifulSoup objects. What data do you have about each state? How is it 
# organized in HTML?

# HINT: remember the method .prettify() on a BeautifulSoup object -- might be useful for your investigation! So, 
# of course, might be .find or .find_all, etc...

# HINT: Remember that the data you saved is data that includes ALL of the parks/sites/etc in a certain state, but 
# you want the class to represent just ONE park/site/monument/lakeshore.

# We have provided, in sample_html_of_park.html an HTML file that represents the HTML about 1 park. However, your 
# code should rely upon HTML data about Michigan, Arkansas, and Califoria you saved and accessed in Part 1.

# However, to begin your investigation and begin to plan your class definition, you may want to open this file and 
# create a BeautifulSoup instance of it to do investigation on.

# Remember that there are things you'll have to be careful about listed in the instructions -- e.g. if no type of 
# park/site/monument is listed in input, one of your instance variables should have a None value...


## Define your class NationalSite here:

class NationalSite(object):
	def __init__(self,object):
		self.location = object.find('h4').text
		self.name = object.find('h3').text
		if object.find('h2').text == "":
			self.type = None
		else:
			self.type = object.find('h2').text
		if object.find('p').text == "":
			self.description = ""
		else:
			self.description = object.find('p').text.strip()
		park_links = object.find('div',{'class':'stateListLinks'})
		park_list = park_links.find_all('li')
		self.park_url = park_list[0].find('a').get('href')

	def __str__(self):
		return "{} | {}".format(self.name, self.location)

	def get_mailing_address(self):
		site_html = requests.get(self.park_url).text
		site_soup = BeautifulSoup(site_html,'html.parser')
		park_address = site_soup.find('p',{'class':'adr'})
		park_adr_span = park_address.find_all('span')
		address = ""
		for each in park_adr_span:
			address += each.text
		stripped_address = address.strip()
		formatted_address = stripped_address.replace('\n',' / ')
		return formatted_address

	def __contains__(self,x):
		if x in self.name:
			return True
		else:
			return False

## Recommendation: to test the class, at various points, uncomment the following code and invoke some of the 
# methods / check out the instance variables of the test instance saved in the variable sample_inst:

# f = open("sample_html_of_park.html",'r')
# soup_park_inst = BeautifulSoup(f.read(), 'html.parser') # an example of 1 BeautifulSoup instance to pass into your class
# sample_inst = NationalSite(soup_park_inst)
# f.close()

######### PART 3 #########

# Create lists of NationalSite objects for each state's parks.

# HINT: Get a Python list of all the HTML BeautifulSoup instances that represent each park, for each state.

arkansas_soup = BeautifulSoup(arkansas_html,'html.parser')

arkansas_results = arkansas_soup.find('ul',{'id':'list_parks'})
arkansas_list_html = arkansas_results.find_all('li',{'class':'clearfix'})

arkansas_natl_sites = []
for each in arkansas_list_html:
	arkansas_natl_sites.append(NationalSite(each))

michigan_soup = BeautifulSoup(michigan_html,'html.parser')

michigan_results = michigan_soup.find('ul',{'id':'list_parks'})
michigan_list_html = michigan_results.find_all('li',{'class':'clearfix'})

michigan_natl_sites = []
for each in michigan_list_html:
	michigan_natl_sites.append(NationalSite(each))

california_soup = BeautifulSoup(california_html,'html.parser')

california_results = california_soup.find('ul',{'id':'list_parks'})
california_list_html = california_results.find_all('li',{'class':'clearfix'})

california_natl_sites = []
for each in california_list_html:
	california_natl_sites.append(NationalSite(each))

##Code to help you test these out:
# for p in california_natl_sites:
# 	print(p)
# for a in arkansas_natl_sites:
# 	print(a)
# for m in michigan_natl_sites:
# 	print(m)

######### PART 4 #########

## Remember the hints / things you learned from Project 2 about writing CSV files from lists of objects!

## Note that running this step for ALL your data make take a minute or few to run -- so it's a good idea to test any 
# methods/functions you write with just a little bit of data, so running the program will take less time!

## Also remember that IF you have None values that may occur, you might run into some problems and have to debug 
# for where you need to put in some None value / error handling!

# with open('arkansas.csv','w', newline='') as arkansas_file:
# 	writer = csv.writer(arkansas_file)
# 	arkansas_file.write('Name,Location,Type,Address,Description\n')
# 	for each in arkansas_natl_sites:
# 		writer.writerow([each.name,each.location,each.type,each.get_mailing_address(),each.description])

# with open('michigan.csv','w', newline='') as michigan_file:
# 	writer = csv.writer(michigan_file)
# 	michigan_file.write('Name,Location,Type,Address,Description\n')
# 	for each in michigan_natl_sites:
# 		writer.writerow([each.name,each.location,each.type,each.get_mailing_address(),each.description])

# with open('california.csv','w', newline='') as california_file:
# 	writer = csv.writer(california_file)
# 	california_file.write('Name,Location,Type,Address,Description\n')
# 	for each in california_natl_sites:
# 		writer.writerow([each.name,each.location,each.type,each.get_mailing_address(),each.description])
# 	for row in california_natl_sites:
# 		if not row["Type"].strip():
# 			row["Type"] = "None"
# 		writer.writerow(row)

arkansas_file = open('arkansas.csv','w')
arkansas_file.write('Name,Location,Type,Address,Description\n')

for each in arkansas_natl_sites:
	arkansas_file.write('"{}","{}","{}","{}","{}"\n'.format(each.name, each.location, each.type, each.get_mailing_address(), each.description))

arkansas_file.close()

michigan_file = open('michigan.csv','w')
michigan_file.write('Name,Location,Type,Address,Description\n')

for each in michigan_natl_sites:
	michigan_file.write('"{}","{}","{}","{}","{}"\n'.format(each.name, each.location, each.type, each.get_mailing_address(), each.description))

michigan_file.close()

california_file = open('california.csv','w')
california_file.write('Name,Location,Type,Address,Description\n')

for each in california_natl_sites:
	california_file.write('"{}","{}","{}","{}","{}"\n'.format(each.name, each.location, each.type, each.get_mailing_address(), each.description))

california_file.close()
