import discord
import json
import requests
import subprocess
import sys
sys.path.append("..")
import time
import re#eeeeee
from datetime import datetime
from discord.ext import commands
from random import seed

class InfoCog(commands.Cog):
    seed(datetime.now())
    start_time = time.time()
    json_file = "db.json"
    json_db = {}
    try:
        with open(json_file, 'r') as f:
            try:
                json_db = json.load(f)
            except:
                json_db = {}
    except:
        pass

    def __init__(self, bot):
        self.bot = bot

    def get_server_uptime(self):
        """
        Helper function for uptime to get server uptime
        """
        result = subprocess.run(['uptime', '-p'], stdout=subprocess.PIPE)
        return result.stdout.decode("utf-8").rstrip()

    def pretty_print_uptime(self, time):
        #Chomp off the tiny bits
        time = int(time)
        #Need all data in terms of seconds
        minute = 60
        hour = minute * 60
        day = hour * 24
        days = time//day #How many days has this been up?
        time %= day #Get rid of days
        hours = time//hour
        time %= hour
        minutes = time//minute
        time %= minute
        seconds = time
        return f"up {days} days, {hours} hours, {minutes} minutes"

    @commands.command()
    async def uptime(self, ctx):
        """
        Displays the uptime of both the bot and the server the bot is running on
        """
        current = time.time()
        delta = current - self.start_time
        await ctx.send(f"Bot has been {self.pretty_print_uptime(delta)}\nServer has \
        been {self.get_server_uptime()}")

    @commands.command(name='vaccines', aliases=['vc', 'vaccine', 'vaccinations', 'vaccination'])
    async def vaccines(self, ctx, loc="United States"):
        """
        Uses the information available at howmanyvaccinated.com to state how many
        people have been vaccinated based off location
        Will default to United States
        """
        url = "https://www.howmanyvaccinated.com/vaccine"
        states_url = "https://promotions.newegg.com/EC/covid19/vaccination/vaccina.json"

        page = requests.get(url)
        states_page = requests.get(states_url)
        js = page.json()
        states_js = states_page.json()

        state_dat = self.sll(states_js["vaccination_data"], loc)
        dat = None
        if state_dat is None: # Should only do extra work if can't find state data
            dat = self.gll(js, self.normalize_location(loc))

        msg = ""
        if state_dat is not None:
            ad1 = "{:,}".format(int(state_dat['Administered_Dose1_Recip']))
            ad2 = "{:,}".format(int(state_dat['Administered_Dose2_Recip']))

            msg = (f"In {state_dat['LongName']} as of {state_dat['Date']}, there have been "
                f"{ad1}({state_dat['Administered_Dose1_Pop_Pct']}%) "
                f"persons who have received Dose 1, "
                f"{ad2}({state_dat['Administered_Dose2_Pop_Pct']}%) persons who have received Dose 2")

        elif dat is not None:
            # Format the number with commas to make it easier to read
            tot = "{:,}".format(int(dat['total_vaccinations']))
            msg = f"In {loc} as of {dat['date']}, there have been {tot}\
            vaccinations, totalling {dat['total_vaccinations_per_hundred']}% of\
            the population."
            msg = ' '.join(msg.split())
        else:
            msg = f"Unable to find information for {loc}"
        await ctx.send(msg)

    def normalize_location(self, loc):
        """
        Used by vaccines command:
        Will change a phrase like "uNITED sTATES" to "United States" since all 
        location are stored as proper nouns
        """
        arr = [i.lower() for i in loc.split(' ')]
        arr = [
            ''.join(
                [word[i] if i != 0 else word[i].upper() for i in range(len(word))])
            for word in arr
        ]
        return ' '.join(arr)

    def gll(self, js, loc):
        """
        Used for the vaccines command, will find the first information
        based off the country.
        """
        for s in js[::-1]:
            if s['location'] == loc:
                return s
        return None

    def sll(self, js, loc):
        """
        Used for the vaccines command, will search through and try to find the state's
        information using newegg's data
        Heck newegg
        """
        loc = loc.lower()
        for s in js:
            if s['Location'].lower() == loc or s['ShortName'].lower() == loc or s['LongName'].lower() == loc:
                return s
        return None

    @commands.command()
    async def joined(self, ctx):
        """
        Tells you when you joined the server using UTC
        """
        member = ctx.author
        await ctx.send(
            f"Time {member.mention} joined {ctx.guild.name} in UTC:\n{member.joined_at}"
        )

    @commands.command()
    async def whoisjoe(self, ctx):
        """
        Joe mama meme lolol
        """
        if "whoisjoe" in self.json_db:
            await ctx.send(self.json_db['whoisjoe'])
        else:
            await ctx.send("JOE MAMA")

    @commands.command()
    async def prse(self, ctx):
        """
        because of course we need a !prse command
        """
        await ctx.send("PReSEnting: https://github.com/Asterisk007/prse\n[This programming language is not endorsed by the University, nor this Discord server.]")

    # Detect stock tickers and display their current price
    @commands.Cog.listener()
    async def on_message(self, payload):
        max_tickers = 10 # adjusts the max amount of tickers the bot will fetch
        msg_str = await payload.channel.fetch_message(payload.id)
        msg_str = msg_str.content

        output_msg = ""

        # ignore user commands, as well as responses by the bot
        if(msg_str[0] == "!" or payload.author.bot):
            return

        matches = re.finditer("\$[a-zA-Z]+", msg_str)
        num_matches = 0
        for match in matches:
            if(num_matches >= max_tickers):
                num_matches += 1
                continue

            stock = msg_str[match.start()+1:match.end()]
            token = "pk_b2df4f042df34774b50c5693366f8a57" # public token
            request_url = f"https://cloud.iexapis.com/stable/stock/{stock}/quote?token={token}"

            page = requests.get(request_url)
            if(page.status_code != 200):
                continue

            if(num_matches == 0):
                # add a reaction the first time a succesful connection is made. messages with many
                # tickers may take a bit to respond, so this lets the user know the command is working
                await payload.add_reaction('📈')

            num_matches += 1
            js = page.json()

            output_msg += f"➝ {stock.upper()} ({js['companyName']}) - "
            if(js['extendedPrice'] is not None and not js['isUSMarketOpen']):
              output_msg += f"Current price: ${str('{:.2f}'.format(js['latestPrice']))}\n"
              output_msg += f"\t\tAfter hours price: **${str('{:.2f}'.format(js['extendedPrice']))}**\n"
            else:
              output_msg += f"Current price: **${str('{:.2f}'.format(js['latestPrice']))}**\n"

        if(num_matches == 0):
          return

        # we are not guarenteed to respond until at least this line

        if(num_matches > max_tickers):
            output_msg += f"Plus {num_matches - max_tickers} more\n"

        output_msg = "I have detected " + str(num_matches) + f" stock ticker{('s') if num_matches != 1 else ''} in your message\n\n" + output_msg
        output_msg += "\n"
        output_msg += "ᴡᴇ ᴅᴏ ɴᴏᴛ ɢᴜᴀʀᴀɴᴛᴇᴇ ᴛʜᴇ ᴀᴄᴄᴜʀᴀᴄʏ ᴏғ ᴛʜɪs ᴅᴀᴛᴀ"
        channel = payload.channel #await discord.Client.fetch_channel(Cog, payload.channel.id)
        await channel.send(output_msg)

# Adds the cog to the bot
def setup(bot):
    bot.add_cog(InfoCog(bot))
