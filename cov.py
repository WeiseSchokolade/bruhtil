import requests
import nextcord
from bruhtil.bruhtil import can_be_int

def get_district(district, location):
    r = requests.get("".join(['https://api.corona-zahlen.org/', str(location), '/', str(district)]))
    response_prepare = r.json()['data']
    try:
        response = response_prepare[district]
    except Exception:
        return "Error#404"
    return response

def generate_message(area):
    if len(area) == 5 and can_be_int(area):
        data = get_district(area, "districts")
        if data == "Error#404":
            return "bruh I couldn't find this district!"
        else:
            return generate_embed(data, area)
    elif len(area) == 2 and not can_be_int(area):
        data = get_district(area, "states")
        if data == "Error#404":
            return "bruh I couldn't find that area"
        else:
            return generate_embed(data, area)
    else:
        return "bruh that's not a valid state"

def generate_embed(data, area):
    embed = nextcord.Embed(title = f"Covid-19 in {data['name']} ({area})", color = nextcord.Colour.red())
    embed.add_field(name = "Total Numbers", value = f"Population: {data['population']}\nCases: {data['cases']}\nDeaths: {data['deaths']}")
    embed.add_field(name = "Spreading", value = f"Incidence: {round(data['weekIncidence'])}\nPercentage: {round(data['casesPer100k']/1000)}%")
    return embed