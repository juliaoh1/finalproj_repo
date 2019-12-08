
#Julia Coxen
#SI 507
#Discussion: Tuesday 4pm
#With help from Wunmi 

## Project 3 for SI 507

import sqlite3
import pandas as pd
import sys
#import csv
#import plotly.offline as py
import plotly.graph_objects as go
import plotly.express as px
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import matplotlib.pyplot as plt

DBNAME = 'rubratings.db'
RRCSV = 'RR_combined.csv'
CITIESCSV = 'uscities.csv'


RRCSV = pd.read_csv('RR_combined.csv', sep = ',', encoding='utf-8')
#converts date column to date type
#RRCSV['date'] = RRCSV['date'].astype('datetime64[ns]')
RRCSV['date'] = pd.to_datetime(RRCSV['date'], errors='coerce')
RRCSV['date'] = RRCSV['date'].astype(str)
CITIESCSV = pd.read_csv('uscities.csv', sep = ',', encoding='utf-8')


def init_db():

    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()

# Drop tables
    statement = '''
        DROP TABLE IF EXISTS 'RR_combined';
    '''
    cur.execute(statement)
    statement = '''
        DROP TABLE IF EXISTS 'Cities';
    '''
    cur.execute(statement)

    conn.commit()


    statement = '''
        CREATE TABLE 'RR_combined' (
            'Id' INTEGER PRIMARY KEY AUTOINCREMENT,
            'pageid' TEXT,
            'date' TEXT,
            'description' TEXT,
            'location' TEXT,
            'state' TEXT ,
            'city' TEXT ,
            'phone_number' TEXT,
            'area_code' TEXT,
            'middele_three' TEXT,
            'last_four' TEXT,
            'date_scraped' TEXT, 
            'locationID' INTEGER,
            FOREIGN KEY('locationID') REFERENCES 'Cities'('Id')

        );
    '''
    cur.execute(statement)


    statement = '''
        CREATE TABLE 'Cities' (
                'Id' INTEGER PRIMARY KEY AUTOINCREMENT,
                'city' TEXT,
                'state_name' TEXT,
                'county_name' TEXT,
                'lat' TEXT,
                'lng' TEXT
        );
    '''
    cur.execute(statement)
    
    conn.commit()
    conn.close()

if len(sys.argv) > 1 and sys.argv[1] == '--init':
    print('Deleting db and starting over from scratch.')
    init_db()
else:
    print('Leaving the DB alone.')

initializing = init_db()

def insert_stuff():
    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()
#    print(RRCSV)
#    print(10* "-")
    
    
    Bars = RRCSV
    
    for index, row in Bars.iterrows():
        insertion = (index, row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10])
        statement = 'INSERT INTO "RR_combined" '
        statement += 'VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, NULL)'
        cur.execute(statement, insertion)



    start_key = 1
    cities = CITIESCSV
    foreign_key_dict = {} #k: city, v: key
    for index, row in cities.iterrows():
        insertion = (index, row[0], row[1], row[2], row[3], row[4])
        city = row[0]
        statement = 'INSERT INTO "Cities" '
        statement += 'VALUES (?, ?, ?, ?, ?, ?)'
        cur.execute(statement, insertion)
        
        foreign_key_dict[city] = start_key
        start_key +=1
        

    for city, foreign_key in foreign_key_dict.items():

        try:
            cur.execute('UPDATE RR_combined SET locationID =' + str(foreign_key) + ' WHERE city =' + '"' + city  + '"')
        except:
            pass

    conn.commit()
    conn.close()
insert_stuff()

#%%

#Function processes user commands 
def process_command(command):
    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()

#this handles a city command which gives the top/bottom 10 cities and the count of ads   
    if command.split()[0] == 'city':
        city_select= "SELECT city, COUNT(pageid) FROM RR_combined"
        city_join = " "
        city_order = 'ORDER BY COUNT(pageid)'
        city_group = 'GROUP BY city'
        city_limit= 'DESC LIMIT 10'
    
        command_split = command.split(' ')
        for item in command_split:
            if "bottom" in item:
                bottom = item.split('=')[1]
                city_limit = 'ASC LIMIT ' + bottom
            elif "top" in item:
                top= item.split('=')[1]
                city_limit = 'DESC LIMIT ' + top           
  
        statement = city_select  + city_join + city_group +" " + city_order + city_limit
        
        
        
        
#this handles a state command which gives the top/bottom 10 states and the count of ads   
    elif command.split()[0] == 'state':
        state_select= "SELECT cities.state_name, count(RR_combined.pageid) FROM RR_combined "
        state_join = " JOIN Cities ON RR_combined.locationID= cities.Id "
        state_order = 'ORDER BY count(RR_combined.pageid)'
        state_group = 'GROUP BY cities.state_name'
        state_limit= 'DESC LIMIT 10'
    
        command_split = command.split(' ')
        for item in command_split:
            if "bottom" in item:
                bottom = item.split('=')[1]
                state_limit = 'ASC LIMIT ' + bottom
            elif "top" in item:
                top= item.split('=')[1]
                state_limit = 'DESC LIMIT ' + top           
  
        statement = state_select  + state_join + state_group +" " + state_order + state_limit
 
#%%
#this handles a map command which produced a map with counts across the US
    elif command.split()[0] == 'map':
        map_select= '''SELECT RR_combined.city, count(RR_combined.pageid) as ads, lat, lng  FROM RR_combined 
                    JOIN Cities ON RR_combined.locationID= cities.Id
                    GROUP BY cities.city
                    ORDER BY count(RR_combined.pageid) DESC'''
        statement = map_select
        
        map= cur.execute(statement)
        map_list = map.fetchall()

        df = pd.DataFrame(map_list)
        df.columns = ['city', 'Ad_count', 'lat', 'lng']  

