import discord
import yt_dlp
import re

def is_facebook_url(url):
    """檢查是否為Facebook影片連結"""
    fb_patterns = [
        r'facebook\.com/.*?/videos/',
        r'facebook\.com/watch',
        r'facebook\.com/share/v/',
        r'facebook\.com/share/r/',
        r'facebook\.com/share/',
        r'fb\.watch',
        r'm\.facebook\.com/.*?/videos/',
        r'facebook\.com/.*?/posts/.*?',
        r'facebook\.com/reel/'
    ]
    return any(re.search(pattern, url, re.IGNORECASE) for pattern in fb_patterns)

async def get_video_info(url):
    """取得影片資訊（最佳化版本）"""
    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
        'extract_flat': False,
        'skip_download': True,
        'writeinfojson': False,
        'writesubtitles': False,
        'writeautomaticsub': False,
        # 最佳化：只取得需要的資訊
        'extract_comments': False,
        'extract_chapters': False,
        'extract_subtitles': False,
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            # 只回傳需要的欄位，減少記憶體使用
            return {
                'title': info.get('title'),
                'thumbnail': info.get('thumbnail'),
                'duration': info.get('duration')
            }
    except Exception as e:
        print(f"取得影片資訊失敗: {e}")
        return None

def format_duration(seconds):
    """格式化影片時長"""
    if not seconds:
        return "未知"
    
    try:
        seconds = int(float(seconds))
        minutes = seconds // 60
        seconds = seconds % 60
        return f"{minutes}:{seconds:02d}"
    except:
        return "未知"

async def handle_facebook_video(message, url, delete_original=False):
    """處理Facebook影片（簡化版）"""
    
    # 簡化載入訊息
    loading_msg = await message.reply("🔍 載入中...")
    
    try:
        # 取得影片資訊
        video_info = await get_video_info(url)
        
        if not video_info or not video_info.get('title'):
            await loading_msg.edit(content="❌ 無法載入影片資訊")
            return
        
        # 建立簡化embed
        embed = discord.Embed(
            color=0x1877f2
        )
        
        # 影片標題
        title = video_info.get('title', '無標題')
        if len(title) > 100:
            title = title[:97] + "..."
        embed.title = f"📺 {title}"
        
        # 時長
        duration = video_info.get('duration')
        if duration:
            embed.description = f"⏱️ {format_duration(duration)}"
        
        # 縮圖
        thumbnail = video_info.get('thumbnail')
        if thumbnail:
            embed.set_image(url=thumbnail)
        
        # 前往FB按鈕（使用field模擬按鈕）
        embed.add_field(
            name="🔗",
            value=f"[前往 Facebook 觀看]({url})",
            inline=False
        )
        
        # 更新訊息
        await loading_msg.edit(content="", embed=embed)
        
        # 刪除原始訊息（如果是指令調用）
        if delete_original:
            try:
                await message.delete()
            except discord.Forbidden:
                print("沒有權限刪除訊息")
            except discord.NotFound:
                print("訊息已被刪除")
                
    except Exception as e:
        print(f"處理影片時發生錯誤: {e}")
        await loading_msg.edit(content="❌ 處理失敗")


