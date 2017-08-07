# To automate the setup a Ikev2 VPN Tunnel on Android devices

from appium import webdriver
from time import sleep
import requests
import json
from collections import namedtuple
import time,sys
import progressbar
#from utils import loadJson, formatRelPath 

bar = progressbar.ProgressBar(maxval=100, widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])


#1 . ################################ get VPN Server Ip from Json  #################################
def getServerIp(json_data):
    print "json_data :",json_data
    url = "https://vpnbridgeirlstg.mcafee.com/api/v1/partners/samsung/users/sessions"

    headers =   {
            'content-type': "application/json",
            'cache-control': "no-cache",
            'postman-token': "cc0a11f0-09dd-6407-b0cc-0a039cf85d0d"
         }
    response = requests.request("POST", url,json=json_data, headers=headers)
    #print "Response :",response
    server_ip =  response.text
    #print "server_ip :",server_ip
    return server_ip



#2 . ################################ Setup Appium #################################
def setupAppium( ):
    print "Setting up Appium, and capabilities"
    desired_caps = {}
    desired_caps['platformName'] = 'Android'
    desired_caps['platformVersion'] = '6.0.1'
    desired_caps['deviceName'] = 'Android Emulator'
    desired_caps['app'] ='com.android.settings'
    desired_caps['appPackage'] = 'com.android.settings'
    desired_caps['appActivity'] = '.Settings'
    driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
    return driver





#3 . ################################ Add and save a VPN Tunnel on device #################################
def setupVPN(driver,vpncfg,server_ip):
   #print  vpncfg['service_id']
   more_connection = driver.find_element_by_android_uiautomator('new UiSelector().text("More connection settings")')
   more_connection.click()
   driver.find_element_by_android_uiautomator('new UiSelector().text("VPN")').click()
   driver.find_element_by_id("com.android.settings:id/vpn_create").click()
   driver.find_element_by_id("com.android.settings:id/name").set_text(vpncfg['service_id'])
   #select Type from Spinner
   driver.find_element_by_id("com.android.settings:id/type_with_strongswan").click()
   driver.find_element_by_android_uiautomator('new UiSelector().textContains("IPSec IKEv2 PSK")').click()
   driver.hide_keyboard(key_name='Done')
   driver.page_source
    #select Server Address text field 
   driver.find_element_by_id("com.android.settings:id/server").set_text(server_ip)
   driver.hide_keyboard(key_name='Done')
   driver.page_source
   #select IPSec Identifier text field 
   driver.find_element_by_id("com.android.settings:id/ipsec_identifier").set_text(vpncfg['vpn_id'])
   driver.hide_keyboard(key_name='Done')
   driver.page_source
   #select IPSec psk text field 
   driver.find_element_by_id("com.android.settings:id/ipsec_secret").set_text(vpncfg['psk'])
   driver.hide_keyboard(key_name='Done')
   driver.page_source
    #Save the entered credentials
   driver.find_element_by_id("android:id/button1").click()
   driver.page_source

    #Connect to the saved VPN Tunnel 


#4. ################################ Connect to the saved VPN Tunnel #################################
def connectVPN( driver ,vpnname):
    driver.find_element_by_android_uiautomator('new UiSelector().text("'+vpnname+'")').click()
    driver.page_source
    driver.find_element_by_id("android:id/button1").click()
   

    #run top100 url script 




#5 . ################################ Open Termux and run top100 url script #################################
def runScript( driver ,urlsjson,testname):
    driver.start_activity('com.termux', '.app.TermuxActivity')
    terminal=driver.find_element_by_android_uiautomator('new UiSelector().resourceId("com.termux:id/terminal_view")')
    terminal.set_text("cd nodedroid" + "\n")
    terminal.set_text("git pull" + "\n")
    terminal.set_text("node index.js -w="+urlsjson + " -n="+testname+"\n")
    sleep(30)
    driver.start_activity('com.android.settings', '.Settings')


    
if __name__ == '__main__':
    bar.start()
    bv = 20;
    driver = setupAppium( )
    bv = bv + 20
    bar.update(bv)
    json_data = json.loads(open('VPN.json').read())
    bv = bv + 5
    bar.update(bv)
    for vpnconf in json_data:
        bar.update(bv+1)
        server_ip = getServerIp(vpnconf)
        server_ip=json.loads(server_ip)
        #TODO check if ip is 0 skip this test else whole test will stop
        print  server_ip['vpn_server_ip']
        print "Setting up VPN....."
        setupVPN(driver,vpnconf,server_ip['vpn_server_ip'])
        #TODO change name instead of service_id as it might get very longs
        print "Click VPN to connect..."
        connectVPN(driver,vpnconf['service_id'])
        sleep(10)
        #TODO inclune json file name in config
        print "Running Top URL script"
        runScript( driver,vpnconf['urls'],server_ip['vpn_server_ip'])

    print "tests finished"
    driver.quit()
 
    # server_ip = getServerIp(json_data)
    # server_ip = server_ip['vpn_server_ip']
    # print "server Ip:",server_ip
    #
 



 
