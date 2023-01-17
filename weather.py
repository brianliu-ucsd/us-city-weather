import requests
from bs4 import BeautifulSoup

def main():
	exit = False

	while exit == False:
		state = get_state()
		city = get_city(state)

		url = 'https://www.wunderground.com/weather/us/' + state.lower() + \
		'/' + city

		# If URL is bad, return to start of loop and reprompt user
		if check_url(url, city) == False:
			continue

		get_weather(url, state)

		# Gives user option to exit program at end of each cycle
		if user_exit():
			exit = True

def get_state():
	eligible_states = ["AL","AK","AZ","AR","CA","CO","CT","DE","DC","FL","GA",
	"HI","ID","IL","IN","IA","KS","LA","ME","MD","MA","MI","MN","MS","MO","MT",
	"NE","NV","NH","NJ","NM","NY","NC","ND","OH","OK","OR","PA","RI","SC","SD",
	"TN","TX","UT","VT","VA","WA","WV","WI","WY"]

	state = input("Enter a state using its two letter code: ").strip()

	while state.upper() not in eligible_states:
		print("Ineligible state name, try again")
		state = input("Enter a state using its two letter code: ").strip()

	return state

def get_city(state):
	city = input("Enter a city: ").strip()

	return city

def check_url(url, city):
	# Storing html info from url
	response = requests.get(url)

	# Error if website does not load correctly
	if response.status_code == 404:
	    print('Website not loading. Try again later')
	    return False

	# Print raw website html onto file.txt
	with open('file.txt', 'w', encoding = "utf-8") as file:
			    file.write(response.text)

	# Use BeautifulSoup to parse html from file.txt
	with open("file.txt", encoding = "utf-8") as fp:
			    soup = BeautifulSoup(fp, 'html.parser')

	# When city not found, Wunderground directs to a site titled
	# "Weather Underground"
	if soup.find("title").string == "Weather Underground":
		print("Hmm... something went wrong. Check the spelling of your city" +
			" name!")
		return False

	# Comparing city name inputted and city name loaded by website
	for char in city:
		if char == " ":
			city.replace(" ","")

	actual_city = ""
	for char in soup.find("title").string:
		if char == ",":
			break
		actual_city = actual_city + char

	true_actual_city = actual_city

	for char in actual_city:
		if char == " ":
			actual_city.replace(" ","")

	# If inputted city and loaded city are different, and "Weather
	# Underground" site was not loaded, ask if user meant the loaded
	# city. This also accounts for slight spelling errors.
	if city.lower() == actual_city.lower():
		pass
	else:
		print("Did you mean " + true_actual_city + "?")
		print("Showing results for " + true_actual_city)

	return True	

def get_weather(url, state):
	# Storing html info from url
	response = requests.get(url)

	# Error if website does not load correctly
	if response.status_code == 404:
	    print('Website not loading. Try again later')
	    return

	# Print raw website html onto file.txt
	with open('file.txt', 'w', encoding = "utf-8") as file:
	    file.write(response.text)

	# Use BeautifulSoup to parse html from file.txt
	with open("file.txt", encoding = "utf-8") as fp:
	    soup = BeautifulSoup(fp, 'html.parser')

	# Accessing specific part of html where current temperature is
	span = soup.find_all('span', class_= "wu-value wu-value-to",
		style = "color:;")
	currentTemp = span[0].string

	# Build city name from website data, rather than user input.
	# Prevents user spelling or capitalization errors in output
	city = ""
	for char in soup.find("title").string:
		if char == ",":
			break
		city = city + char

	# Print out current temperature, low, and high if it exists
	if currentTemp == None:
		print("Hmm... something went wrong. Check the spelling of your city" +
			" name and state!")
		return
	else: 
		print("The current temperature in " + city + ", " + state.upper()
			+ " is " + currentTemp + "°F")

		span = soup.find_all('span', class_ = "lo")
		low = span[0].string
		print("Low for today is " + low + "F")

		span = soup.find_all('span', class_ = "hi")
		high = span[0].string
		print("High for today is " + high + "F")

def user_exit():
	exit = input("Finished? Type Y to exit or N to continue using this" +
	" application: ")

	while exit.upper() != "Y" and exit.upper() != "N":
		exit = input("Invalid input! Please type Y to exit or N to continue" +
		" using this application: ")

	if exit.upper() == "Y":
		return True
	else:
		return False

main()
