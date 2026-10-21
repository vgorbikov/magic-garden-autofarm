# Magic Garden Bot
The python bot for [MagicGarden game](https://magicgarden.gg/r/GKTQ)


## What a bot can do

At the moment, the Bot supports a number of directives. Directives can be added by you, if desired.

The currently supported directives are listed below

### Shop Items

Bot monitor shop stocks and buy items which you select.

It may be eggs, seeds, tools and decor.

### Weather pet teams rotation

Bot monitor a weather and set pet team which you select to this weather.

>Pet team must have a name, to can be selected

### Feeding active pets (beta)

Bot monitor level of hunger of active pets and feeding it. If you don't have vrops in you inventory, bot harvest it.

## Configuration

All directives configurating in `config.yaml` file. You can see emy example in repo.

## Auth

For working, bot needs a auth in you profile. Now you must start a `save_auth_state.py` script for do it. Program opens a browser window? you must login in you account any way and press `Enter` in terminal. Auth session will be saved in you local repo.

## Usage

Write all settings in `config.yaml` file and starts `main.py` file. Bot starts working!

>You must have python on you PC to starts it.

While bot working, you dont must play in opened browser window. If you want to join game youself, off the Bot and join to game.

>To off the Bot, press `Enter` in terminal.

## To Do

My plans to upgrade the Bot:
- Do useful console interface
- Adding reloading on errors, game updates and any incedents
- Adding directives:
  - Farm dust with common eggs growing
  - Selective crop harvesting and selling
  - Situationship pet teams rotation
