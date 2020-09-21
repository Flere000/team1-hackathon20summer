#Discord.pyとGoogle Cloud Text-to-Speech APIを使った読み上げbotです。
#コード実行の際はBotの登録、Discord.pyやGoogle Cloud SDKのインポート、プロジェクトのJSONファイルを環境変数に通すなど最低限の設定は済ませておいてください。

import discord
import html
from discord.channel import VoiceChannel
from discord.player import FFmpegPCMAudio
from google.cloud import texttospeech

TOKEN = 'YOUR BOT TOKEN'
SERVER_ID = 'YOUR SERVER ID(type: int)'
client = discord.Client()
isConnect = False
part = 0

exclusive_extension = {
    '.png',
    '.jpg',
    '.jpeg',
    '.gif',
    '.tiff',
    '.bmp',
    '.svg',
    '.pict',
    '.mp3',
    '.wav',
    '.aac',
    '.flac',
    '.aiff',
    '.alac',
    '.m4a',
    '.ogg',
    '.mp4',
    '.avi',
    '.mov',
    '.mkv',
}

voiceChannel: VoiceChannel 

@client.event
async def on_ready():
    print('Login!!!')
    print('----------')

@client.event
async def on_message(message):
    global voiceChannel
    global isConnect
    if message.author.bot:
        return
    if message.content.startswith('!'):
        if message.content == '!close':
            await client.close()
            return
        elif message.content == '!connect':
            voiceChannel = await discord.VoiceChannel.connect(message.author.voice.channel)
            await message.channel.send('接続しました')
            return
        elif message.content == '!disconnect':
            voiceChannel.stop()
            await voiceChannel.disconnect()
            return
        else:
            await message.channel.send('コマンドが違います')
            return
    if voiceChannel.is_connected:
        if isConnect == False:
            isConnect = True
            return
        print(message.content)
        for i in exclusive_extension:
            if (message.content.endswith(i)):
                return 
        if message.content.startswith('http'):
            play_voice('uRL省略')
            return

        play_voice(message.content)

def text_to_ssml(text):
    escaped_lines = html.escape(text)
    ssml = "{}".format(
        escaped_lines.replace("\n", '\n<break time="1s"/>')
    )
    return ssml

def ssml_to_speech(text, file):
    ttsClient = texttospeech.TextToSpeechClient()
    synthesis_input = texttospeech.SynthesisInput(text=text)
    voice = texttospeech.VoiceSelectionParams(
        language_code="ja-JP", ssml_gender=texttospeech.SsmlVoiceGender.MALE
    )
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )
    response = ttsClient.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )
    with open(file, "wb") as out:
        out.write(response.audio_content)
        print("Audio content written to file " + file)
    return file

def play_voice(text):
    ssml = text_to_ssml(text)
    file = ssml_to_speech(ssml, "voice.mp3")
    voiceChannel.play(FFmpegPCMAudio(file))

client.run(TOKEN)