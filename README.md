# finalproj_repo


SI507 Final Project, Julia Coxen

My Github repo: https://github.com/juliaoh1/finalproj_repo.git

(final_part3.py) creates a user interaction that requires some explanation. The help.txt file has some more details, but I will summarize here. 


## Commands and options:
	“city”: Produces the cities and the number of advertisements in that city over the entire period that RR_combined covers. This command must be accompanied by “top=<number>” or “bottom=<number>”, which renders the top or bottom cities accordingly.
	“state”: Produces the states and the number of advertisements in that state over the entire period that RR_combined covers (11/20-12/8). This command must be accompanied by “top=<number>” or “bottom=<number>”, which renders the top or bottom states accordingly.
	“map”:  Produces a bubble map that shows the density of advertisements across the country 
	“time”:  Produces a line graph and accompanying data that shows the number of advertisements for a particular day.  This command must be accompanied by “all”, “city=<city>”, or “state=<full state name>”, which renders data by city or by state accordingly. 
	“words”:  Produces a wordcloud of the advertisement descriptions.  This command must be accompanied by “all”, “city=<city>”, or “state=<full state name>”, which renders data by city or by state accordingly.


As a reminder, for my project I scraped rubratings.com, which is closely linked to the problem of Human Trafficking 
and commercial sex work.  The experts I interviewed suspect that traffickers are using websites like these to connect 
with clients.  I am trying to determine if we can understand supply/demand in an area and during a requested period of time.  Scrapes ran almost daily, but as suspected the website was unreliable, but I provided at least 7 days worth of scrapes. 

## Github Repository contains the following: 

	(finalproj_part1.py) is the website scraper/crawler
	(finalproj_part2.py) combines the daily CSVs into one CSV. 
	(finalproj_part3.py) conducts all of the data handling
	(help.txt) is the help file that accompanies the user interaction
	(requirements.txt) maintains the pip freeze requirements per our instructions

	(RubRatings_Data_2019%%%%.csv) are the series of scrapes
	(RR_combined.CSV) is the combined CSV of the 7 daily scrapes
	(rubratings.db) is the generated database
	(uscities.csv) is the additional table to reference US cities, states, and lat/lng


## Some notes on my project:
	-- Scrape takes approximately 35-40 minutes to run.  
	-- Building the database takes approximately four minutes to run.
	-- I did not include caching after my conversation with Professor Klasnja. I am reading out each scrape each day to a CSV file for persistent storage.  Instead I had to add more functionality to my workflow to combine those CSVs into one CSV to read into my database.   I explained what the project requirements stated and he said that with persistent storage, no requirement for caching.
	-- If you are running (finalproj_part2) which combines the daily CSVs, you must ensure that (RR_combined.csv) and (uscities.csv) are not in the same folder.  Part2 will walk through the directory and try to combine all *.csv. 
	-- Testing will temporarily pause until the visualization windows produced from the testing are closed. 
