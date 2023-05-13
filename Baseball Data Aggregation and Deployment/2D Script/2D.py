from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import requests
import csv
chromeOptions = Options()
chromeOptions.headless = True
driver = webdriver.Chrome(executable_path="/home/hassan/chromedriver", options=chromeOptions)
url = 'https://youth.2dsports.org/?page=1&month=&name=&event_label_id=&state=&venue_id='
driver.get(url)
info = driver.find_elements(By.CLASS_NAME, "list-wrapper")
pages = info[0].find_elements(By.XPATH, "/html/body/div/section/div[2]/div[6]/ul")
pages = pages[0].text
l=[int(x) for x in pages.split() if x.isdigit()]
pages = l
pages = max(pages)
db_ID= []
filename = '2d.csv'
with open(filename, 'r') as csvfile:
    datareader = csv.reader(csvfile)
    for row in datareader:
        db_ID.append(row[0])
#----------------------------------------------------------------------
def get_info():
    event_name = info[0].find_elements(By.CLASS_NAME, 'list-title')
    urls = info[0].find_elements(By.LINK_TEXT, "DETAILS")
    value = len(event_name[0].text)
    i = 1
    for i in range(1,value+1):
        chromeOptions = Options()
        chromeOptions.headless = True
        driver = webdriver.Chrome(executable_path="/home/hassan/chromedriver", options=chromeOptions)
        t = urls[i].get_attribute('href')
        driver.get(t)
        infoo = driver.find_elements(By.CLASS_NAME, "team-details")
        result = infoo[0].text
        result = result.replace("\n",", ")
        result = result.replace("  "," ")
        
        #city - state
        city = info[0].find_elements(By.CLASS_NAME, 'list-city')
        city = city[i].text
        state = city[-2:]
        city = city[0:-4]
        
        #Start Date - And - Event Date
        start_dd = info[0].find_elements(By.CLASS_NAME, 'list-date')
        start_dd = start_dd[i].text
        start_dd_yy =  start_dd[9:18]
        start_dd = start_dd[0:5]
        
        #eventID 
        #Format [event name with dashes replacing spaces]-[city]-[state]-[start date mm]-[start date dd]-[start date yyyy]
        event_name = info[0].find_elements(By.CLASS_NAME, 'list-title')
        event_ID = info[0].find_elements(By.CLASS_NAME,'list-container')
        event_ID = event_ID[i].get_attribute('data-event-id')
        
        
        
        event_label = info[0].find_elements(By.CLASS_NAME, 'event_details_label')
        teams = info[0].find_elements(By.CLASS_NAME, 'team-details')
        teams = teams[i].text
        if len(teams) == 0:
            teams = 0
        else:
            teams = [int(i) for i in teams.split() if i.isdigit()]
            teams = teams[0]
        
        #writing data into csv
        
        if event_ID not in db_ID:
            Data = [[event_ID]]
            file = open('2d.csv','a',newline ='')
            writer = csv.writer(file)
            writer.writerows(Data)
            file.close()  
            requests.post('https://brakts.bubbleapps.io/....',headers={ 'Authorization': 'Bearer .....' },data={'city':city,'event_date':start_dd_yy,'event_label':event_label[i].text,'event_name':event_name[i].text,'event_url':urls[i].get_attribute('href'),'eventID':event_ID,'price':result,'start_date':start_dd,'state':state,'teams':teams})                                                                                                                                               

for i in range(1,pages+1):
    chromeOptions = Options()
    chromeOptions.headless = True
    driver = webdriver.Chrome(executable_path="/home/hassan/chromedriver", options=chromeOptions)
    url = 'https://youth.2dsports.org/?page='+str(i)+'&month=&name=&event_label_id=&state=&venue_id='
    driver.get(url)
    info = driver.find_elements(By.CLASS_NAME, "list-wrapper")
    get_info()
    
    

    

    
    

        

