from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import requests
import csv

#Filter to be applied on the website
response = requests.get('https://brakts.bubbleapps.io/version-test/api/1.1/obj/states',headers={ 'Authorization': 'Bearer 9b25be9aceabd81b0dfbaaec3d3bbfee' })
qq = response.json()
qq = qq['response']
qq = qq['results']
qq = qq[0]
db_ID=[]

filename = 'gsm.csv'#Get the data
with open(filename, 'r') as csvfile:
    datareader = csv.reader(csvfile)
    for row in datareader:
        db_ID.append(row[0])
        
def get_info():
    eventID = []
    eventName = []
    Date = []
    urls=[]
    chromeOptions = Options()
    chromeOptions.headless = True
    driver = webdriver.Chrome(executable_path="/home/hassan/chromedriver", options=chromeOptions)
    url = ('https://www.grandslamtournaments.com/baseball/Events?state='+str(qq['GS_stateID']))
    driver.get(url)
    info = driver.find_elements(By.XPATH, "/html/body/div/div[3]")
    event_id = info[0].find_elements(By.CLASS_NAME,'media')
    event_name = info[0].find_elements(By.CLASS_NAME,'h3')
    dates = info[0].find_elements(By.CLASS_NAME,'h4')


    for a in range(len(event_id)):
        eventID.append(event_id[a].get_attribute('data-eventid'))
        eventName.append(event_name[a].text)
        ddd = dates[a].text[0:5]
        Date.append(ddd)
        
    for b in range(1,len(event_id)+1):
        url = info[0].find_element(By.XPATH,'/html/body/div/div[3]/div['+str(b)+']/div[3]/div/div[2]/a[1]')
        urls.append(url.get_attribute('href'))
    for o in range(len(eventID)):
        print('in event id')
        if eventID[o] in db_ID:
            True
        else:
            Data = [[eventID[o]]]
            file = open('gsm.csv','a',newline ='')
            writer = csv.writer(file)
            writer.writerows(Data)
            file.close() 
            print('data stored')
            update_info(o,urls[o],eventID,eventName,Date,urls)        
def update_info(o,a,eventID,eventName,Date,urls):
    age = []
    fee = []
    chromeOptions = Options()
    chromeOptions.headless = True
    driver = webdriver.Chrome(executable_path="/home/hassan/chromedriver", options=chromeOptions)
    url = (a+str('#teams'))
    driver.get(url)
    info = driver.find_elements(By.CLASS_NAME,'tab-content')
    results = info[0].find_elements(By.CLASS_NAME,'col-xs-3')
    park = info[0].find_element(By.XPATH,'/html/body/div[1]/div/div[1]/div[2]/h3[2]')
    cs = info[0].find_element(By.XPATH,'/html/body/div[1]/div/div[1]/div[2]/h3[1]')
    teams = info[0].find_elements(By.CLASS_NAME,'col-xs-6')
    park = park.text[2:]
    cs = cs.text
    cs = cs.split(',')
    city = cs[0]
    state = cs[1]
    for c in range(0,len(results),2):
        age.append(results[c].text)
    for d in range(1,len(results),2):
        if results[d].text == '':
            fee.append(0)
        else:
            fee.append(results[d].text[1:])

    for e in range(len(age)):
        requests.post('https://brakts.bubbleapps.io/version-test/....',headers={'Authorization': 'Bearer ....'},data = {'city':city,'division':age[e],'entry_fee':fee[e],'event_name':eventName[o],'event_url':urls[o],'eventID':eventID[o],'park':park,'start_date':Date[o],'state':state,'teams':teams[e].text[0:2]}) 

    
get_info()
