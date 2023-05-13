from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import requests
import csv
import datetime

#Filter to be applied on the website
response = requests.get('https://brakts.bubbleapps.io/version-test/api/1.1/obj/states',headers={ 'Authorization': 'Bearer 9b25be9aceabd81b0dfbaaec3d3bbfee' })
qq = response.json()
qq = qq['response']
qq = qq['results']
qq = qq[0]

# Getting pages from website
chromeOptions = Options()
chromeOptions.headless = True
driver = webdriver.Chrome(executable_path="/home/hassan/chromedriver", options=chromeOptions)
url = 'https://offthechainsports.com/baseball/Events?&state='+str(qq['2D_stateID'])
driver.get(url)
pages = driver.find_elements(By.CLASS_NAME,'pagination')
pages = pages[1].text
l=[int(x) for x in pages.split() if x.isdigit()]
pages = l
pages = max(pages)

db_ID=[]
filename = 'otcc.csv'
with open(filename, 'r') as csvfile:
    datareader = csv.reader(csvfile)
    for row in datareader:
        db_ID.append(row[0])


def get_info():
    for i in range(1,pages+1):
        chromeOptions = Options()
        chromeOptions.headless = True
        driver = webdriver.Chrome(executable_path="/home/hassan/chromedriver", options=chromeOptions)
        url = 'https://offthechainsports.com/baseball/Events?page='+str(i)+'&state='+str(qq['2D_stateID'])
        driver.get(url)
        info = driver.find_elements(By.CLASS_NAME, "event-listing")
        event_name = info[0].find_elements(By.CLASS_NAME,'text-blue')
        urls = []
        event_ID = []
        division = []
        age = []
        date = []
        city = []
        state = []
        park = []
        entry_fee = []
        event_Name = []

        for j in event_name:
            urls.append(j.get_attribute('href'))
            event_Name.append(j.text)
        for l in range(len(urls)):
            event_ID.append(urls[l][54:57])
        for m in range(1, len(event_name)+1):
            s = info[0].find_elements(By.XPATH,'//*[@id="wrapper"]/div/div[1]/div[1]/div[2]/div['+str(m)+']/div[2]/div[3]/div[1]')
            s = s[0].text
            s = s.split('-')
            s = datetime.datetime.strptime(s[0],'%b %d').strftime('%m/%d')
            date.append(s)
    
        for n in range(1, len(event_name)+1):
            s = info[0].find_elements(By.XPATH,'//*[@id="wrapper"]/div/div[1]/div[1]/div[2]/div['+str(n)+']/div[2]/div[1]/div[1]')
            s = s[0].text
            s = s.split('|')
            ss = s[0].split(',')
            city.append(ss[0])
            state.append(ss[-1])
            park.append(s[1])
    
           
        for o in range(len(event_Name)):
            if event_ID[o] in db_ID:
                True
            else:
                Data = [[event_ID[o]]]
                file = open('otcc.csv','a',newline ='')
                writer = csv.writer(file)
                writer.writerows(Data)
                file.close()
                print('data stored')
                gett_info(o,urls[o],event_ID,event_Name,date,urls,city,state,park)

           
        
def gett_info(o,a,event_ID,event_Name,date,urls,city,state,park):
    age = []
    division= []
    entry_fee=[]
    chromeOptions = Options()
    chromeOptions.headless = True
    driver = webdriver.Chrome(executable_path="/home/hassan/chromedriver",options=chromeOptions)
    url = a
    driver.get(url)
    infoo = driver.find_elements(By.CLASS_NAME,'inline-block')
    button = driver.find_element(By.XPATH,'//*[@id="heading-teams"]/a')
    button.click()
    info = driver.find_elements(By.ID , 'whosComingContainer')
    ages = info[0].find_elements(By.CLASS_NAME,'col-md-2')
    fees = info[0].find_elements(By.CLASS_NAME,'col-md-1')
    teams = info[0].find_elements(By.CLASS_NAME,'col-md-7')
    for q in range(len(ages)):
        if ages[q].text == 'SHOW' or ages[q].text == '':
            True
        else:
            aaa = ages[q].text
            aaa = aaa.split('-')
            age.append(aaa[0])
            division.append(aaa[1])

    for r in range(len(fees)):
        entry_fee.append(fees[r].text[1:])

    for s in range(len(age)):
        requests.post('https://brakts.bubbleapps.io/version-test/....',headers={'Authorization': 'Bearer ....'},data = {'age':age[s],'city':city[o],'division':division[s],'entry_fee':entry_fee[s],'event_name':event_Name[o],'event_url':a,'eventID':event_ID[o],'park':park[o],'start_date':date[o],'state':state[o],'teams':teams[s].text[0:2]})                                                                                                                                                                        

get_info()

