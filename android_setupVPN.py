# To automate the setup a Ikev2 VPN Tunnel on Android devices

from appium import webdriver
from time import sleep

desired_caps = {}
desired_caps['platformName'] = 'Android'
desired_caps['platformVersion'] = '6.0.1'
desired_caps['deviceName'] = 'Android Emulator'
desired_caps['app'] ='com.android.settings'
desired_caps['appPackage'] = 'com.android.settings'
desired_caps['appActivity'] = '.Settings'

driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)



#1 . ################################ Add and save a VPN Tunnel on device #################################
more_connection = driver.find_element_by_android_uiautomator('new UiSelector().text("More connection settings")')
more_connection.click()
driver.find_element_by_android_uiautomator('new UiSelector().text("VPN")').click()
driver.find_element_by_id("com.android.settings:id/vpn_create").click()
driver.find_element_by_id("com.android.settings:id/name").set_text('Test VPN - USA WEST')
#select Type from Spinner
driver.find_element_by_id("com.android.settings:id/type_with_strongswan").click()
driver.find_element_by_android_uiautomator('new UiSelector().textContains("IPSec IKEv2 PSK")').click()
driver.hide_keyboard(key_name='Done')
driver.page_source
#select Server Address text field 
driver.find_element_by_id("com.android.settings:id/server").set_text('107.182.238.199')
driver.hide_keyboard(key_name='Done')
driver.page_source
#select IPSec Identifier text field 
driver.find_element_by_id("com.android.settings:id/ipsec_identifier").set_text('amc@gmail.com')
driver.hide_keyboard(key_name='Done')
driver.page_source
#select IPSec psk text field 
driver.find_element_by_id("com.android.settings:id/ipsec_secret").set_text('100100')
driver.hide_keyboard(key_name='Done')
driver.page_source
#Save the entered credentials
driver.find_element_by_id("android:id/button1").click()
driver.page_source


#2 . ################################ Connect to the saved VPN Tunnel #################################
driver.find_element_by_android_uiautomator('new UiSelector().text("Test VPN - USA WEST")').click()
driver.page_source
driver.find_element_by_id("android:id/button1").click()
sleep(10)


#3 . ################################ Open Termux and run top100 url script #################################
driver.start_activity('com.termux', '.app.TermuxActivity')
terminal=driver.find_element_by_android_uiautomator('new UiSelector().resourceId("com.termux:id/terminal_view")')
terminal.set_text("cd nodedroid" + "\n")
terminal.set_text("git pull" + "\n")
terminal.set_text("node index.js -w=US100.json" + "\n")
sleep(100)




 



 
