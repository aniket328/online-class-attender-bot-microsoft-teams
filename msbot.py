from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
#import chromedriver_binary
import time
import re
import os.path
from os import path
import sqlite3
import schedule
from datetime import datetime
from selenium.webdriver.common.action_chains import ActionChains
#import discord_webhook

opt = Options()
#linux
#opt.add_argument('--headless')
opt.add_argument('--no-sandbox')
opt.add_argument('--disable-dev-shm-usage')
opt.add_argument("--disable-infobars")
opt.add_argument("start-maximized")
opt.add_argument("--disable-extensions")
opt.add_experimental_option("prefs", { \
    "profile.default_content_setting_values.media_stream_mic": 1, 
    "profile.default_content_setting_values.media_stream_camera": 1,
    "profile.default_content_setting_values.geolocation": 1, 
    "profile.default_content_setting_values.notifications": 1 
 	 })


driver = None
URL = "https://teams.microsoft.com"
PASS = 'S7Lf(J%xgUXt\"8\''
CREDS = {'email':'email@gmail.com','passwd':PASS}

def out():
    driver.close()
    driver.quit()
    exit()

def login():
    global driver
    print('logging in...')
    emailField=driver.find_element_by_xpath('//*[@id="i0116"]')
    emailField.click()
    emailField.send_keys(CREDS['email'])
    print('validating email...')
    driver.find_element_by_xpath('//*[@id="idSIButton9"]').click() #nextbutton
    time.sleep(5)
    try:
        passField=driver.find_element_by_xpath('//*[@id="i0118"]')
        passField.click()
        print('validating password...')
        passField.send_keys(CREDS['passwd'])
        driver.find_element_by_xpath('//*[@id="idSIButton9"]').click()
        time.sleep(5)
        print('Staying signed in...')
        driver.find_element_by_xpath('//*[@id="idSIButton9"]').click()
        print('Login SUCCESS !!')
        print('make sure you have changed the class view in your teams account to list view ')
        time.sleep(5)


    except:
        print('invalid email, kindly correct credentials in CRED Dictionary for help refer README.md')
        out()


def createDB():
    conn=sqlite3.connect('timetable.db')
    c=conn.cursor()
    #create table
    c.execute('''CREATE TABLE IF NOT EXISTS timetable (class text, start_time text, end_time text,day text)''')
    conn.commit()
    conn.close()
    print("Created timetable Database")

def validate_input(regex,inp):
	if not re.match(regex,inp):
		return False
	return True

def validate_day(inp):
	days = ["monday","tuesday","wednesday","thursday","friday","saturday","sunday"]

	if inp.lower() in days:
		return True
	else:
		return False

def add_timetable():

	name = input("Enter class name : ")
	start_time = input("Enter class start time in 24 hour format: (HH:MM) ")
	while not(validate_input("\d\d:\d\d",start_time)):
		print("Invalid input, try again")
		start_time = input("Enter class start time in 24 hour format: (HH:MM) ")

	end_time = input("Enter class end time in 24 hour format: (HH:MM) ")
	while not(validate_input("\d\d:\d\d",end_time)):
		print("Invalid input, try again")
		end_time = input("Enter class end time in 24 hour format: (HH:MM) ")

	day = input("Enter day (Monday/Tuesday/Wednesday..etc) : ")
	while not(validate_day(day.strip())):
		print("Invalid input, try again")
		end_time = input("Enter day (Monday/Tuesday/Wednesday..etc) : ")


	conn = sqlite3.connect('timetable.db')
	c=conn.cursor()

	# Insert a row of data
	c.execute("INSERT INTO timetable VALUES ('%s','%s','%s','%s')"%(name,start_time,end_time,day))

	conn.commit()
	conn.close()

	print("Class added to database\n")

def view_timetable():
	conn = sqlite3.connect('timetable.db')
	c=conn.cursor()
	num=0
	for row in c.execute('SELECT * FROM timetable'):
		num+=1
		print(str(num)+'. ',row)
	conn.close()

