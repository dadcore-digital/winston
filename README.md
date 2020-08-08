# Winston

Winston is a Discord bot for the Killer Queen Black Community. 

The plan is to *not* ever make this a publicly listed bot. However, you're free to run it on your own server, or contact me and I can probably run an instance for you as well.

## Setup
1. Find some linux shell space.
2. Git clone this repo
3. Save `settings.json.example` as -> `settings.json`
4. Change `BOT_TOKEN` setting in `settings.json` to the secret token provided in your Discord Development admin screen.
5. `python winston.py`

You can poke around in `settings.json` to customize some of the language Winston uses too.

## Plug-Ins ("Cogs")
To enable a plugin, edit the `LOAD_COGS` array in `settings.json`, and add/remove cogs as needed. They should be capitalized (not all uppercase, not all lowercase).

Current plug-ins:

- **Autoresponder** - displays a message defined by the admins of the Killer Queen Black wiki
  - `!show poem`
- **Chance** - Dice and Coin Flips. 
  - `!roll 3d20 2d6`
  - `!flip snails`
  - `!flip snails should i install this bot?`
- **Events** - Retrieve match events from the KQB IGL Calendar. Also auto-announces upcoming matches to a channel of your chosing.
  -   `!matches`
  -   `!matches next`
- **Wiki** Search the Killer Queen Black Wiki for topics and display results.
  - `!wiki helix`

## Help

For help contact `@dadcore` on the [Killer Queen Black Discord Server](https://kqbdiscord.com).