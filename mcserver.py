from nextcord import Colour, Embed
from mcstatus.server import MinecraftServer
from bruhtil.bruhtil import remove_sectionsign
class mcserver_info:
    def __init__(self, ip, servername="None"):
        self.ip = ip
        if servername == "None":
            self.servername = ip
        else:
            self.servername = servername
        try:
            server = MinecraftServer.lookup(ip)
            self.status = server.status()
            continue_analising = True
        except TimeoutError:
            self.timeout()
            continue_analising = False
        except ConnectionRefusedError:
            self.connectionrefused()
            continue_analising = False
        if continue_analising:
            self.version = remove_sectionsign(self.status.version.name)
            self.description = remove_sectionsign(self.status.description)
            self.maxplayers = self.status.players.max
            self.players = self.status.players.online
            self.latency = self.status.latency
            self.colour = Colour.green()
    def timeout(self):
        self.version = " "
        self.description = "This server couldn't be found"
        self.maxplayers = 0
        self.players = 0
        self.latency = "∞"
        self.colour = Colour.red()
    def connectionrefused(self):
        self.version = " "
        self.description = "This server is offline or no mc-server"
        self.maxplayers = 0
        self.players = 0
        self.latency = "∞"
        self.colour = Colour.red()
    def generate_embed(self):
        embed = Embed(title = "I'm looking for a server", color = self.colour)
        embed.add_field(name=self.servername, value = self.description)
        embed.set_footer(text=f"IP: {self.ip}\nVersion: {self.version}")
        embed.add_field(name=f"Players: {self.players}/{self.maxplayers}", value=f"Latency: {self.latency}")
        return embed