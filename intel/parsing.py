import requests 
import time 
import datetime
import random
import urllib.request
import os
from pyvirtualdisplay import Display
from pymongo import MongoClient
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.options import Options as ChromeOptions

class Intel:
    def __init__(self, db, login_url, username, password, chrome_path, chromedriver_path):
        self.username = username
        self.password = password
        self.db = db
        self.count = 0
        self.endtable = ''      
        self.sign = login_url
        chrome_options = ChromeOptions()  
        chrome_options.add_argument("--headless")  
        chrome_options.binary_location = chrome_path
        print(chrome_path)
        print(chromedriver_path)
        self.driver = webdriver.Chrome(executable_path=chromedriver_path,   chrome_options=chrome_options )  

    def sign_in(self):
        self.driver.get(self.sign)
        WebDriverWait(self.driver, 25).until(
            EC.presence_of_element_located((By.ID, "identifierId"))
        )
        time.sleep(3)
        username = self.driver.find_element_by_id("identifierId")
        username.send_keys(self.username)
        self.driver.find_element_by_id("identifierNext").click()
        time.sleep(5)
        WebDriverWait(self.driver, 29).until(
            EC.presence_of_element_located((By.ID, "password"))
        )
        time.sleep(3)
        password = self.driver.find_element_by_name("password")
        password.send_keys(self.password)
        self.driver.find_element_by_id("passwordNext").click()
        time.sleep(2)
        WebDriverWait(self.driver, 28).until(
            EC.presence_of_element_located((By.ID, "plexts"))
        )

    def find_port(self, name, lat, lng, portals, player):
        cursor = portals.find({ "name": name, "lat": lat, 'lng': lng })    
        ind = ""    
        f = True
        for doc in cursor:
            f = False
            ind = doc["_id"]
        if f:
            portals.insert({ "name": name, "level":"", "owner": player, "lat": lat, 'lng': lng , "mod": ""})
            cursor = portals.find({ "name": name, "lat": lat, 'lng': lng })    
            for port in cursor:
                ind = port["_id"]        
        return ind
    
    def get_portal_db(self, flag):
        portals = self.db.portals.find({"mod": flag})
        for port in portals:
            self.get_data_portal(port['_id'], port['lat'], port['lng'])
    
    def find_player(self, player, players, time, portal, flag):
        pl = players.find({ 'nameing': player})
        f = True        
        for doc in pl:
            f = False
            if flag:
                players.update({ 'nameing': player }, 
                { 'nameing': player, 'time': time, 'portal': portal, 'fraction': doc['fraction'] } )
        if f:    
            players.insert( { 'nameing': player, 'time': time, 'portal': portal, 'fraction': "E"} )
            
    def get_result(self):        
        time.sleep(2)
        soup = BeautifulSoup(self.driver.page_source, "html.parser")  
        time.sleep(3) 
        table = soup.findAll('div', { 'class', 'plext' })
        last = table[-20:]   
        self.get_portal_db('X') 
        if last != self.endtable:
            self.count = 0     
            portals = self.db['portals']
            players = self.db['players']
            mods = self.db['portals.mods']
            resrs = self.db['portals.resonators']   
            name_port = ''                       
            for obj in last:
                try:
                    if 'created a Control Field' in obj.text:
                        st = 'field'     
                    else:    
                        log_time = obj.find('div', class_='pl_timestamp_date').text                      
                        span = obj.findAll('span')   
                        #1 portal       
                        player = span[0].text #player
                        if name_port == '':
                            name_port = span[1].text
                        name = span[1].text #portal name    
                        if name != name_port:     
                            name_port = name      
                            lat = span[1]["data-plat"]
                            lng = span[1]["data-plng"]  
                            self.find_player(player, players, log_time, name, True)
                            ind = self.find_port(name, lat, lng, portals, player)    
                            self.get_data_portal(ind, lat, lng)
                            print(name +"="+log_time+"="+player)
                        if 'linked' in obj.text: #2 portals
                            name2 = span[3].text #portal name
                            lat2 = span[3]["data-plat"]
                            lng2 = span[3]["data-plng"]     
                            ind2 = self.find_port(name2, lat2, lng2, portals, player)
                            self.get_data_portal( ind2, lat2, lng2)                
                except KeyError:
                    print("message comm")
                except TimeoutError:
                    print("timeout:\n"+ obj)    
            self.driver.get(self.sign)            
            self.endtable = last   
        else:
            self.count = self.count + 1    

    def get_data_portal(self, ind, lat, lng):        
        res_data = []
        mod_data = []
        url = "https://www.ingress.com/intel?pll={},{}&z=11&pll={},{}".format(lat,lng,lat,lng)
        try:
            self.driver.get(url)
            time.sleep(2)
            try:
                WebDriverWait(self.driver, 60).until(
                    EC.presence_of_element_located((By.ID, "portal_details_container"))
                )
            except TimeoutError:
                print("timeout error exception")   
            portals = self.db['portals']
            players = self.db['players']
            mods = self.db['portals.mods']
            resrs = self.db['portals.resonators']   

            soup = BeautifulSoup(self.driver.page_source, "html.parser")   
            time.sleep(5)       
            table = soup.find('div', { 'class', 'portal_details_container_captured' })
            title = table.find('div', {'id': 'portal_primary_title'}).text
            level = table.find('div', {'id': 'portal_level'}).text
            owner = table.find('div', id='portal_capture_details').find('span').text
            while owner == 'loading...':
                soup = BeautifulSoup(self.driver.page_source, "html.parser")   
                time.sleep(10)       
                table = soup.find('div', { 'class', 'portal_details_container_captured' })
                title = table.find('div', {'id': 'portal_primary_title'}).text
                level = table.find('div', {'id': 'portal_level'}).text
                owner = table.find('div', id='portal_capture_details').find('span').text
                print("loading owner ..." )

            print(title + "=" + level  + "=" + owner)

            resonators = table.find('div', id='tab_content_res')
            modss = table.find('div', id='tab_content_mod')
            res_left = resonators.find('div', id='resonators_left')
            res_right = resonators.find('div', id='resonators_right')

            for resL in res_left:                
                if resL.find('span') != None:
                    r1 = resL.find('span').text
                else:
                    r1 = ''
                if resL.find('div', class_='resonator_level') != None:
                    u1 = resL.find('div', class_='resonator_level').text
                else:
                    u1 = ''
                res_data.append( { 'owner': r1, 'level': u1 })

            for resR in res_right:
                if resR.find('span') != None:
                    r2 = resR.find('span').text
                else:
                    r2 = ''
                if resR.find('div', class_='resonator_level') != None:
                    u2 = resR.find('div', class_='resonator_level').text
                else:
                    u2 = ''
                res_data.append( { 'owner': r2, 'level': u2 })
            
            very_rare = ''
            for mod in modss.find_all('div', class_='mod'):
                mown = ''
                mname = ''

                if mod.find('span') != None:
                    mown = mod.find('span').text

                if mod.find('div', class_="mod_name_common") != None:
                    mname = mod.find('div', class_="mod_name_common").text

                if mod.find('div', class_="mod_name_rare") != None:    
                    mname = 'rare ' + mod.find('div', class_="mod_name_rare").text
                    
                if mod.find('div', class_="mod_name_very_rare") != None:    
                    mname = 'very rare ' + mod.find('div', class_="mod_name_very_rare").text
                    if 'Heat' in mname or 'Multi' in mname or 'Transmuter' in mname:
                        very_rare = 'X' 

                if mod.find('div', class_="mod_icon_empty") != None:    
                    mname = mod.find('div', class_="mod_icon_empty").text
                       
                mod_data.append( { 'owner' : mown, 'name': mname })
            
            self.find_player(owner, players, '', title, False)
            portal = portals.find({ "_id": ind })
            mod = mods.find({ "_id": ind })
            res = resrs.find({ "_id": ind })
            plr = players.find({"nameing": owner})
            for port in portal:
                for p in plr:
                    if very_rare == 'X':
                        port['mod'] = 'X'
                    portals.update({"_id": port['_id']}, 
                    {"_id": port['_id'], "level": p['fraction'] + level[6:], "owner": owner, "name": port['name'], "lat": port['lat'], 'lng':port['lng'], 'mod': port['mod'] })
                f = True   
                if mod != None:         
                    for mds in mod:
                        f = False
                        mods.update({"_id": ind}, 
                        {"_id": ind, 
                        "mod1": mod_data[0]['name'], "own1": mod_data[0]['owner'],
                        "mod2": mod_data[1]['name'], "own2": mod_data[1]['owner'],
                        "mod3": mod_data[2]['name'], "own3": mod_data[2]['owner'],
                        "mod4": mod_data[3]['name'], "own4": mod_data[3]['owner']} )
                if f:
                    mods.insert(
                    {"_id": ind, 
                    "mod1": mod_data[0]['name'], "own1": mod_data[0]['owner'],
                    "mod2": mod_data[1]['name'], "own2": mod_data[1]['owner'],
                    "mod3": mod_data[2]['name'], "own3": mod_data[2]['owner'],
                    "mod4": mod_data[3]['name'], "own4": mod_data[3]['owner']} )
                f = True    
                if res != None:
                    for rs in res:
                        f = False
                        resrs.update({"_id": ind}, 
                        {"_id": ind, 
                        "res1": res_data[0]['level'], "own1": res_data[0]['owner'],
                        "res2": res_data[1]['level'], "own2": res_data[1]['owner'],
                        "res3": res_data[2]['level'], "own3": res_data[2]['owner'],
                        "res4": res_data[3]['level'], "own4": res_data[3]['owner'],
                        "res5": res_data[4]['level'], "own5": res_data[4]['owner'],
                        "res6": res_data[5]['level'], "own6": res_data[5]['owner'],
                        "res7": res_data[6]['level'], "own7": res_data[6]['owner'],
                        "res8": res_data[7]['level'], "own8": res_data[7]['owner']} )
                if f:
                    resrs.insert(
                    {"_id": ind, 
                    "res1": res_data[0]['level'], "own1": res_data[0]['owner'],
                    "res2": res_data[1]['level'], "own2": res_data[1]['owner'],
                    "res3": res_data[2]['level'], "own3": res_data[2]['owner'],
                    "res4": res_data[3]['level'], "own4": res_data[3]['owner'],
                    "res5": res_data[4]['level'], "own5": res_data[4]['owner'],
                    "res6": res_data[5]['level'], "own6": res_data[5]['owner'],
                    "res7": res_data[6]['level'], "own7": res_data[6]['owner'],
                    "res8": res_data[7]['level'], "own8": res_data[7]['owner']} )
        
        except AttributeError:
            portals = self.db['portals']
            portal = portals.find({ "_id": ind })
            mod = mods.find({ "_id": ind })
            res = resrs.find({ "_id": ind })
            f = True
            for port in portal:
                portals.update({"_id": port['_id']}, 
                {"_id": port['_id'], "level": '0', "name": port['name'],"owner": '', "lat": port['lat'], 'lng':port['lng'], 'mod': port['mod'] })
                for mds in mod:
                    f =  False    
                    mods.update({"_id": ind}, 
                    {"_id": ind, 
                    "mod1": '', "own1": '',
                    "mod2": '', "own2": '',
                    "mod3": '', "own3": '',
                    "mod4": '', "own4": ''} )
                for rs in res:
                    f =  False    
                    resrs.update({"_id": ind}, 
                    {"_id": ind, 
                    "res1": '', "own1": '',
                    "res2": '', "own2": '',
                    "res3": '', "own3": '',
                    "res4": '', "own4": '',
                    "res5": '', "own5": '',
                    "res6": '', "own6": '',
                    "res7": '', "own7": '',
                    "res8": '', "own8": ''} )
            if f: 
                mods.insert({"_id": ind, 
                "mod1": '', "own1": '',
                "mod2": '', "own2": '',
                "mod3": '', "own3": '',
                "mod4": '', "own4": ''} )
                resrs.insert({"_id": ind, 
                "res1": '', "own1": '',
                "res2": '', "own2": '',
                "res3": '', "own3": '',
                "res4": '', "own4": '',
                "res5": '', "own5": '',
                "res6": '', "own6": '',
                "res7": '', "own7": '',
                "res8": '', "own8": ''} )
        except TimeoutError:
            print(ind + "=" + lat + "-"+lng)

def main():   
    URL_INTEL = "https://www.google.com/accounts/ServiceLogin?service=ah&passive=true&continue=https://appengine.google.com/_ah/conflogin%3Fcontinue%3Dhttps://www.ingress.com/intel%253Fll%253D52.436235,30.998523%2526z%253D11"
    USERNAME = os.environ['USERNAME']
    PASSWORD = os.environ['PASSWORD']
    MONGO_URI = os.environ['MONGO_URI']    
    CHROME_PATH = os.environ['CHROME_PATH'] 
    CHROMEDRIVER_PATH = os.environ['CHROME_PATH'] 
    os.environ["webdriver.chrome.driver"] = CHROME_PATH
    client = MongoClient(MONGO_URI)
    db = client.ingressdb 
    intel = Intel(db, URL_INTEL, USERNAME, PASSWORD, CHROME_PATH, CHROMEDRIVER_PATH)
    intel.sign_in() 
    time.sleep(5)
    while True:        
        intel.get_result()     
        time.sleep(10)
        if intel.count > 3:
            intel.compare_portal(db)
            time.sleep(800)    
 
if __name__ == '__main__':  
    main()