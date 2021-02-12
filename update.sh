#!/bin/bash

BOTSESH="bot"
BOTPANE=0
TOBOT="tmux send-keys -t $BOTSESH.$BOTPANE"

#Stop Bot
$TOBOT C-c

#Update Repo
$TOBOT "git pull origin master" ENTER

#Make Sure Packages are Up To Date
$TOBOT "pip install -r requirements.txt" ENTER

#Restart Bot
$TOBOT "python bot.py" ENTER
