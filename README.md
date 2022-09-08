# hackbot
## Discord bot for Hackathon
### This bot is a continuing project and I welcome pull requests that improve/fix or add features







# Installation Instructions

Prerequisites:
Linux / WSL
Git 
Python 3
Discord Account
VENV


## Creating the Bot

1. Create the discord bot using your account
https://discord.com/developers/applications

2. 

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
* Uses a `.env` file to define the bot token. Syntax is `TOKEN="<discord bot token here>"`.
    * Place the `.env` file in the same directory as this project.
* Originally created by AguilarJoel, jameswhowell, and CodeMastr3 on March 7, 2020.
