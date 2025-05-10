import os
import discord 
import datetime
from datetime import timedelta
from discord.ext import tasks, commands
import keep_alive

intents = discord.Intents.default()
intents.message_content = True  # 正確方式
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    await bot.add_cog(TaskTime(bot))
    #await bot.add_cog(TaskTimes(bot))
    print(f"目前登入身份 --> {bot.user}")

class TaskTime(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.everyday.start()
        self.tz = datetime.timezone(timedelta(hours=8))
        self.everyday_time = datetime.time(hour=3, minute=0, tzinfo=tz)

    @tasks.loop(time=self.everyday_time)
    async def everyday(self):
        channel_ids = [1300828046131200081, 1192478035966951606]
        today = datetime.datetime.now(tz=self.tz).date()
        target_date = datetime.date(today.year, 5, 14)

        # 計算倒數天數
        days_left = (target_date - today).days

        for c_id in channel_ids:
            channel = self.bot.get_channel(c_id)
            if channel:
                embed = discord.Embed(
                    title="🛏 洞三洞洞 部隊起床",
                    description=f"🕛 現在時間 【{datetime.datetime.now(tz=self.tz).time().strftime('%H:%M')}】",
                    color=discord.Color.orange()
                )

                # 加入倒數或特別訊息
                if days_left > 0:
                    embed.add_field(name="📅 倒數中", value=f"距離 114514 還剩 {days_left} 天！", inline=False)
                elif days_left == 0:
                    embed.add_field(name="🎉 今天就是 114514！", value="哼!哼!啊啊啊啊啊! 這麼臭的日子有存在的必要嗎", inline=False)

                await channel.send(embed=embed)
                await channel.send(file=discord.File("./3am.gif"))

class TaskTimes(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.every_hour.start()
        self.tz = datetime.timezone(timedelta(hours = 8))
        self.every_hour_time = [
            datetime.time(hour = i, minute = j, tzinfo = datetime.timezone(timedelta(hours = 8)))
            for i in range(24) for j in range(0,60,2)
        ]
    
    @tasks.loop(time = self.every_hour_time)
    async def every_hour(self):
        channel_id = 1300828046131200081
        channel = self.bot.get_channel(channel_id)

        today = datetime.datetime.now(tz=self.tz).date()
        target_date = datetime.date(today.year, 5, 14)

        # 計算倒數天數
        days_left = (target_date - today).days
        
        if channel:
            embed = discord.Embed(
                title = "🛏 洞三洞洞 部隊起床",
                description = f"🕛 現在時間 【{datetime.datetime.now(tz = self.tz).time().strftime('%H:%M')}】", 
                color = discord.Color.random()
            )

            if days_left > 0:
                embed.add_field(name="📅 倒數中", value=f"距離 114514 還剩 {days_left} 天！", inline=False)
            elif days_left == 0:
                embed.add_field(name="🎉 今天就是 114514！", value="哼!哼!啊啊啊啊啊! 這麼臭的日子有存在的必要嗎", inline=False)
            await channel.send(embed = embed)
            await channel.send(file=discord.File("./3am.gif"))



bot_token = os.environ['TOKEN']
keep_alive.keep_alive()
bot.run(bot_token)
