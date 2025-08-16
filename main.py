import os
import discord 
import datetime as dt
from datetime import timedelta
from discord.ext import tasks, commands
import keep_alive
from fb_helper import *
import asyncio

intents = discord.Intents.default()
intents.message_content = True  # 正確方式
bot = commands.Bot(command_prefix="!", intents=intents)

ALLOWED_GUILD_IDs = [1300828046131200081, 1192478035966951606]

@bot.event
async def on_ready():
    await bot.add_cog(TaskTime(bot))
    #await bot.add_cog(TaskTimes(bot))
    print(f"目前登入身份 --> {bot.user}")
'''
@bot.event
async def on_message(message):
    # 忽略bot自己的訊息
    if message.author == bot.user:
        return
    
    # 限制只在指定群組使用
    if message.guild and message.guild.id != ALLOWED_GUILD_ID:
        return
    
    # 檢查Facebook連結
    urls = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', message.content)
    fb_urls = [url for url in urls if is_facebook_url(url)]
    
    if fb_urls:
        await handle_facebook_video(message, fb_urls[0])
    
    await bot.process_commands(message)
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
    
    await handle_facebook_video(ctx.message, url, delete_original=False)
    await asyncio.sleep(2)  # 等待Discord載入內嵌
    try:
        # 重新取得訊息以獲取最新的embeds
        fresh_message = await ctx.channel.fetch_message(ctx.message.id)
        
        # 如果有Discord自動產生的embeds，就編輯訊息移除它們
        if fresh_message.embeds:
            # 保留訊息內容但移除embeds
            await fresh_message.edit(content=fresh_message.content, embeds=[], suppress=True)
    except discord.Forbidden:
        print("沒有權限修改訊息")
    except discord.NotFound:
        print("訊息已被刪除")
    except Exception as e:
        print(f"處理內嵌時發生錯誤: {e}")

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
            dt.time(hour = i, minute = j, tzinfo = dt.timezone(timedelta(hours = 8)))
            for i in range(24) for j in range(0,60,2)
    ]
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.every_hour.start()
        self.tz = dt.timezone(timedelta(hours = 8))
        
    @tasks.loop(time = every_hour_time)
    async def every_hour(self):
        channel_id = 1300828046131200081
        channel = self.bot.get_channel(channel_id)

        today = dt.datetime.now(tz=self.tz).date()
        target_date = dt.date(today.year, 5, 14)

        # 計算倒數天數
        days_left = (target_date - today).days
        
        if channel:
            embed = discord.Embed(
                title = "🛏 洞三洞洞 部隊起床",
                description = f"🕛 現在時間 【{dt.datetime.now(tz = self.tz).time().strftime('%H:%M')}】", 
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
