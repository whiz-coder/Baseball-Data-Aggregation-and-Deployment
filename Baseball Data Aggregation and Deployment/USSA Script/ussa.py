import requests
import csv
import json
import re
import datetime

#we getting filters from our api's to be applied on website

#states
response = requests.get('https://brakts.bubbleapps.io/version-test/api/1.1/obj/states',headers={ 'Authorization': 'Bearer 9b25be9aceabd81b0dfbaaec3d3bbfee' })
qq = response.json()
qq = qq['response']
qq = qq['results']
qq = qq[0] 

#season
response1 = requests.get('https://brakts.bubbleapps.io/version-test/api/1.1/obj/season',headers={ 'Authorization': 'Bearer 9b25be9aceabd81b0dfbaaec3d3bbfee' })
qqq = response1.json()
qqq = qqq['response']
qqq = qqq['results']
qqq = qqq[0] 
db_ID = []

filename = 'usssa.csv'
with open(filename, 'r') as csvfile:
    datareader = csv.reader(csvfile)
    for row in datareader:
        db_ID.append(row[0])



#This function will get ID & state from our events
def main_func():
    url = "https://usssa.com/api/?action=eventSearchSimpleV11"
    payload='sportID=11&seasonID='+str(qqq['USSSA_seasonID'])+'&age=null&classID=null&stateID=null&regionID='+str(qq['USSSA_regionID'])+'&zip=null&mile=null&statureID=null&startDate=null&endDate=null&director=null&parkID=null'
    headers = {
      'authority': 'usssa.com',
      'accept': 'application/json, text/plain, */*',
      'accept-language': 'en-US,en;q=0.9',
      'content-type': 'application/x-www-form-urlencoded',
      'cookie': '_gid=GA1.2.625944477.1666361295; _gat_gtag_UA_97468231_8=1; _ga_T9JN9TMQ0X=GS1.1.1666361296.1.1.1666367052.0.0.0; _ga=GA1.1.83726782.1666361295',
      'origin': 'https://usssa.com',
      'referer': 'https://usssa.com/baseball/eventSearch/?sportID=11&seasonID='+str(qqq['USSSA_seasonID'])+'&region='+str(qq['USSSA_regionID']),
      'sec-ch-ua': '"Chromium";v="106", "Google Chrome";v="106", "Not;A=Brand";v="99"',
      'sec-ch-ua-mobile': '?1',
      'sec-ch-ua-platform': '"Android"',
      'sec-fetch-dest': 'empty',
      'sec-fetch-mode': 'cors',
      'sec-fetch-site': 'same-origin',
      'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Mobile Safari/537.36'
    }
    r = requests.request("POST", url, headers=headers, data=payload)
    playerdata = r.json()
    aa = playerdata.get('results')
    for i in aa:
        f = str(i['ID'])
        ss = str(i['state'])
        if f not in db_ID:
            Data = [[f]]
            file = open('usssa.csv','a',newline ='')
            writer = csv.writer(file)
            writer.writerows(Data)
            file.close()
            store_data(f,ss)
        
# This function will go to that events by using eventID and get info and store information        
def store_data(ID,state):
    url = "https://usssa.com/api/?action=selpV2"
    payload='eventID='+str(ID)+'&divisionID=null&tabName=home'
    headers = {
      'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:106.0) Gecko/20100101 Firefox/106.0',
      'Accept': 'application/json, text/plain, */*',
      'Accept-Language': 'en-US,en;q=0.5',
      'Accept-Encoding': 'gzip, deflate, br',
      'Content-Type': 'application/x-www-form-urlencoded',
      'Origin': 'https://usssa.com',
      'Connection': 'keep-alive',
      'Referer': 'https://usssa.com/baseball/event_home/?eventID='+str(ID),
      'Cookie': '_ga_T9JN9TMQ0X=GS1.1.1666729133.3.1.1666729634.0.0.0; _ga=GA1.1.128555122.1666364721; _pbjs_userid_consent_data=3524755945110770; _pubcid=d5572926-a1e4-428f-98bc-4b2b58320f29; __gads=ID=57d6955d1a3ec9c4-22c839b75ad600ab:T=1666364757:S=ALNI_MY05eyUmp2fk1Cu7GG7PvxZYDRM2g; __gpi=UID=00000b14e02f278b:T=1666364757:RT=1666729155:S=ALNI_Mac36xLrGkHZv5ZrEqZdY9DGI19Nw; _cc_id=f528687f0a0d3b72252293ce1a7eeefb; panoramaId_expiry=1666969560995; panoramaId=b1ad1cb2896182f266e906dc695316d53938a3cc3fb62b46b6eb9a8b10c22362; cto_bundle=CPEJ8184b21jVHJQNXVyRUUlMkZKUnRmUkQ2dm9HRjkyRFBvT053YWNtVjFSJTJGd2N6JTJCTWtQT2JvaTI0YWtYTmRPeDY3NXMxMFdtWHBxUTh5VDFGbFJBckdodSUyRjZCdGdJdVJrNWNKTGVvd1pxJTJCQzNNRTlCOEJqcFRMRUdEeXBReXglMkZDSGViNFNNVE5zUmM2aXBObzlsZUxZWklieEpmZ21EYzBpT1loajdjb3dDNW5Uc1ElM0Q; _gid=GA1.2.594487774.1666729139; aasd=3%7C1666729141281; __aaxsc=2',
      'Sec-Fetch-Dest': 'empty',
      'Sec-Fetch-Mode': 'cors',
      'Sec-Fetch-Site': 'same-origin',
      'TE': 'trailers'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    a = response.text
    d = json.loads(a)
    f = d.get('home')
    c = f.get('eventDivisions')
    i = 1
    for i in c:
        my_list = list(filter(None, re.split(r'(\d+)', i['class'])))
        Age = my_list[0]
        Division = my_list[1]
        date = i['startDate']
        date = date[:10]
        date = date.replace('-','/')
        date = datetime.datetime.strptime(date, '%Y/%m/%d').strftime('%m/%d/%Y')
        requests.post('https://brakts.bubbleapps.io/version-test/....',headers={ 'Authorization': 'Bearer  ......' },data={'age':Age,'city': i['city'],'director':i['director'],'division':Division,'entry_fee':i['entryFee'],'event_name':i['name'],'event_url':headers['Referer'],'eventID':ID,'start_date':date,'state':state,'stature':i['stature'],'teams':i["teamEntered"]})
        
        
        
        
        
main_func()
    
