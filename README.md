# Requirements


- Linux, Windows or Mac OS 
- Python Installed on the machine
- Google Chrome installed
- (This script uses google chrome driver to run the web-browser, you can use mozilla or any other browser with their respective driver and slight modificaiton in the code, if you face any issue let me know in the issues box, i will try to fix them asap.)

# Microsoft Teams Online Class Attender


This bot attends the online classes (or meetings) held on Microsoft teams, according to the given timetable.

## Configure

There are few things you need to configure before running this bot.

 - Open Microsoft teams on your browser, login to your account, change the dashboard view to list view (from grid view), so that your classes are displayed in a list view. 
 - ![This is how list view looks like](https://github.com/aniket328/images-raw/blob/main/list-view-team.png)
 - Open *msbot.py*, and put your microsoft teams credentials in the **CREDS** dictionary. 
 - Example - `CREDS  = {'email' : 'myemail@email.com', 'passwd':'''mypassword'''}`
 - Open *discord_webhook.py* and put your discord webhook URL in the **webhook_url** variable. 
 - Example - `webhook_url = "https://discordapp.com/...."`
 - Make sure that the timezone of the PC is correct. If you're running the bot on cloud, you may want to manually change the timezone of the virtual machine to an appropriate time zone (i.e., the timezone that your online classes follow)

## Install

 - Clone the repository ```https://github.com/aniket328/online-class-attender-bot-microsoft-teams.git```
 - Install requirements.txt `pip install -r requirements.txt`
 - Run cmd (to install chrome binary): ```pip3 install chromedriver-binary-auto```


## Run the bot

 - Run the bot `python msbot.py`
 - Press ctrl+C to quit

Written on Python3.

 # YOUTUBE REFERENCE TUTORIAL
 https://youtu.be/wY7ffeCT3Ro
