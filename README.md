# Grow-Flow

A relaxing underwater fantasy game where you play as a small water creature. 
Grow by feeding on the cells and smaller creatures around you and discover the world of Grow Flow.

Have fun ;)

***
### Presentation

Year of creation : 2023
Version : 1.0.5
Language : Python

***
## Vocabulary :

- Player bubble : A circle on the center of the screen the player can move with the mouse
- Enemy : Small red cell randomly moving in the map. Will pursue player if come too close. Will damage player when come to contact.
- Bubble of life : Small green cell randomly moving in the map. Will flee player if come too close. Will heal player when come to contact.
- Cell : Small white cell randomly moving in the map. Player will gain xp when come to contact. Become an eaten cell and stay in stomach.
- Eaten cell : Very small cells moving inside player (on his "stomach"). Will appear after eating a cell.
- Level : A part of this world, have its own size, color and depth.
- [later] Obstacles : Bloc of dead cell corpses, can't be eaten but can be slighty push.
- [later] Power : An ability player can use to help them during his journey.
- [later] Mutation : A passive upgrade that permanently that boost player's characteristic.

***
## Rules :

- Player can swim wherever they want as long as they stay in the level. (levels have borders)
- Enemy make damage to player when collide with them, then disappear.
- Bubble of life heal player when collide with them, then disappear.
- Cell give player xp when collide with them, then are placed in their stomach.
- Player must eat all cell to finish a level.
- For now, automatically go to next level when the last cell is eaten.

***
## Prerequisites :

- Python 3.11.1 or below
- Python interpreter
<!-- Complete libraries -->
- Librairies :
    - ast : Use to 
    - math : Use to make mathematical operations.
    - mutagen : Use to 
    - os : Use to access files and create directories and files.
    - pygame : Use to manage the whole program interface.
    - random : Use to 
    - sys : Use to
    - time : Use to 

***
## Installation guide

- Click on the green "<> Code" button
- On Local/SSH/, click on "Download as zip"
- Choose a location for the program in your machine
- Unzip the files
- With your python interpreter, launch the file "main.py"
- The game can start !

***
## User guide

#### Methods
<!-- Complete methods -->
- "name" (options) : result

-Images-
![Menu](images/screenshots/main_menu.png)
![First level](images/screenshots/level_1_part_1.png)
![First level](images/screenshots/level_1_part_2.png)
![Second level](images/screenshots/level_2.png)
![Third level](images/screenshots/level_3_part_1.png)
![Third level](images/screenshots/level_3_part_2.png)

***
## Roadmap

- v0.0.1 : 
    - Create basic functions of the game
- v0.1.0 : 
    - Create the main screen (window)
    - Add life bar + cells bar (stomach)
    - Choose a color for player
- v0.2.0 :
    - Add images and sounds for the game
    - Add enemies and bubbles of life (heal player)
- v0.3.0 : 
    - Display bubbles and enemies to the game
    - Add musics
- v0.4.0 : 
    - Add dynamic life bar, hunger bar and sounds bar
    - Add feature to go to next level + update music
    - Add movement for player with mouse
- v0.5.0 : 
    - Add spawn of cells (food), bubbles of life and enemies
    - Make player bigger when eat cells
    - Add eaten cells moving inside player
- v0.6.0 : 
    - Add damage when eat an enemy
    - Add healing when eat a bubble of life
- v0.7.0 : 
    - Fix balancing fo the gameplay
    - Close game when player die (will be change later by returning to main menu)
- v0.8.0 : 
    - Add auto saves
    - Add update game with saves data (player's name, etc)
- v0.9.0 : 
    - Display player's name above themself
    - Ask player's name when launch game
- v1.0.0 : 
    - Fix collision problem for eaten cells inside player
    - Remove objects related to changing screen size and making title disappear
    - Rewrite comments in english
    - Add documentation
- v1.0.5 : [In production]
    - Optimize larger levels (old version make them lag) : background is now a single image (might be a file too big)
    - Make enemies stronger as player goes through levels (increase speed, range, damage, or size) -> random upgrade(s)
- v1.1.0 : 
    - Add random obstacles
- v1.1.5 :
    - Add temporary powers for player :
        - speed boost (add energy bar ?)
        - detect entities enemies & life bubbles (already exists in late level)
        - invisibility
        - damage boost
        - became smaller
        - range attack (timer or limited munitions ?)
- v1.2.0 :
    - Add stars : small missions for each levels
        - Finish level
        - Don't take damage
        - Don't heal
    - Add rewards : mutations ? xp ? pets ?
- v1.2.5 : 
    - Auto load player's save when launch game
- v1.3.0 : [Design update]
    - Add visual effects :
        - blur
        - sunbeam
        - bubble coming from the bottom of the screen
        - giant sea creature at the background (blurry)
- v1.4.0 :
    - Add menus
    - Add parameters screen :
        - Methods of movement (arrows, mouse, joystick)
        - Personalize game theme (colors of background, enemies, etc)
        - Choose commands
    - Add credits
- v1.5.0 : 
    - If player is afk for at least 1 min, player's bubble will move in circles
- v1.6.0 :
    - Add tutorials
    - Add more transparency (interface, tutorials, etc)
- v1.7.0 :
    - Add mini-save : respawn if player dies but not full life
- v1.8.0 : [Security update]
    - Secure application (encryption, etc)
- v1.9.0 :
    - Add upgrades/mutations : upgrade player stats and skins
- v1.9.8 : 
    - Allow player to attack and defend themself neat the end of the game (against boss fight ?)
- v1.9.9 : 
    - Make documentations
- v2.0.0 : 
    - Create executioner class
    - Make the code into a .exe

***
## User license : GNU GPL v3

- Copyleft strict
- You can use it, modify it and share it but you have to keep the same license
- Must stay open source

***
**Contact : mir.nathan666@gmail.com**

Feel free to share your exprerience and your suggestions !
