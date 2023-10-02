## Discord bot for Hackathon
This bot is a continuing project and I welcome pull requests that improve/fix or add features


## Installation Instructions
This installation will be using WSL/Linux

### Prerequisites:

Git 

Python 3.9

Discord Account

Discord Developer Account


## Creating the Bot

More Detailed instructions under: https://discord.com/developers/docs/getting-started
1.  Create the discord application using your account
https://discord.com/developers/applications

2.  Create the bot under the BOT tab
   
3.  Copy your TOKEN and keep it someplace safe, think of the TOKEN as a password for your bot

4.  Go to the OAUTH tab, then the URL Generator tab click on the checkboxes labeled "Bot" and "Administrator"
  
5.  Click generate link

6.  Copy the URL into your browser

7.  Add the Bot to your server  


## This installation will be done using Linux/WSL

## Installing WSL (Windows Users)

https://docs.microsoft.com/en-us/windows/wsl/install

(Pro Tip, make a shortcut to your WSL folder using `explorer.exe ~ `)

## Installing VENV

   `sudo apt install python3-venv`

##

## Creating the Directory

1. `mkdir -p ~/Documents/repos/`

2. `cd ~/Documents/repos/`

### Cloning The Github Repo
1. `git clone https://github.com/CodeMastr3/hackbot.git`

2. `cd hackbot`

### Using the correct version of python

As Charon was developed in 2020, there are a few notes, the current version of Python will not work. The latest version I can get to work is Python 3.9.0 which can be found [here](https://www.python.org/downloads/release/python-390/).  

Because of this you will need to use `python3.9` when working with your venv and running the bot

### Starting VENV and Installing Required Libraries
1. `python3.9 -m venv venv`

2. `source venv/bin/activate`

3. `pip install -r requirements.txt`

## Setting Token and Starting the Bot

1. `export TOKEN=<INSERT_TOKEN_HERE>`

2. `python3.9 bot.py`


# Credits and Acknowledgements
* Feel free to take the code and create your own bot to host.
* Originally created by AguilarJoel, jameswhowell, and CodeMastr3 on March 7, 2020.
* Join our Discord Server! http://charon.click
