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
import os

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
        await ctx.send(f"Bot has been {self.pretty_print_uptime(delta)}\nServer has been {self.get_server_uptime()}")

    """
    @commands.command()
    async def poll(self, ctx, *arg):
        "Adds (a) reaction(s) to a poll message with the number immediately after poll"
        for i in range(arg1):
            ctx.send('I\'m not implemented yet')
            #
            #await ctx.message.add_reaction('\U0001F3B2')
    """

    @commands.command(name='vaccines', aliases=['vc', 'vaccine', 'vaccinations', 'vaccination'])
    async def vaccines(self, ctx, loc="United States"):
        """
        Uses the information available at howmanyvaccinated.com to state how many
        people have been vaccinated based off location
        Will default to United States
        """
        url = "https://www.howmanyvaccinated.com/vaccine"
        #states_url = "https://promotions.newegg.com/EC/covid19/vaccination/vaccina.json"
        states_url = "https://covid.cdc.gov/covid-data-tracker/COVIDData/getAjaxData?id=vaccination_data"

        page = requests.get(url)
        states_page = requests.get(states_url)
        js = page.json()
        states_js = states_page.json()

        state_dat = self.sll(states_js["vaccination_data"], loc)
        dat = None
        if state_dat is None: #Should only do extra work if can't find state data
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
            #Format the number with commas to make it easier to read
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
    async def classes(self, ctx, class_name="CSCI-111"):
        """
        Will query CSU Chico's Class schedule to show info about classes. Format: 'CSCI-111' or 'cins_465'
        """
        message = ""
        try:
            subject, catalog_nbr = re.split('-|_', class_name, 1)
            subject = subject.upper()
        except:
            message += f"Failed to parse {class_name}, failing..."
            await ctx.send(message)
            return None
        url = "https://cmsweb.csuchico.edu/psc/CCHIPRD/EMPLOYEE/SA/s/WEBLIB_HCX_CM.H_CLASS_SEARCH.FieldFormula.IScript_ClassSearch?"
        params = {
            'institution': 'CHICO',
            'term': self.get_term(0),
            'subject': subject,
            'catalog_nbr': catalog_nbr,
        }
        class_result = requests.get(url, params)
        if class_result.status_code == 200:
            class_dict = class_result.json()
            message += f"Search results for {class_name}:\n"
            if not bool(class_dict):
                message += "No classes found with that Subject and Catalog Number"
            else:
                for class_found in class_dict:
                    class_msg = ""
                    prof = class_found['instructors'][0]['name']
                    class_msg += f"{class_found['subject']}-{class_found['catalog_nbr']} {class_found['component']} Section {class_found['class_section']}: \t{prof}\n"
                    for class_time in class_found['meetings']:
                        try:
                            class_msg += f"\t{class_time['days']}\t{class_time['bldg_cd']} {class_time['room']}\n"

                            start_hour, start_minute, excess = class_time['start_time'].split('.', 2)
                            start_hour_int = int(start_hour) if int(start_hour) <= 12 else int(start_hour) % 12
                            start_M = "PM" if int(start_hour) >= 12 else "AM"
                            class_msg += f"\t{start_hour_int}:{start_minute} {start_M}"

                            end_hour, end_minute, excess = class_time['end_time'].split('.', 2)
                            end_hour_int = int(end_hour) if int(end_hour) <= 12 else int(end_hour) % 12
                            end_M = "PM" if int(end_hour) >= 12 else "AM"

                            class_msg += f"\t{end_hour_int}:{end_minute} {end_M}\n--------------------------------\n"
                        except:
                            pass
                        message += class_msg
        else:
            message = "Failed to retrieve data from server"
        if len(message) > 2000:
            message = "Holy cow there were too many classes to list! Try a more specific search."
        await ctx.send(message)
        return None

    def get_term(self, mod):
        """
        Used for the classes command, uses current date to determine the term number to be
        used in parameters
        """
        # Mod can be used to change the relative term. Don't have the energy currently to implement
        today_term = datetime.now()
        add_sem = 0
        if today_term.month > 6:
            add_sem = 6
        term = (today_term.year % 2022)*10 + 2222 + add_sem
        return str(term)

    @commands.command()
    async def joined(self, ctx):
        """
        Tells you when you joined the server using UTC
        """
        members = ctx.message.mentions
        message = ""
        if len(members) < 1:
            members = [ ctx.author ]

        for member in members:
            if len(message) > 0:
                message += "\n\n"
            message += f"{member.mention} joined {ctx.guild.name}\n{member.joined_at}"

        if len(message) > 2000:
            message = "Too many members to check"

        await ctx.send(message)

    @commands.command()
    async def whoisjoe(self, ctx):
        """
        Joe mama meme lolol
        """
        if "whoisjoe" in self.json_db:
            await ctx.send(self.json_db['whoisjoe'])
        else:
            await ctx.send("JOE MAMA")

    @commands.command(hidden=True)
    async def joeis(self, ctx, *, arg):
        """
        Will alter the output from whoisjoe
        """
        json_file = "db.json"
        #Alter memory copy
        self.json_db['whoisjoe'] = arg
        #Write to FS
        with open(json_file, 'w') as f:
            json.dump(self.json_db, f)
        await ctx.message.delete()

    @commands.command()
    async def prse(self, ctx):
        """
        because of course we need a !prse command
        """
        await ctx.send("PReSEnting: https://github.com/Asterisk007/prse\n[This programming language is not endorsed by the University, nor this Discord server.]")

    # detect stock tickers and display their current price
    @commands.Cog.listener()
    async def on_message(self, payload):
        max_tickers = 10 # adjusts the max amount of tickers the bot will fetch
        try: 
            msg_str = await payload.channel.fetch_message(payload.id)
        except:
            return
        msg_str = msg_str.content

        output_msg = ""

        # ignore user commands, as well as responses by the bot
        if(payload.author.bot or msg_str[0] == "!" ):
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
            @commands.Cog.listener()
            
            
            #due to low enrollment, charon has been reduced to become a walking advertisement ;-(
    @commands.Cog.listener()
    async def on_message(self, message):

        ad_msg_channel = await message.channel.fetch_message(message.id)
        channel = ad_msg_channel.channel
        ad_msg = ad_msg_channel.content
        msgCount = randint(1, 1000)
        keywords = ['enroll','enrollment','classes','class','565']

        if(message.author.bot or ad_msg[0] == "!" or msgCount != 69):
            return
        
        else:
            five_sixty_five_Ad = choice(["Have you thought about CSCI-565?", "CSCI-565 is looking real nice", "Obviously this means you should Enroll in CSCI-565", "CSCI-565?",
                                    "Don't care, Enroll in CSCI-565"])
            await message.reply(f'{five_sixty_five_Ad}')
            

def setup(bot):
    bot.add_cog(InfoCog(bot))
