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

More Detailed instructions under: https://discord.com/developers/docs/getting-started
1.  Create the discord Application using your account
https://discord.com/developers/applications

2.  Create the bot under the BOT tab
   
3.  Copy your TOKEN and keep it someplace safe, think of the TOKEN as a password for your bot

4.  go to the OAUTH tab, and URL Generator select "Bot" and "Administrator"

5.  Copy the URL into your browser

6.  Add the Bot to your server  



https://discordapp.com/oauth2/authorize?&client_id=[CLIENT ID]&scope=bot

## Installing WSL (Windows Users)

https://docs.microsoft.com/en-us/windows/wsl/install

(Pro Tip, make a shortcut to your WSL folder using explorer.exe ~ )

## Installing VENV

`sudo apt install python3-venv`

##

## Creating the Directory

`mkdir -p ~/Documents/repos/`

`cd ~/Documents/repos/`

### Cloning The Github Repo
`git clone https://github.com/CodeMastr3/hackbot.git`

`cd hackbot`


### Starting VENV and installing Required Libraries

`python3 -m venv venv`

`source venv/bin/activate`

`pip install -r requirements.txt`

## Setting Token and Starting the Bot

`export TOKEN = <INSERT_TOKEN_HERE> `

`python3 bot.py`


#Credits and Acknowledgements
* Feel free to take the code and create your own bot to host.
* Originally created by AguilarJoel, jameswhowell, and CodeMastr3 on March 7, 2020.
