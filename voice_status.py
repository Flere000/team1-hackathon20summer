# インストールした discord.py を読み込む
import discord
from datetime import datetime, timedelta
import datetime
pretime_dict = {}

# 自分のBotのアクセストークンに置き換えてください
TOKEN = ''
TEXT_CHANNEL =  # テキストチャットのチャンネルID

# 接続に必要なオブジェクトを生成
client = discord.Client()
text_chat = discord.Object(id=TEXT_CHANNEL)

# 起動時に動作する処理
@client.event
async def on_ready():
    # 起動したらターミナルにログイン通知が表示される
    print('ログインしましたやったね')

    """

# メッセージ受信時に動作する処理
@client.event
async def on_message(message):
    # メッセージ送信者がBotだった場合は無視する
    if message.author.bot:
        return
    # 「/neko」と発言したら「にゃーん」が返る処理
    if message.content == '/neko1':
        await message.channel.send('にゃーん1')

        """


#メンバーがテキストを打った時に実行されるイベントハンドラ
@client.event
async def on_message(message):
    if message.author.bot:
           return
    # 「おはよう」で始まるか調べる
    if message.content.startswith("おはよう"):
            # メッセージを書きます
            m = "おはよう" + message.author.name + "さん！"
            # メッセージが送られてきたチャンネルへメッセージを送ります
            await message.channel.send(m)


@client.event
async def on_voice_state_update(member,before,after):
   if member.guild.id == サーバID and (before.channel != after.channel):
          now = datetime.datetime.utcnow() + timedelta(hours=9)
          alert_channel = client.get_channel(サーバID)
          if before.channel is None:#入室
              msg = f'{now:%m/%d-%H:%M}に{member.name} が {after.channel.name} にやってきたぞ!'
              pretime_dict[member.name] = datetime.datetime.now()
              await alert_channel.send(msg)
          elif after.channel is None:#退出
              duration_time = pretime_dict[member.name] - datetime.datetime.now()
              duration_time_adjust = int(duration_time.total_seconds()) * -1
              min=int(duration_time_adjust/60)
              s=duration_time_adjust%60
              #msg = f' {now:%m/%d-%H:%M}に{member.name} が たった{str(duration_time_adjust)}秒で{before.channel.name} から帰ってしまった...。'
              msg = f' {now:%m/%d-%H:%M}に{member.name} が たった{str(min)}分{str(s)}秒で{before.channel.name} から帰ってしまった...。'
              await alert_channel.send(msg)

# Botの起動とDiscordサーバーへの接続
client.run(TOKEN)