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
    everyday_time = datetime.time(hour=3, minute=0, tzinfo=datetime.timezone(timedelta(hours=8)))

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.everyday.start()
        self.tz = datetime.timezone(timedelta(hours=8))
        self.channel_ids = [1300828046131200081, 1192478035966951606]

    @tasks.loop(time=everyday_time)
    async def everyday(self):
        await self.send_everyday_message(self.channel_ids)

    async def send_everyday_message(self, channel_ids):
        today = datetime.datetime.now(tz=self.tz).date()
        target_date = datetime.date(today.year, 7, 29)
        days_str = ["四", "三", "二", "一"]
        days_left = (target_date - today).days

        for c_id in channel_ids:
            channel = self.bot.get_channel(c_id)
            if channel:
                embed = discord.Embed(
                    title="🛏 洞三洞洞 部隊起床",
                    description=f"🕛 現在時間 【{datetime.datetime.now(tz=self.tz).time().strftime('%H:%M')}】",
                    color=discord.Color.orange()
                )

                if days_left > 0 and days_left <= len(days_str):
                    embed.add_field(name="", value=f"屯懸賞第 {days_str[days_left-1]} 天！", inline=False)
                    await channel.send(file=discord.File("./wanted2.jpg"))
                elif days_left == 0:
                    embed.add_field(name="🎉 今天「維修前」掃蕩懸賞", value="懸賞維修前掃光光\n哼！哼！啊啊啊啊啊！", inline=False)
                    await channel.send(file=discord.File("./wanted2.jpg"))

                
                await channel.send(embed=embed)
                await channel.send(file=discord.File("./3am.gif"))

    @commands.command(name='test_everyday')
    async def test_everyday(self, ctx):
        test_channel_ids = [1300828046131200081]
        await self.send_everyday_message(test_channel_ids)
        await ctx.send("✅ 測試訊息已發送！")

class TaskTimes(commands.Cog):
    every_hour_time = [
            datetime.time(hour = i, minute = j, tzinfo = datetime.timezone(timedelta(hours = 8)))
            for i in range(24) for j in range(0,60,2)
    ]
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.every_hour.start()
        self.tz = datetime.timezone(timedelta(hours = 8))
        
    @tasks.loop(time = every_hour_time)
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

            if days_left == 0:
                embed.add_field(name="", value=f"距離 114514 還剩 {days_left} 天！", inline=False)
            elif days_left > 0:
                embed.add_field(name="今天就是 114514！", value="哼!哼!啊啊啊啊啊!\n這麼臭的日子有存在的必要嗎?", inline=False)
            await channel.send(embed = embed)
            await channel.send(file=discord.File("./senpai.gif"))



bot_token = os.environ['TOKEN']
keep_alive.keep_alive()
bot.run(bot_token)