#transition to the use of plot.ly to make a map        
        df['text'] = df['city'] + '<br>Number of ads ' + (df['Ad_count'].astype(str))
        limits = [(0,10),(11,20),(21,74),(75,109),(110,150)]
        colors = ["royalblue","crimson","lightseagreen","orange","lightgrey"]
        cities = []
        scale = 5000
        
        fig = go.Figure()
        
        for i in range(len(limits)):
            lim = limits[i]
            df_sub = df[lim[0]:lim[1]]
            fig.add_trace(go.Scattergeo(
                locationmode = 'USA-states',
                lon = df_sub['lng'],
                lat = df_sub['lat'],
                text = df_sub['text'],
                marker = dict(
                    size = df_sub['Ad_count']/scale,
                    sizeref = 0.001,
                    color = colors[i],
                    line_color='rgb(40,40,40)',
                    line_width=0.5,
                    sizemode = 'area'
                ),
                name = '{0} - {1}'.format(lim[0],lim[1])))
        
        fig.update_layout(
                title_text = 'RubRating Advertisement Count by US Cities<br>(Click legend to toggle traces)',
                showlegend = True,
                geo = dict(
                    scope = 'usa',
                    landcolor = 'rgb(217, 217, 217)',
                )
            )
        
        fig.show()
#%%
#this handles a time command which produced a chart with counts over time across the US, city or state
    elif command.split()[0] == 'time':
        
        time_select= "SELECT date, count(pageid) FROM RR_combined "
        time_join = ' '
        time_where = ' '
        time_group = 'GROUP BY date'
    
        command_split = command.split(' ')

        if 'city' in command:
                city = command.rsplit('=')[1]
                time_where = "WHERE city= '" + city + "' "
        elif 'state' in command:
                state = command.rsplit('=')[1]
                time_select = "SELECT RR_combined.date, count(RR_combined.pageid) FROM RR_combined "
                time_join = 'JOIN Cities ON RR_combined.locationID= cities.Id'
                time_where = "WHERE Cities.state_name = '" + state + "' "
                time_group = 'GROUP BY RR_combined.date'
        elif 'all' in command:
                time_select = "SELECT date, count(pageid) FROM RR_combined "
                time_join = ' '
                time_where = ' '
                time_group = 'GROUP BY date'
                
        statement =  time_select + ' '  + time_join +  ' '  + time_where + ' '  + time_group
        
        time= cur.execute(statement)
        time_list = time.fetchall()

        df = pd.DataFrame(time_list)
        df.columns = ['Date', 'Ad_count']  
#transition to plot.ly to build the graph
        wide_df = pd.DataFrame(dict(Date=df['Date'], Ad_count=df['Ad_count']))
        tidy_df = wide_df.melt(id_vars='Date')
        
#        fig = px.bar(tidy_df, x='Date', y='value', color="variable", barmode="group")
        fig = px.line(tidy_df, x='Date', y='value', color="variable")
        fig.show()
#%%
#this handles the words command which produced a wordcloud from RR_combined description
    elif command.split()[0] == 'words':
        words_select = "SELECT description from RR_combined"
        words_join = ' '
        words_where = ' '
        

        if 'city' in command:
            city = command.rsplit('=')[1]
            words_where = "WHERE city = '" + city + "' "
        elif 'state' in command:
            state = command.rsplit('=')[1]
            words_select = "SELECT RR_combined.description FROM RR_combined "
            words_join = 'JOIN Cities ON RR_combined.locationID= cities.Id'
            words_where = "WHERE Cities.state_name = '" + state + "' "
        elif 'all' in command:
            words_select = "SELECT description from RR_combined"
            words_join = ' '
            words_where = ' '
        
        
        statement = words_select + ' ' + words_join + ' ' + words_where
        
        words= cur.execute(statement)
        words_list = words.fetchall()

        df = pd.DataFrame(words_list)
        df.columns = ['description'] 
#        print(df)
        # Start with one review:
        text = df.description[0]

#transition to wordcloud to build wordclouds of the advertisements    
        # Create stopword list:
        stopwords = set(STOPWORDS)
        stopwords.update(["will", "best", "Birmingham", "Address", "HWY", "Alabama", "Roots", "East"])
        
        # Generate a word cloud image
        wordcloud = WordCloud(stopwords=stopwords, background_color="white").generate(text)
        
        # Display the generated image:
        # the matplotlib way:
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis("off")
        plt.show()
        
        
        
    result= cur.execute(statement)
    result_list = result.fetchall()

    df = pd.DataFrame(result_list)
    print(df)
          
    return result_list

#process_command("words state=Texas")

#%%
## Part 3: Implement interactive prompt. We've started for you!
def load_help_text():
    with open('help.txt') as f:
        return f.read()
    
def interactive_prompt():
    help_text = load_help_text()
    response = ''
    cmds = ['city','state','map','time','words']
    second = ['city=', 'state=', 'top=', 'bottom=', 'all']
    options = tuple(second)
    while response != 'exit':
        response = input('Enter a command (or type "help"): ')

        if response == 'help':
            print(help_text)
        elif response == 'exit':
            print('bye!')
        elif response == 'map' :
            process_command(response)
        elif not response.split(' ')[0] in cmds:
            print("Command not recognized")
        elif not (response.split(' ')[1]).startswith(options):
            print("Command not recognized")
        else:
            process_command(response)

##
## Make sure nothing runs or prints out when this file is run as a module
if __name__=="__main__":
    interactive_prompt()






