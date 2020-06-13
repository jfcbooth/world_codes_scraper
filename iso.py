from time import sleep
import pandas as pd
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import csv

url = "https://www.iso.org/obp/ui/#search/code/"

driver = webdriver.Chrome(ChromeDriverManager().install())

driver.get(url) # open webpage in browser
sleep(10) # wait for vaadin to load (their web builder)
driver.find_element_by_xpath("//select[@class='v-select-select']/option[text()='300']").click() # change elemnts from 25 to 300 per page
sleep(10) # wait for new data to load

data = []
list_header = ['entity', 'gec', 'iso 3166', 'iso 3166 cont']
web_row = driver.find_elements_by_tag_name('td')
csv_row = []
csv_row_len = 0
in_junk = 1
for el in web_row:
    # skip over junk at beginning
    if 'A' in el.text:
        in_junk = 0
    if not in_junk:
        # if not french spelling
        if(csv_row_len != 1):
            csv_row.append(el.text)
        csv_row_len+=1
        if(csv_row_len >= 5):
            #print("csv_row_len: {}, csv_row: {}".format(csv_row_len, csv_row))
            csv_row_len = 0
            data.append(csv_row)
            csv_row = []

driver.quit()
dataFrame = pd.DataFrame(data=data, columns=list_header)
dataFrame = dataFrame.applymap(str) # convert all data to strings
dataFrame.to_csv('iso_world_codes.csv', index=False, quoting=csv.QUOTE_ALL) # write to csv explicitly including strings
