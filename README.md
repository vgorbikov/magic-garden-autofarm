# Magic Garden autofarm bot
The python autofarm bot for [MagicGarden game](https://magicgarden.gg/r/GKTQ?mc_source=router)


## What a bot can do

It can... Harvest all day while you're doing something else (unless you're working on a PC and preventing the bot from doing its job)!

### The algorithm 

- The bot walks all over your garden
- If the bot sees that something is ripe, the bot will harvest it! (...and move on because it has a job)
- If the inventory is full, he sells out the entire harvest (not forgetting to check in the magazine if he found something new).
- And again he walks all over your garden and looks for a crop that is ready for harvesting.

>[!note] The strategy 
> You might have noticed that this algorithm works well only if you have a lot of shrubs that mature quickly enough (because the bot does not plant new plants). 
>
>One of the best options, in my opinion, is to plant all (or almost all) burro's tail (you can add some camellias and fast-maturing trees).

## Deployment

>[!warning] You need a Python
> I recommended using python version 3.12 or later

1. Clone repo
    ```bash
    git clone https://github.com/vgorbikov/magic-garden-autofarm.git
    ```
2. Go to the project folder
    ```
    cd magic-garden-autofarm
    ```
3. Create a virtual environment
   ```bash
   python -m venv env
   ```
4. Install dependences
    ```bash
    pip install -r requirements.txt
    ```


## How to use it

1. Open the MagicGarden game on you Discord.
2. Place your character on the top left cell of your garden (the one where there is still a garden bed).
3. Run the script and click on the Discord window with the game (this is necessary to activate the game window so that it responds to signals from the script. You have 5 seconds to do this)
4. Enjoy!


## How it works

This project uses `pyautogui` (with `opencv`) to recognize interface elements (harvest buttons, notifications) and `pydirectinput` for keyboard and mouse input.

This way, we do not interfere with the MagicGarden API (this makes the program more complex, but it reduces the likelihood of account blocking). It also imposes restrictions on its operation in the background - it emulates input devices, and therefore you will not be able to work at the same PC at the same time as it, as you will compete for the input stream.