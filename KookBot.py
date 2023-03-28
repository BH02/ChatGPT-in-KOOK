from khl import Bot, Message
import openai

#KOOK机器人
bot = Bot(token='KOOK_BOT_TOKEN')

#ChatGPT
openai.api_key = 'OPENAI_API_KEY'
GPTmessage = []

@bot.command(regex=r'[\s\S]*')
async def chatgpt(msg:Message):
    GPTmessage.append(
      {
        "role": "user",
        "content": msg.content
      }
    )
    completion = openai.ChatCompletion.create(
      model="gpt-3.5-turbo",
      messages=GPTmessage
     )

    #机器人以回复的形式发送消息
    await msg.reply(completion.choices[0].message.content)

bot.run()