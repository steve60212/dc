import os
import discord 
import datetime as dt
from datetime import timedelta
from discord.ext import tasks, commands
import keep_alive
from fb_helper import *
import time

intents = discord.Intents.default()
intents.message_content = True  # 正確方式
bot = commands.Bot(command_prefix="!", intents=intents)

ALLOWED_GUILD_IDs = [1192478035966951606]

@bot.event
async def on_ready():
    await bot.add_cog(TaskTime(bot))
    #await bot.add_cog(TaskTimes(bot))
    print(f"目前登入身份 --> {bot.user}")
'''
@bot.command(name='fb')
async def manual_fb_info(ctx, *, url: str = None):
    """手動取得Facebook影片資訊"""
    if not url or not is_facebook_url(url):
        embed = discord.Embed(
            description="請提供Facebook影片連結\n範例：`!fb https://www.facebook.com/share/xxx`",
            color=0x1877f2
        )
        await ctx.reply(embed=embed)
        return
    
    await handle_facebook_video(ctx.message, url, delete_original=True)
'''
class TaskTime(commands.Cog):
    everyday_time = dt.time(hour=3, minute=0, tzinfo=dt.timezone(timedelta(hours=8)))

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.everyday.start()
        self.tz = dt.timezone(timedelta(hours=8))

    @tasks.loop(time=everyday_time)
    async def everyday(self):
        await self.send_everyday_message(ALLOWED_GUILD_IDs)

    async def send_everyday_message(self, channel_ids):
        today = dt.datetime.now(tz=self.tz).date()
        target_date = dt.date(today.year, 7, 29)
        days_str = ["四", "三", "二", "一"]
        days_left = (target_date - today).days

        for c_id in channel_ids:
            channel = self.bot.get_channel(c_id)
            if channel:
                embed = discord.Embed(
                    title="🛏 洞三洞洞 部隊起床",
                    description=f"🕛 現在時間 【{dt.datetime.now(tz=self.tz).time().strftime('%H:%M')}】",
                    color=discord.Color.orange()
                )
                '''
                if days_left > 0 and days_left <= len(days_str):
                    embed.add_field(name="", value=f"屯懸賞第 {days_str[days_left-1]} 天！", inline=False)
                    await channel.send(file=discord.File("./wanted2.jpg"))
                elif days_left == 0:
                    embed.add_field(name="🎉 今天「維修前」掃蕩懸賞", value="懸賞維修前掃光光\n哼！哼！啊啊啊啊啊！", inline=False)
                    await channel.send(file=discord.File("./wanted2.jpg"))
                '''
                
                await channel.send(embed=embed)
                await channel.send(file=discord.File("./3am.gif"))
        
    @commands.command(name='test_everyday')
    async def test_everyday(self, ctx):
        test_channel_ids = [1300828046131200081]
        await self.send_everyday_message(test_channel_ids)
        await ctx.send("✅ 測試訊息已發送！")


bot_token = os.environ['TOKEN']
keep_alive.keep_alive()
bot.run(bot_token)


