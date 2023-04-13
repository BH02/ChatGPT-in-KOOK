from khl import Bot, Message
import openai
import yaml
import os

# KOOK机器人
bot = Bot(token='KOOK_BOT_TOKEN')

# ChatGPT
openai.api_key = 'OPENAI_API_KEY'


# /gpt 发送聊天内容 /gpt own 则是专属于单个用户的聊天
@bot.command(regex=r'[\s\S]*')
async def gpt(msg: Message):
    if '/gpt' in msg.content:

        # 检查是否是用户专属的聊天
        specified = True if 'own' in msg.content else False

        # 拿到发消息的用户id，不是专属聊天就拿频道id
        ChatID = msg.extra['author']['id'] if specified else msg.target_id
        # 指定聊天记录文件的路径
        ChatFile = f'ChatRecord/chat-{ChatID}.yaml'

        # 判断是否存在旧的聊天记录，有则读取，无则新建
        if os.path.exists(ChatFile):
            with open(ChatFile, 'r', encoding='utf-8') as getTalk:
                data = yaml.safe_load(getTalk)

                # 新建的文件获取到的getTal会为空，需要处理一下
                talk = data if data else []
        else:
            # 新建文件
            os.mknod(ChatFile)
            talk = []

        # 去除指令内容，更美观
        chat = msg.content.replace('/gpt ', '').replace('own', '')
        LatestChat = {"role": "user", "content": chat}

        # 存入ChatRecord
        ChatRecord = talk if len(talk) < 20 else talk[-20:]

        # 往聊天记录添加刚收到的消息
        ChatRecord.append(LatestChat)

        # 调用API
        completion = openai.ChatCompletion.create(model="gpt-3.5-turbo",
                                                  messages=ChatRecord)

        # 回复信息
        await msg.reply(completion.choices[0].message.content)

        # 往聊天记录文件里追加最新的消息
        with open(ChatFile, 'a', encoding='utf-8') as writeTalk:
            yaml.dump([LatestChat], writeTalk, allow_unicode=True, default_flow_style=False)


bot.run()
