# hackbot
## Discord bot for Hackathon
### This bot is a continuing project and I welcome pull requests that improve/fix or add features

* Feel free to take the code and create your own bot to host.
* Uses a `.env` file to define the bot token. Syntax is `TOKEN=<discord bot token here>`
    * This is currently broken. As a temporary solution, when testing you code locally, use the following procedure:
    * In `bot.py`:
        * Comment out the line `import token1 as token`
        * At the bottom of the file, temporarily comment out the line `bot.run(token.stringToken())`
        and replace it with `bot.run("<bot token here>")`. Remember to delete this temporary line afterwards,
        as committing your Discord private token is a major security risk.
    * Run `python ./bot.py`. Procede to test as usual.
* Originally created by AguilarJoel, jameswhowell, and CodeMastr3 on March 7, 2020.
