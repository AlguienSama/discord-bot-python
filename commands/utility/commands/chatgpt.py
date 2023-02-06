import os
import openai

async def openai_chatgpt(ctx, prompt): 
    openai.api_key = os.getenv("OPENAI_API")
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=0.9,
        max_tokens=500,
        top_p=1,
        frequency_penalty=0.0,
        presence_penalty=0.6,
        stop=[" Human:", " AI:"]
    )

    answer = response.choices[0].text.strip()
    return await ctx.send(content=answer)