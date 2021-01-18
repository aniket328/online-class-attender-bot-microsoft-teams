# Microsoft Teams Online Class Attender

This bot attends the online classes (or meetings) held on Microsoft teams, according to the given timetable.


## Configure

There are few things you need to configure before running this bot.

 - Open Microsoft teams on your browser, login to your account, change the dashboard view to list view (from grid view), so that your classes are displayed in a list view. 
 - ![This is how list view looks like](https://i.imgur.com/SSDo8c6.png)
 - Open *bot.py*, and put your microsoft teams credentials in the **CREDS** dictionary. 
 - Example - `CREDS  = {'email' : 'myemail@email.com', 'passwd':'''mypassword'''}`
 - Open *discord_webhook.py* and put your discord webhook URL in the **webhook_url** variable. 
 - Example - `webhook_url = "https://discordapp.com/...."`
 - Make sure that the timezone of the PC is correct. If you're running the bot on cloud, you may want to manually change the timezone of the virtual machine to an appropriate time zone (i.e., the timezone that your online classes follow)

## Install

 - Clone the repository `git clone https://github.com/aniket328/msbot`
 - Install requirements.txt `pip install -r requirements.txt`
 - RUM COMMAND ```pip3 install chromedriver-binary-auto``` #to install chrome driver binary

 

## Run the bot

 - Run the bot `msbot.py`

Enjoy!
Written on Python3.

Please raise an issue if you face any difficulty in running the bot.