def update_timetable():
	class_name = input("Enter the class name you want to update: ")
	conn = sqlite3.connect('timetable.db')
	c = conn.cursor()
	c.execute("SELECT * FROM timetable WHERE class = :class", {"class":class_name})
	results = c.fetchall()

	if len(results) == 0:
		print(f"Found no such class named {class_name}!")
		return None

	while (True):
		start_time = input("Enter new class start time in 24 hour format: (HH:MM) ")
		while not(validate_input("\d\d:\d\d",start_time)):
			print("Invalid input, try again")
			start_time = input("Enter new class start time in 24 hour format: (HH:MM) ")

		end_time = input("Enter new class end time in 24 hour format: (HH:MM) ")
		while not(validate_input("\d\d:\d\d",end_time)):
			print("Invalid input, try again")
			end_time = input("Enter new class end time in 24 hour format: (HH:MM) ")

		day = input("Enter new day (Monday/Tuesday/Wednesday..etc) : ")
		while not(validate_day(day.strip())):
			print("Invalid input, try again")
			end_time = input("Enter new day (Monday/Tuesday/Wednesday..etc) : ")


		c.execute("UPDATE timetable SET start_time = :new_start_time WHERE class = :class", {"new_start_time":start_time, "class":class_name})
		c.execute("UPDATE timetable SET end_time = :new_end_time WHERE class = :class", {"new_end_time":end_time, "class":class_name})
		c.execute("UPDATE timetable SET day = :new_day WHERE class = :class", {"new_day":day, "class":class_name})
		conn.commit()
		conn.close()
		print(f"Class {class_name} updated with new start time as {start_time}, new end time as {end_time} and new day as {day} successfully. ")
		break

def delete_timetable():
	class_name = input("Enter the name of the class you want to delete: ")
	conn = sqlite3.connect("timetable.db")
	c = conn.cursor()
	c.execute("SELECT * FROM timetable WHERE class = :class", {"class":class_name})
	results = c.fetchall()

	if len(results) == 0:
		print(f"Found no such class named {class_name}!")
		return None

	_ = input(f"Are you sure you want to delete class {class_name}? This action cant be undone. Press any key to continue. ")
	c.execute("DELETE FROM timetable WHERE class = :class", {"class":class_name})
	conn.commit()
	conn.close()
	print(f"Deleted entry {class_name} from timetable successully. ")

def start_browser():
    global driver
    #try:    
    driver=webdriver.Chrome(options=opt)
    print('getting URL')
    driver.get(URL)
    print('awaiting login promt')
    WebDriverWait(driver,10000).until(EC.visibility_of_element_located((By.TAG_NAME,'body')))
    if("login.microsoftonline.com" in driver.current_url):
        login()

def attend(class_name,start_time,end_time):
	time.sleep(4)
	webcam = driver.find_element_by_xpath('//*[@id="page-content-wrapper"]/div[1]/div/calling-pre-join-screen/div/div/div[2]/div[1]/div[2]/div/div/section/div[2]/toggle-button[1]/div/button/span[1]')
	if(webcam.get_attribute('title')=='Turn camera off'):
		webcam.click()
	time.sleep(1)
	print('switched off webcam...')
	microphone = driver.find_element_by_xpath('//*[@id="preJoinAudioButton"]/div/button/span[1]')
	if(microphone.get_attribute('title')=='Mute microphone'):
		microphone.click()
	print('switched off microphone...')
	time.sleep(1)
	joinnowbtn = driver.find_element_by_xpath('//*[@id="page-content-wrapper"]/div[1]/div/calling-pre-join-screen/div/div/div[2]/div[1]/div[2]/div/div/section/div[1]/div/div/button')
	joinnowbtn.click()
	print('Joining class SUCCESSFUL\n currently attending class...')
	
	
	#now schedule leaving class
	tmp = "%H:%M"

	class_running_time = datetime.strptime(end_time,tmp) - datetime.strptime(start_time,tmp)

	time.sleep(class_running_time.seconds)
	print('time to leave the class')

	try:
		driver.find_element_by_class_name("ts-calling-screen").click()
		driver.find_element_by_xpath('//*[@id="teams-app-bar"]/ul/li[3]').click() #come back to homepage
		time.sleep(1)
		driver.find_element_by_xpath('//*[@id="hangup-button"]').click()
		print("Class left")
	except:
		print('seems the lecture has already stopped...')

def button_present():
	try:
		tele=driver.find_element_by_class_name("ts-calling-join-button")
		return True
	except:
		return False

