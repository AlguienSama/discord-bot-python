import requests
import json


async def colorizer(ctx, link):
    r = requests.post(
        "https://api.deepai.org/api/colorizer",
        data={
            'image': link,
        },
        headers={'api-key': '1e7d5e87-a067-48ce-b193-f8b37d8983b5'}
    )

    return await ctx.send(content=r.json()['output_url'])


async def super_resolution(ctx, link):
    r = requests.post(
        "https://api.deepai.org/api/torch-srgan",
        data={
            'image': link,
        },
        headers={'api-key': '1e7d5e87-a067-48ce-b193-f8b37d8983b5'}
    )

    return await ctx.send(content=r.json()['output_url'])


async def waifu2x(ctx, link):
    r = requests.post(
        "https://api.deepai.org/api/waifu2x",
        data={
            'image': link,
        },
        headers={'api-key': '1e7d5e87-a067-48ce-b193-f8b37d8983b5'}
    )

    return await ctx.send(content=r.json()['output_url'])


async def text_to_image(ctx, args):
    texto = " ".join(args)

    r = requests.post(
        "https://api.deepai.org/api/text2img",
        data={
            'text': texto,
        },
        headers={'api-key': '1e7d5e87-a067-48ce-b193-f8b37d8983b5'}
    )

    return await ctx.send(content=r.json()['output_url'])


async def toonify(ctx, link):
    r = requests.post(
        "https://api.deepai.org/api/toonify",
        data={
            'image': link,
        },
        headers={'api-key': '1e7d5e87-a067-48ce-b193-f8b37d8983b5'}
    )

    return await ctx.send(content=r.json()['output_url'])