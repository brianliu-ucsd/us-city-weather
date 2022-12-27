# current problem:
# putting in Brian, CA 
# expect an error, saying city doesn't exist
# instead, prints weather in Los Angeles

# smaller problem:
# probably more related to website than me, doesn't seem to display high at certain 
# times of the day, or when current temp is high

import requests
from bs4 import BeautifulSoup

def main():
	exit = False

	while exit == False:
		state = get_state()
		city = get_city(state)

		url = 'https://www.wunderground.com/weather/us/' + state.lower() + '/' + city

		if check_url(url) == False:
			continue

		get_weather(url, state)

		if user_exit():
			exit = True

def get_state():
	eligible_states = ["AL","AK","AZ","AR","CA","CO","CT","DE","DC","FL","GA","HI",
	"ID","IL","IN","IA","KS","LA","ME","MD","MA","MI","MN","MS","MO","MT","NE","NV",
	"NH","NJ","NM","NY","NC","ND","OH","OK","OR","PA","RI","SC","SD","TN","TX","UT",
	"VT","VA","WA","WV","WI","WY"]

	state = input("Enter a state using its two letter code: ")

	while state.upper() not in eligible_states:
		print("Ineligible state name, try again")
		state = input("Enter a state using its two letter code: ")

	return state

def get_city(state):
	city = input("Enter a city: ")

	url = 'https://www.wunderground.com/weather/us/' + state.lower() + '/' + city

	return city

def check_url(url):
	response = requests.get(url)
	if response.status_code == 404:
	    print('Website not loading. Try again later')
	    return False

	with open('file.txt', 'w', encoding = "utf-8") as file:
			    file.write(response.text)

	with open("file.txt", encoding = "utf-8") as fp:
			    soup = BeautifulSoup(fp, 'html.parser')

	if soup.find("title").string == "Weather Underground":
		print("Hmm... something went wrong. Check the spelling of your city name!")
		return False
	
	return True	

def get_weather(url, state):
	response = requests.get(url)

	with open('file.txt', 'w', encoding = "utf-8") as file:
	    file.write(response.text)

	with open("file.txt", encoding = "utf-8") as fp:
	    soup = BeautifulSoup(fp, 'html.parser')

	span = soup.find_all('span', class_= "wu-value wu-value-to", style = "color:;")
	currentTemp = span[0].string

	title = soup.find("title").string
	city = ""

	for char in title:
		if char == ",":
			break
		city = city + char

	if currentTemp == None:
		print("Hmm... something went wrong. Check the spelling of your city name and state!")
	else: 
		print("The current temperature in " + city + ", " + state.upper() + " is " 
			+ currentTemp + "°F")

		span = soup.find_all('span', class_ = "lo")
		low = span[0].string
		print("Low for today is " + low + "F")

		span = soup.find_all('span', class_ = "hi")
		high = span[0].string
		print("High for today is " + high + "F")

def user_exit():
	exit = input("Finished? Type Y to exit or N to continue using this application: ")

	while exit.upper() != "Y" and exit.upper() != "N":
		exit = input("Invalid input! Please type Y to exit or N to continue using this application: ")

	if exit.upper() == "Y":
		return True
	else:
		return False

main()