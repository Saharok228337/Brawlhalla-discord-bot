import discord, requests
import os
from dotenv import load_dotenv
from discord.ext import commands
from discord import app_commands
from discord.utils import MISSING

load_dotenv()

class Client(commands.Bot):
    async def on_ready(self):
        print(f'Logged on as {self.user}!')

        try:
            guild = discord.Object(id=1349772694685749299)
            synced = await self.tree.sync(guild=guild)
            print(f'Synced {len(synced)} commands to guild {guild.id}')
        except Exception as e:
            print(f'Error syncing commands: {e}')

    async def on_message(self, message):
        if message.author == self.user:
            return

        if message.content.startswith('SBot'):
            await message.channel.send(f'Hello {message.author}!')
        

intents = discord.Intents.default()
intents.message_content = True
client = Client(command_prefix='!', intents=intents)


GUILD_ID = discord.Object(id=1349772694685749299)



@client.tree.command(name='brawlhalla', description='Дізнайся статистику гравця в бравлхалла', guild=GUILD_ID)
async def add(interaction: discord.Interaction, brawlhalla_id: int):
    await interaction.response.defer()

    url = 'https://api.brawlhalla.com/v1/player/stats'
    url2v2 = 'https://api.brawlhalla.com/v1/player/teams'
    urlG = 'https://api.brawlhalla.com/v1/player/guild'
    urlL = 'https://api.brawlhalla.com/v1/static/legends'

    query_params = {"brawlhalla_id": brawlhalla_id}
    response = requests.get(url, params=query_params)

    query_params1v1 = {"brawlhalla_id": brawlhalla_id, 'mode': 'ranked_1v1'}
    response1v1 = requests.get(url, params=query_params1v1)

    response2v2 = requests.get(url2v2, params=query_params)

    query_params3v3 = {"brawlhalla_id": brawlhalla_id, 'mode': 'ranked_3v3'}
    response3v3 = requests.get(url, params=query_params3v3)

    responseG = requests.get(urlG, params=query_params)

    if response.status_code != 200:
        await interaction.followup.send(f'Щось пішло не так. Код помилки: {response.status_code}')

    if response.status_code == 200:
        data = response.json()
        max_games = 0
        favourite = None

        for legend in data["legends"]:
            if legend["games"] > max_games:
                max_games = legend["games"]
                favourite = legend

        query_paramsL = {'filter_by_id': favourite['legend_id']}
        responseL = requests.get(urlL, params=query_paramsL)
        dataL = responseL.json()

    if response1v1.status_code == 200:
        data1v1 = response1v1.json()
        max_elo = 0
        best = None

        for legend in data1v1["legends"]:
            if legend["rating"] > max_elo:
                max_elo = legend["rating"]
                best = legend

        query_paramsL1 = {'filter_by_id': best['legend_id']}
        responseL1 = requests.get(urlL, params=query_paramsL1)
        dataL1 = responseL1.json()  

    if response2v2.status_code == 200:
        data2v2 = response2v2.json()
        max_elo = 0
        Bteam = None
        max_games = 0
        Bteam2 = None

        for team in data2v2["teams"]['ranked_2v2']:
            if int(team["rating"]) > max_elo:
                max_elo = team["rating"]
                Bteam = team

            if int(team["games"]) > max_games:
                max_games = team["games"]
                Bteam2 = team       

    if response1v1.status_code == 200 and data1v1.get('tier'):
        if data1v1['tier'].startswith("Tin"):
            color = discord.Color.dark_green()
        elif data1v1['tier'].startswith("Bronze"):
            color = discord.Color.dark_orange()
        elif data1v1['tier'].startswith("Silver"):
            color = discord.Color.light_gray()
        elif data1v1['tier'].startswith("Gold"):
            color = discord.Color.gold()
        elif data1v1['tier'].startswith("Platinum"):
            color = discord.Color.blue()
        elif data1v1['tier'].startswith("Diamond"):
            color = discord.Color.purple()
        elif data1v1['tier'].startswith("Valhallan"):
            color = discord.Color.blurple()
    elif response2v2.status_code == 200 and Bteam.get('tier'):
        if Bteam['tier'].startswith("Tin"):
            color = discord.Color.dark_green()
        elif Bteam['tier'].startswith("Bronze"):
            color = discord.Color.dark_orange()
        elif Bteam['tier'].startswith("Silver"):
            color = discord.Color.light_gray()
        elif Bteam['tier'].startswith("Gold"):
            color = discord.Color.gold()
        elif Bteam['tier'].startswith("Platinum"):
            color = discord.Color.blue()
        elif Bteam['tier'].startswith("Diamond"):
            color = discord.Color.purple()
        elif Bteam['tier'].startswith("Valhallan"):
            color = discord.Color.blurple()
    else:
        color = discord.Color.dark_gray()

    if response1v1.status_code == 200 and data1v1.get('tier') is None:
        await interaction.followup.send('Щось пішло не так')

    if response2v2.status_code == 200 and Bteam.get('tier') is None:
        await interaction.followup.send('Щось пішло не так')

    if response2v2.status_code == 200 and Bteam2.get('tier') is None:
        await interaction.followup.send('Щось пішло не так')

    print(response.status_code)
    if response.status_code == 200:
        embed = discord.Embed(title=f'Статистика {data['name']}', description=f'*ID: {brawlhalla_id}*', color=color)
        embed.set_author(name='Saharok', url='https://www.youtube.com/@sahar_is_real', icon_url='https://yt3.googleusercontent.com/MeVCIqlkHHGMGvrJPuXJwTbxBldWdb9NK85V4apSg7y_IwgJYdNg-pgP2uCI3m8SW1j1MhTqn74=s160-c-k-c0x00ffffff-no-rj')
        embed.set_thumbnail(url='https://static.wikia.nocookie.net/brawlhalla_gamepedia/images/1/14/Brawlhalla_Logo_100M_Full.png/revision/latest/scale-to-width-down/340?cb=20230520001004')
        embed.add_field(name=f'ІГРИ', value=f'Зіграно ігор: {data['games']}\nПеремог: {data['wins']}\nПоразок: {data['games'] - data['wins']}', inline=False)
        embed.add_field(name=f'Улюблений персонаж: {dataL['legends'][0]['legend_name']}', value=f'Ігор зіграно: {favourite['games']}\nПеремог: {favourite['wins']}\nПоразок: {favourite['games'] - favourite['wins']}\n{favourite['ko_weapon_one']} вбивств за {dataL['legends'][0]['weapon_one']}\n{favourite['ko_weapon_two']} вбивств за {dataL['legends'][0]['weapon_two']}', inline=False)
    if response1v1.status_code == 200:
        embed.add_field(name=f'RANKED 1v1', value=f'{data1v1['games']} ігор зіграно ({data1v1['wins']} перемог | {data1v1['games'] - data1v1['wins']} поразок)\nРанг: {data1v1['tier']}\nElo: {data1v1['rating']}\nPeak Elo: {data1v1['peak_rating']}\nНайкращий персонаж в цьому сезоні: **{dataL1['legends'][0]['legend_name']}** (elo: {best['rating']})\n{data1v1['global_rank']}th місце в світі\n{data1v1['region_ranks'][0]['rank']}th місце в {data1v1['region_ranks'][0]['region']}', inline=False)
    if response2v2.status_code == 200:
        embed.add_field(name=f'RANKED 2v2', value=f'**{Bteam['username_one']} і {Bteam['username_two']}**\n*Найкраща команда за ELO*\n{Bteam['games']} ігор зіргано ({Bteam['wins']} перемог | {Bteam['games'] - Bteam['wins']} поразок)\nРанг: {Bteam['tier']}\nElo: {Bteam['rating']}\nPeak Elo: {Bteam['peak_rating']}\n{Bteam['global_rank']}th місце в світі\n{Bteam['region_ranks'][0]['rank']}th місце в {Bteam['region_ranks'][0]['region']}', inline=False)
        if Bteam != Bteam2:
            embed.add_field(value=f'**{Bteam2['username_one']} і {Bteam2['username_two']}**\n*Найкраща команда за кількістю ігор*\n{Bteam2['games']} ігор зіргано ({Bteam2['wins']} перемог | {Bteam2['games'] - Bteam2['wins']} поразок)\nРанг: {Bteam2['tier']}\nElo: {Bteam2['rating']}\nPeak Elo: {Bteam2['peak_rating']}\n{Bteam2['global_rank']}th місце в світі\n{Bteam2['region_ranks'][0]['rank']}th місце в {Bteam2['region_ranks'][0]['region']}', inline=False)
    if response3v3.status_code == 200:
        data3v3 = response3v3.json()
        embed.add_field(name=f'RANKED 3v3', value=f'{data3v3['games']} ігор зіграно ({data3v3['wins']} перемог | {data3v3['games'] - data3v3['wins']} поразок)\nРанг: {data3v3['tier']}\nElo: {data3v3['rating']}\nPeak Elo: {data3v3['peak_rating']}\n{data3v3['global_rank']}th місце в світі\n{data3v3['region_ranks'][0]['rank']}th місце в {data3v3['region_ranks'][0]['region']}', inline=False)
    if responseG.status_code == 200:
        dataG = responseG.json()
        embed.set_footer(text=f'Знаходиться в клані {dataG['guild']['guild_name']}\nid: {dataG['guild']['guild_id']}')
    if responseG.status_code != 200:
        embed.set_footer(text=f'Поки без клану')
    if response.status_code == 200:
        await interaction.followup.send(embed=embed)