def check_class(class_name,start_time,end_time):
	present=button_present()
	count=1
	while count<=15:
		count+=1
		if present:
			count-=1
			print('class found...')
			driver.find_element_by_class_name("ts-calling-join-button").click()
			print('now joining class...')
			attend(class_name,start_time,end_time)
			break
		else:
			print('class not found...rechecking after few seconds')
			driver.refresh()
			time.sleep(20)
			present=button_present()
	
	if count==6:
		print('Seems there is no class, aborting this search')

def joinclass(class_name,start_time,end_time):
	global driver
	
	print('in function join classsss')
	
	try:
		element = WebDriverWait(driver, 20).until(
			EC.presence_of_element_located((By.ID, "left-rail-header")))
	except:
		print('class not found in list of teams! aborting this class')
	
	time.sleep(2)
	classes_available = driver.find_elements_by_class_name("name-channel-type")

	for i in classes_available:
		print('checking i\'s')
		if class_name.lower() in i.get_attribute('innerHTML').lower():
			print("Subject Found...",class_name)
			i.click()
			time.sleep(4)
			print('Checking Class status...')
			check_class(i,start_time,end_time)
			break

def join_specific():
	print('\nSELECT ONE:')
	view_timetable()
	want=int(input("Enter your choice:"))

	name=None
	start_time=None
	end_time=None
	day=None

	conn=sqlite3.connect('timetable.db')
	c=conn.cursor()
	
	cc =0

	for row in c.execute('SELECT * FROM timetable'):
		cc+=1
		name=row[0]
		start_time=row[1]
		end_time=row[2]
		day=row[3]
		if cc==want:
			break
	conn.close()
	if want > cc:
		print('invalid input')
	else:
		print("\nyou have selected class:",name,"\nstarting from:",start_time,"\nto:",end_time,"\non",day)	
		tek=input("Do you want to initiate Bot? [y/n] : ")
		if tek=='y' or tek=='Y':
			start_browser()
			print('initiating join class ... ')
			
			joinclass(name,start_time,end_time)
			print(name,start_time,end_time)


def sched():
	conn=sqlite3.connect('timetable.db')
	c=conn.cursor()
	for row in c.execute('SELECT * FROM timetable'):
		name=row[0]
		start_time=row[1]
		end_time=row[2]
		day=row[3]

		if day.lower()=="monday":
			schedule.every().monday.at(start_time).do(joinclass,name,start_time,end_time)
			print("Scheduled class '%s' on %s at %s"%(name,day,start_time))
		if day.lower()=="tuesday":
			schedule.every().tuesday.at(start_time).do(joinclass,name,start_time,end_time)
			print("Scheduled class '%s' on %s at %s"%(name,day,start_time))
		if day.lower()=="wednesday":
			schedule.every().wednesday.at(start_time).do(joinclass,name,start_time,end_time)
			print("Scheduled class '%s' on %s at %s"%(name,day,start_time))
		if day.lower()=="thursday":
			schedule.every().thursday.at(start_time).do(joinclass,name,start_time,end_time)
			print("Scheduled class '%s' on %s at %s"%(name,day,start_time))
		if day.lower()=="friday":
			schedule.every().friday.at(start_time).do(joinclass,name,start_time,end_time)
			print("Scheduled class '%s' on %s at %s"%(name,day,start_time))
		if day.lower()=="saturday":
			schedule.every().saturday.at(start_time).do(joinclass,name,start_time,end_time)
			print("Scheduled class '%s' on %s at %s"%(name,day,start_time))
		if day.lower()=="sunday":
			schedule.every().sunday.at(start_time).do(joinclass,name,start_time,end_time)
			print("Scheduled class '%s' on %s at %s"%(name,day,start_time))

	#Start browser
	start_browser()
	tuna=1
	while True:
		# Checks whether a scheduled task
		# is pending to run or not
		print("i am waiting for the class" + str(tuna))
		tuna+=1
		schedule.run_pending()
		time.sleep(1)

if __name__=="__main__":
	# joinclass("Maths","15:13","15:15","sunday")
	createDB()
	while True:
		op = int(input(("\n\n1. Start Bot \n2. View Timetable \n3. Update Timetable \n4. Add Class \n5. Delete Class\n6. Join Specific Class\n7. Exit\nEnter option : ")))
		if(op==1):
			sched()	
		elif(op==2):
			view_timetable()
		elif (op==3):
			update_timetable()
		elif (op==4):
			add_timetable()
		elif(op==5):
			delete_timetable()
		elif(op==6):
			join_specific()
		else:
			print("Invalid input!")
			exit()