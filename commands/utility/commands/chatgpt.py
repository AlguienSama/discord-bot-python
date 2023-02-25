import os
import openai
import json

chatgpt_history = './utils/ddbb/chatgpt.json'

async def openai_chatgpt(ctx, prompt):
    msg = await ctx.send('Pensando una respuesta, espera un momento...')

    prompt_history = {}
    server_history = ''
    channel_id = str(ctx.channel.id)
    try:
        with open(chatgpt_history,"r",encoding="utf-8") as file:
            prompt_history = json.load(file)
            server_history = '\n'.join(prompt_history[channel_id])
    except:
        open(chatgpt_history, "w")
        prompt_history[channel_id] = []
    openai.api_key = os.getenv("OPENAI_API")

    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=f"{prompt}",
        context=f"{server_history}",
        temperature=0.9,
        max_tokens=500,
        top_p=1,
        frequency_penalty=0.0,
        presence_penalty=0.6,
        stop=[" Human:", " AI:"]
    )

    answer = response.choices[0].text.strip()

    if answer == '':
        return await msg.edit(content="Error, vuelve a preguntar de nuevo")

    prompt_history[channel_id].append(prompt)
    prompt_history[channel_id].append(answer)

    #eliminar elementos que excedan x numero#
    if len(prompt_history[channel_id]) >= 8:
        del prompt_history[channel_id][:2]

    #guardar#
    with open(chatgpt_history, 'w',encoding="utf-8") as file:
        json.dump(prompt_history, file, indent=4)

    return await msg.edit(content=answer)