@client.tree.command(name='guild', description='Дізнайся статистику клана в бравлхалла', guild=GUILD_ID)
async def add(interaction: discord.Interaction, guild_id: int):
    await interaction.response.defer()

    urlGl = 'https://api.brawlhalla.com/v1/guild/stats'
    urlGm = 'https://api.brawlhalla.com/v1/guild/members'

    query_paramsG = {"guild_id": guild_id}
    responseGl = requests.get(urlGl, params=query_paramsG)
    responseGm = requests.get(urlGm, params=query_paramsG)

    print(responseGl.status_code)

    if responseGl.status_code != 200:
        await interaction.response.send_message(f'Щось пішло не так. Код помилки: {responseGl.status_code}')

    if responseGl.status_code == 200:
        dataGl = responseGl.json()
        dataGm = responseGm.json()

        embed = discord.Embed(title=f'{dataGl['name']}', description=f'\"{dataGl['notice']}\"', color=discord.Color.green())
        embed.set_thumbnail(url='https://static.wikia.nocookie.net/brawlhalla_gamepedia/images/1/14/Brawlhalla_Logo_100M_Full.png/revision/latest/scale-to-width-down/340?cb=20230520001004')
        embed.set_footer(text=f'ID: {dataGl['guild_id']}')
        embed.set_author(name='Saharok', url='https://www.youtube.com/@sahar_is_real', icon_url='https://yt3.googleusercontent.com/MeVCIqlkHHGMGvrJPuXJwTbxBldWdb9NK85V4apSg7y_IwgJYdNg-pgP2uCI3m8SW1j1MhTqn74=s160-c-k-c0x00ffffff-no-rj')
        embed.add_field(name='ІНФОРМАЦІЯ', value=f'Guild Points: {dataGl['guild_points']}\nXP: {dataGl['xp']}', inline=False)
        if 'rank' in dataGl:
            embed.add_field(name='', value=f'\nРАНГ: {dataGl['rank']}', inline=False)

        sortedM = sorted(dataGm['guild_members'], key=lambda x: x["guild_points"], reverse=True)
        o = 0
        for i in sortedM:
            o = o + 1
            embed.add_field(name=f'{o}. {i['name']}', value=f'Ранг: {i['rank']}\nGuild Points: {i['guild_points']}\nXP: {i['xp']}', inline=False)

        await interaction.followup.send(embed=embed)



