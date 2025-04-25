import os
import discord 
import datetime
from datetime import timedelta
from discord.ext import tasks, commands
import keep_alive

intents = discord.Intents.default()
intents.messages = True
bot = commands.Bot(command_prefix = "!", intents = intents)

@bot.event
async def on_ready():
    await bot.add_cog(TaskTime(bot))
    #await bot.add_cog(TaskTimes(bot))
    print(f"目前登入身份 --> {bot.user}")

class TaskTime(commands.Cog):
    tz = datetime.timezone(timedelta(hours = 8))
    everyday_time = datetime.time(hour = 3, minute = 0, tzinfo = datetime.timezone(timedelta(hours = 8)))

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.everyday.start()
    
    @tasks.loop(time = everyday_time)
    async def everyday(self):
        channel_ids = [1300828046131200081, 1192478035966951606]
        for c_id in channel_ids:
            channel = self.bot.get_channel(c_id)
            if channel:
                embed = discord.Embed(
                    title = "🛏 洞三洞洞 部隊起床",
                    description = f"🕛 現在時間 【{datetime.datetime.now(tz = self.tz).time().strftime('%H:%M')}】",
                    color = discord.Color.orange()
                )
                await channel.send(embed = embed)
                await channel.send(file=discord.File("./3am.gif"))

class TaskTimes(commands.Cog):
    tz = datetime.timezone(timedelta(hours = 8))
    every_hour_time = [
        datetime.time(hour = i, minute = j, tzinfo = datetime.timezone(timedelta(hours = 8)))
        for i in range(24) for j in range(0,60,2)
    ]

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.every_hour.start()
    
    @tasks.loop(time = every_hour_time)
    async def every_hour(self):
        channel_id = 1300828046131200081
        channel = self.bot.get_channel(channel_id)
        if channel:
            embed = discord.Embed(
                title = "🛏 洞三洞洞 部隊起床",
                description = f"🕛 現在時間 【{datetime.datetime.now(tz = self.tz).time().strftime('%H:%M')}】", 
                color = discord.Color.random()
            )
            await channel.send(embed = embed)
            await channel.send(file=discord.File("./3am.gif"))



bot_token = os.environ['TOKEN']
keep_alive.keep_alive()
bot.run(bot_token)
