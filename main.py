import discord
import config, requests, json, random

client = discord.Client()

def get_quote():
    response = requests.get("https://zenquotes.io/api/random")
    json_data = json.loads(response.text)
    quote = json_data[0]['q'] + " -" + json_data[0]['a']
    return(quote)

def get_cases():
    response = requests.get(config.COVID_API)
    json_data = json.loads(response.text)
    x = 0
    while json_data[x]['country'] != 'India':
        x = x + 1
    stats = [json_data[x]['infected'],json_data[x]['recovered'],json_data[x]['deceased']]
    return stats

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    msg = message.content.lower()
    if message.author == client.user:
        return

    #Intro texts
    for x in config.INTRO_ENGLISH:
        if msg.startswith(x):
            await message.channel.send(random.choice(config.REPLY_ENGLISH))
            return

    # Inspirational texts
    if msg.startswith('inspire'):
        quote = get_quote()
        await message.channel.send(quote)
        return

    # Corona information
    if any(word in msg for word in config.COVID_WORDS):
        await message.channel.send('Let me enlighten you with some stats from INDIA')
        info = get_cases()
        await message.channel.send("Total cases: " + str(info[0]) + ", Recovered cases: " + str(info[1]) + ", Deceased: " + str(info[2]))
        await message.channel.send('How about that?!')
        return

    # For other inputs
    else:
        await message.channel.send('Sorry, my abilities are limited since I am a bot. Ask me something else')

client.run(config.TOKEN)