@client.tree.command(name='search_player', description='Знайди ID гравця Brawlhalla за нікнеймом (якщо пройдено 10 placement matches)', guild=GUILD_ID)
async def add(interaction: discord.Interaction, player_username: str):
    await interaction.response.defer()

    urlR = 'https://api.brawlhalla.com/v1/leaderboard/ranked'
    query_paramsR = {"game_mode": '1v1', 'region': 'ALL', 'search': player_username.lower()}
    responseR = requests.get(urlR, params=query_paramsR)

    print(responseR.status_code)

    if responseR.status_code != 200:
        await interaction.response.send_message(f'Щось пішло не так. Код помилки: {responseR.status_code}')

    if responseR.status_code == 200:
        dataR = responseR.json()
        embed = discord.Embed(title='СПИСОК ГРАВЦІВ', color=discord.Color.yellow())
        embed.set_thumbnail(url='https://static.wikia.nocookie.net/brawlhalla_gamepedia/images/1/14/Brawlhalla_Logo_100M_Full.png/revision/latest/scale-to-width-down/340?cb=20230520001004')
        embed.set_author(name='Saharok', url='https://www.youtube.com/@sahar_is_real', icon_url='https://yt3.googleusercontent.com/MeVCIqlkHHGMGvrJPuXJwTbxBldWdb9NK85V4apSg7y_IwgJYdNg-pgP2uCI3m8SW1j1MhTqn74=s160-c-k-c0x00ffffff-no-rj')
        for i in dataR['rankings']:
            if i['players'][0]['username'].lower().startswith(player_username.lower()):
                embed.add_field(name=f'{i['players'][0]['username']}', value=f'ID: {i['players'][0]['id']}\nРанг: {i['rating']}', inline=False)
        await interaction.followup.send(embed=embed)


bot_token = os.getenv("SBOT_TOKEN")

client.run(bot_token)
