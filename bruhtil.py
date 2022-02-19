from nextcord.ext import commands
import nextcord 
import requests
import random

class MissingInformationError(Exception):
    def __str__(self, missing_args):
        return f"Missing arguments in info.txt: {missing_args}"

class DevError(Exception):
    def __str__(self, args):
        return args

def get_bot_info():
    """Get bot info from reading a file."""
    TOKEN = ""
    PREFIX = ""
    session = -1
    with open("info.txt", "r+", encoding=None) as file:    
        for line in file:
            if len(line.split(": ")) == 2:
                if line.startswith("TOKEN: "):
                    TOKEN = line.split(": ")[1].strip()
                elif line.startswith("INVITE_LINK: "):
                    INVITE_LINK = line.split(": ")[1].strip()
                elif line.startswith("PREFIX: "):
                    PREFIX = line.split(": ")[1].strip()
                elif line.startswith("session: "):
                    session = int(line.split(": ")[1].strip())
                    update_file("info.txt", {"session": str(session+1)})
    if TOKEN and PREFIX and session:
        return TOKEN,PREFIX,INVITE_LINK,session
    if not TOKEN:
        raise MissingInformationError("Token")
    if not PREFIX:
        raise MissingInformationError("Prefix")
    if session == -1:
        update_file("info.txt", {"session":0})
        return TOKEN,PREFIX,INVITE_LINK,0

def remove_sectionsign(to_remove):
    """Remove special characters from minecraft MOTDs and other strings."""
    to_remove = to_remove.replace("§0", "")
    to_remove = to_remove.replace("§1", "")
    to_remove = to_remove.replace("§2", "")
    to_remove = to_remove.replace("§3", "")
    to_remove = to_remove.replace("§4", "")
    to_remove = to_remove.replace("§5", "")
    to_remove = to_remove.replace("§6", "")
    to_remove = to_remove.replace("§7", "")
    to_remove = to_remove.replace("§8", "")
    to_remove = to_remove.replace("§9", "")
    to_remove = to_remove.replace("§a", "")
    to_remove = to_remove.replace("§b", "")
    to_remove = to_remove.replace("§c", "")
    to_remove = to_remove.replace("§d", "")
    to_remove = to_remove.replace("§e", "")
    to_remove = to_remove.replace("§f", "")
    to_remove = to_remove.replace("§l", "")
    to_remove = to_remove.replace("§n", "")
    to_remove = to_remove.replace("§o", "")
    to_remove = to_remove.replace("§k", "")
    to_remove = to_remove.replace("§m", "")
    to_remove = to_remove.replace("§r", "")
    return to_remove

def read_file(filename, return_type):
    """Read a file and turn it into the given return_type.
    
    return_type is a string. The following modes are possible:
    - "d" will return a dictionary.
    - "l" will return a list
    """
    if return_type == "d":
        data = {}
        with open(filename, 'r', encoding=None) as file:
            for line in file.read().split("\n"):
                if len(line.split(": ")) == 2:
                    data[line.split(": ")[0]] = line.split(": ")[1].strip()
        return data
    elif return_type == "l":
        data = []
        with open(filename, 'r', encoding=None) as file:
            for line in file.readlines():
                data.append(line.strip())
        return data
    raise ValueError("This type couldn't be found.")

def update_file(filename, update_to):
    """Update a file to new data.
    
    Syntax: update_file(filename, update_to)    
    Open the file filename, read it's data and change the data inputed in update_to.
    filename needs to be a String.
    update_to needs to be a dictionary.
    """
    data = read_file(filename, "d")
    data |= update_to
    converted_data = [f"{key}: {value}" for key, value in data.items()]
    finallised_data = "\n".join(converted_data)
    with open(filename, 'w', encoding=None) as file:
        file.write(finallised_data)
    return data
def can_be_int(to_check):
    """Check if a string can be turned into an int."""
    try:
        int(to_check)
        check_result = True
    except ValueError:
        check_result = False
    return check_result

def register_bot():
    """Create a new bot with information read by get_bot_info()."""
    TOKEN, PREFIX, INVITE_LINK, SESSION = get_bot_info()
    client = commands.Bot(command_prefix=PREFIX)
    client.remove_command("help")
    return client, TOKEN, PREFIX, INVITE_LINK, SESSION

def send_as_webhook(url, *args):
    raise DevError("Sorry, this is work in progress.")
    discord_webhook_url = url
    Message = {"content": f'{" ".join(args)}'}
    requests.post(discord_webhook_url, data=Message)

def log_message(message):
    """Log a message."""
    if isinstance(message.channel, nextcord.TextChannel):
        if isinstance(message.author, nextcord.Member):
            if message.author.nick:
                username = message.author.nick
            else:
                username = message.author.name
        else:
            username = message.author.name
    else:
        username = message.author.name
    if message.author.bot:
        username = username + " [BOT]"
    print(f"{message.created_at.strftime('%X')} {username}: {message.content} ({message.channel.type})")

def get_user_id(person):
    user_id = person.replace("@", "").replace("!", "").replace("<", "").replace(">", "")
    try:
        new_id = int(user_id)
    except ValueError:
        raise ValueError(f"{person} is not a valid user!")
        return
    return new_id

def bruhify(text):
    """Bruhify the given text.
    
    Randomly add bruh at the beginning.
    Ramdonly make it all lowercase
    turn fucking, fuckin and fucken into bruhking
    """
    alphabet = "aAbBcCdDeEfFgGhHiIjJkKlLmMnNoOpPqQrRsStTuUvVwWxXyYzZ"
    if not isinstance(text, str):
        raise ValueError("Input needs to be a string!")
    text.replace(" fucking ", " bruhking ")
    text.replace(" fucken ", " bruhken ")
    text.replace(" fuckin ", " bruhkin ")
    if random.randrange(2) == 1:
        first_word = text.split(" ")[0].lower()
        if first_word == "lmao":
            text = " ".join(text.split(" ")[1:])
        elif first_word == "lmfao":
            text = " ".join(text.split(" ")[1:])
        elif first_word == "bruh":
            text = " ".join(text.split(" ")[1:])
        elif first_word == "lol":
            text = " ".join(text.split(" ")[1:])
        text = "bruh " + text
    if random.randrange(5) == 4:
        text = text.lower()
        text.replace(" i ", " I ")
    if random.randrange(5) == 4:
        text = text + " like, wtf?"
    new_text = ""
    for word in text.split(" "):
        if word.lower() == "omg":
            if random.randrange(2) == 1:
                for i in range(random.randrange(10)+5):  # @UnusedVariable
                    new_text += random.choice(alphabet)
                new_text += " "
            else:
                new_text += word
                new_text += " "
        else:
            new_text += word
            new_text += " "
    text = new_text
    
    return text