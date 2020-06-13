# Importing the required modules
import pandas as pd
from bs4 import BeautifulSoup
import requests
import csv

url = "https://www.cia.gov/library/publications/resources/the-world-factbook/appendix/appendix-d.html"
r = requests.get(url, allow_redirects=True) # download html files into variable of binary type
open('cia_world_codes.html', 'wb').write(r.content) # write the variable to a file


path = 'cia_world_codes.html' # open the file to extract info

# empty list
data = []

# for getting the header from
# the HTML file
list_header = []
soup = BeautifulSoup(open(path), 'html.parser') # magic of python, this library does most of the parsing
header = soup.find_all("table")[0].find("tr") # finds the table within the html file

# extra headers I have to add in manually since they aren't marked and mess up the csv
gec2 = 0
iso_cont = 0
for items in header: # goes through all headers in the table and puts them into a list
    try:
        list_header.append(items.get_text())
        if(items.get_text() == 'gec' and gec2 == 0):
            list_header.append('gec cont')
            gec2 = 1
        if(items.get_text() == 'iso 3166' and gec2 == 1):
            list_header.append('iso 3166 cont')
            iso_cont = 1
    except:
        continue

# for getting the data
HTML_data = soup.find_all("table")[0].find_all("tr")[1:] # now that we know the headers, we can find the data

for element in HTML_data:
    sub_data = []
    for sub_element in element:
        try:
            text = sub_element.get_text().strip() # .strip removes whitespace
            if(text) == '-': # replace - with nothing
                text = ''
            sub_data.append(text)
        except:
            continue
    data.append(sub_data)

# Storing the data into Pandas
# DataFrame
dataFrame = pd.DataFrame(data=data, columns=list_header)
dataFrame = dataFrame.applymap(str) # convert all data to strings
#print(dataFrame)
# Converting Pandas DataFrame
# into CSV file
dataFrame.to_csv('cia_world_codes.csv', index=False, quoting=csv.QUOTE_ALL) # write to csv explicitly including strings
