# Codado por Sierra

import discord, re, random, os, dotenv
from tabulate import tabulate

intents = discord.Intents.default()
intents.message_content = True

dotenv.load_dotenv(dotenv.find_dotenv())
tk = os.getenv('TOKEN')

client = discord.Client(intents=intents)

class Dice:

    dds_sort = []

    @staticmethod
    def roll(n_dds, dd):

        Dice.dds_sort = []

        for _ in range(n_dds):
            dice = random.randint(1, dd)
            Dice.dds_sort.append(dice)

class Msg_format:
    
    msg = ''
    
    @staticmethod
    def msg_format(n_dds, dd):

        dds_sort = Dice.dds_sort
        header1 = [f"{n_dds}d{dd}", "rolls", "sum"]
        cache_sum = 0
        num_dice = 0

        data = []

        for item in dds_sort:
            cache = []
            cache_sum += item
            num_dice += 1
            cache.append(f"{num_dice}º")
            cache.append(item)
            cache.append(cache_sum)
            data.append(cache)
        
        Msg_format.msg = tabulate(data, headers=header1, tablefmt='fancy_grid')


@client.event
async def on_ready():
    print('Foi Porra!!!!')

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    pattern = r'(\d+)d(\d+)'
    
    match = re.search(pattern, message.content)
    
    if match:
        n_dds = int(match.group(1))
        dd = int(match.group(2))

        if n_dds > 50:
            await message.channel.send('Desculpe, número de dados não suportado ;-;')
            await message.channel.send('O número limite de dados é 50 por vez!')
        
        else:
            Dice.roll(n_dds, dd)
            Msg_format.msg_format(n_dds, dd)
            
            await message.channel.send(f"```\n{Msg_format.msg}\n```")

client.run(tk)