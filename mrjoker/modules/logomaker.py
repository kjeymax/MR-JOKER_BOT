from mrjoker.events import register
from mrjoker import OWNER_ID
from mrjoker import telethn as tbot
import os 
from PIL import Image, ImageDraw, ImageFont

@register(pattern="^/ylogo ?(.*)")
async def lego(event):
 quew = event.pattern_match.group(1)
 if event.sender_id == OWNER_ID:
     pass
 else:
     
    if not quew:
       await event.reply('Provide Some Text To Draw!')
       return
    else:
       pass
 await event.reply('Creating your logo...wait!🤡')
 try:
    text = event.pattern_match.group(1)
    img = Image.open('./mrjoker/pack/blackimg.jpg')
    draw = ImageDraw.Draw(img)
    image_widthz, image_heightz = img.size
    pointsize = 500
    fillcolor = "gold"
    shadowcolor = "blue"
    font = ImageFont.truetype("./mrjoker/pack/Knife.otf", 1000)
    w, h = draw.textsize(text, font=font)
    h += int(h*0.21)
    image_width, image_height = img.size
    draw.text(((image_widthz-w)/2, (image_heightz-h)/2), text, font=font, fill=(255, 255, 255))
    x = (image_widthz-w)/2
    y= ((image_heightz-h)/2+6)
    draw.text((x, y), text, font=font, fill="yellow", stroke_width=25, stroke_fill="white")
    fname2 = "LogoMakeBy_MRJOKER.png"
    img.save(fname2, "png")
    await tbot.send_file(event.chat_id, fname2, caption="🤡")
    if os.path.exists(fname2):
            os.remove(fname2)
 except Exception as e:
   await event.reply(f'Error Report @lkhitech, {e}')



   
@register(pattern="^/jlogo ?(.*)")
async def lego(event):
 quew = event.pattern_match.group(1)
 if event.sender_id == OWNER_ID:
     pass
 else:
     
    if not quew:
       await event.reply('Provide Some Text To Draw!')
       return
    else:
       pass
 await event.reply('Creating your logo...wait!🤡')
 try:
    text = event.pattern_match.group(1)
    img = Image.open('./mrjoker/pack/fjoker.jpg')
    draw = ImageDraw.Draw(img)
    image_widthz, image_heightz = img.size
    pointsize = 500
    fillcolor = "white"
    shadowcolor = "blue"
    font = ImageFont.truetype("./mrjoker/pack/Gothic-Joker.ttf", 500)
    w, h = draw.textsize(text, font=font)
    h += int(h*0.21)
    image_width, image_height = img.size
    draw.text(((image_widthz-w)/2, (image_heightz-h)/2), text, font=font, fill=(148, 0, 211))
    x = (image_widthz-w)/2
    y= ((image_heightz-h)/2+6)
    draw.text((x, y), text, font=font, fill="white", stroke_width=0, stroke_fill="DarkViolet")
    fname2 = "LogoMakeBy_MRJOKER.png"
    img.save(fname2, "png")
    await tbot.send_file(event.chat_id, fname2, caption="🤡")
    if os.path.exists(fname2):
            os.remove(fname2)
 except Exception as e:
   await event.reply(f'Error Report @lkhitech, {e}')

   
@register(pattern="^/blogo ?(.*)")
async def lego(event):
 quew = event.pattern_match.group(1)
 if event.sender_id == OWNER_ID:
     pass
 else:
     
    if not quew:
       await event.reply('Provide Some Text To Draw!')
       return
    else:
       pass
 await event.reply('Creating your logo...wait!🤡')
 try:
    text = event.pattern_match.group(1)
    img = Image.open('./mrjoker/pack/2.jpg')
    draw = ImageDraw.Draw(img)
    image_widthz, image_heightz = img.size
    pointsize = 500
    fillcolor = "PaleGreen"
    shadowcolor = "blue"
    font = ImageFont.truetype("./mrjoker/pack/Maghrib.ttf", 800)
    w, h = draw.textsize(text, font=font)
    h += int(h*0.21)
    image_width, image_height = img.size
    draw.text(((image_widthz-w)/2, (image_heightz-h)/2), text, font=font, fill=(65, 105, 225))
    x = (image_widthz-w)/2
    y= ((image_heightz-h)/2+6)
    draw.text((x, y), text, font=font, fill="DarkMagenta", stroke_width=0, stroke_fill="Gainsboro")
    fname2 = "LogoMakeBy_MRJOKER.png"
    img.save(fname2, "png")
    await tbot.send_file(event.chat_id, fname2, caption="🤡")
    if os.path.exists(fname2):
            os.remove(fname2)
 except Exception as e:
   await event.reply(f'Error Report @lkhitech, {e}')   
   
   
   
   
   
file_help = os.path.basename(__file__)
file_help = file_help.replace(".py", "")
file_helpo = file_help.replace("_", " ")


__help__ = """
 🔹 /jlogo <text> :  Create your logo with your name
 🔹 /ylogo <text> :  Create your logo with your name
 🔹 /blogo <text> :  Create your logo with your name
 """
__mod_name__ = "Logo 🖼"
