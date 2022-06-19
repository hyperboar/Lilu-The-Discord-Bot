

def print_guilds(client):

    if len(client.guilds) == 0:
        print(f'{client.user} is connected to no guilds...')
        return
    
    print(f'{client.user} is connected to the following guilds:')
    for guild in client.guilds:
        print(f'{guild.name} (id: {guild.id})')


def is_mention_user(message, user):
    return discord.utils.get(message.mentions, id = client.user.id)


def main():
    pass

if __name__ == "__main__":
    main()