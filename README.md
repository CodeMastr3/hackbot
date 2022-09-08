## Discord bot for Hackathon
This bot is a continuing project and I welcome pull requests that improve/fix or add features







## Installation Instructions

Prerequisites:

Linux / WSL

Git 

Python 3

Discord Account

VENV


## Creating the Bot

1. Create the discord Application using your account
https://discord.com/developers/applications
![installation instructions](https://github.com/thomasdevine01/hackbot-1/blob/master/Installation%20Images/New%20Application.png?raw=true)

2. Create the bot

   ![installation instructions](https://github.com/thomasdevine01/hackbot-1/blob/master/Installation%20Images/AddBot.png?raw=true) 
   
3. Copy your TOKEN and keep it someplace safe, think of the TOKEN as a password for your bot

4. go to the OAUTH tab, and URL Generator

5. Copy the URL into your browser



https://discordapp.com/oauth2/authorize?&client_id=[CLIENT ID]&scope=bot

## Installing WSL (Windows Users)

https://docs.microsoft.com/en-us/windows/wsl/install

(Pro Tip, make a shortcut to your WSL folder using explorer.exe ~ )

## Installing VENV

sudo apt install python3-venv

##

## Creating the Directory

mkdir -p ~/Documents/repos/
cd ~/Documents/repos/

### Cloning The Github Repo
git clone https://github.com/CodeMastr3/hackbot.git
cd hackbot


### Starting VENV and installing Required Libraries

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

## Setting Token and Starting the Bot

export TOKEN = <INSERT_TOKEN_HERE> 
python3 bot.py


* Feel free to take the code and create your own bot to host.
* Originally created by AguilarJoel, jameswhowell, and CodeMastr3 on March 7, 2020.
