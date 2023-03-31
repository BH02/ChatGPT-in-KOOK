from khl import Bot, Message
import openai
import yaml

# KOOK机器人
bot = Bot(token='KOOK_BOT_TOKEN')

# ChatGPT
openai.api_key = 'OPENAI_API_KEY'

# 读取本地聊天记录
with open('conversation.yaml', 'r', encoding='utf-8') as getTalk:
    talk = list(yaml.safe_load_all(getTalk))[0]

    # 存入ChatRecord
    ChatRecord = talk if len(talk) < 20 else talk[-20:]


@bot.command(regex=r'[\s\S]*')
async def chatgpt(msg: Message):
    # 判断消息是否属于指定频道且@了机器人
    # 频道列表需要自己设置，或者存在config中 ChannelList = ['TEST_CHANNEL','HAVE_FUN']
    # if msg.extra["channel_name"] in ChannelList and 'BOT_ID' in msg.extra['mention']:

    # 去除消息中@机器人的部分
    chat = msg.content.replace('(met)BOT_ID(met) ', '')

    latestchat = {"role": "user", "content": chat}

    # 往聊天记录添加刚收到的消息
    ChatRecord.append(latestchat)

    # 调用API
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=ChatRecord
    )

    # 机器人以回复的形式发送消息
    await msg.reply(completion.choices[0].message.content)

    # 往聊天记录文件里追加最新的消息
    with open('conversation.yaml', 'a', encoding='utf-8') as writeTalk:
        yaml.dump([latestchat], writeTalk, allow_unicode=True)


bot.run()
