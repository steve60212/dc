import time, discord, datetime
# 導入discord.ext模組中的tasks工具
from discord.ext import tasks, commands
import os
import keep_alive
intents = discord.Intents.all()
bot = commands.Bot(command_prefix = "$", intents = intents)

@bot.event
async def on_ready():
    await bot.add_cog(TaskTime(bot))
    print(f"目前登入身份 --> {bot.user}")

class TaskTime(commands.Cog):
    # 臺灣時區 UTC+8
    tz = datetime.timezone(datetime.timedelta(hours = 8))
    # 設定每日十二點執行一次函式
    everyday_time = datetime.time(hour = 11, minute = 28, tzinfo = tz)

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.everyday.start()

    # 每日十二點發送 "晚安!瑪卡巴卡!" 訊息
    @tasks.loop(time = everyday_time)
    async def everyday(self):
        # 設定發送訊息的頻道ID
        channel_id = 1300828046131200081
        channel = self.bot.get_channel(channel_id)
        embed = discord.Embed(
            title = "🛏 洞三洞洞 部隊起床",
            description = f"🕛 現在時間 {datetime.date.today()} 03:00",
            color = discord.Color.orange()
        )
        await channel.send(embed = embed)

bot_token = os.getenv("DC_bot_token")
keep_alive.keep_alive()
bot.run(bot_token)