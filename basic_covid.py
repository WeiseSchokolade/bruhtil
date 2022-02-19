import requests
import nextcord

def get_district(district):
    r = requests.get("".join(['https://api.corona-zahlen.org/districts/', str(district)]))
    response_prepare = r.json()['data']
    try:
        response = response_prepare[district]
    except Exception:
        return "Error#404"
    return response

def generate_embed(data):
    embed = nextcord.Embed(title = f"Covid-19 in {data['name']} ({data['ags']})", color = nextcord.Colour.red())
    embed.add_field(name = "Total Numbers", value = f"Population: {data['population']}\nCases: {data['cases']}\nDeaths: {data['deaths']}")
    embed.add_field(name = "Spreading", value = f"Incidence: {round(data['weekIncidence'])}\nPercentage: {round(data['casesPer100k']/1000)}%")
    return embed