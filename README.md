# Su Family Hackathon 2024 Winter Special Edition

## Schedule

* Start time: 1/2/2025
* Competition time: 1/5/2025 EOD

## Instructions to participants

* The game has two modes, a one-player mode and a two-player mode. 
  * In the two-player mode, the jet-fighter is controlled by the W-A-S-D keys for acceleration, left-turn, deceleration, 
    right-turn, respectively, and space key for firing a bullet. 
  * In one-player mode, the player will control the prop-fighter, and the jet-fighter will be controlled by the program. 
  * In both modes, the prop-fighter is controlled by a player using the 4 arrow keys. The prop-fighter cannot fire
    bullets. 
  * The two-player mode is for participants to get familiar with the game, and the one-player mode will be used for the
    competition. 
* Victory conditions:
  * Overall objective is for the jet-fighter to shoot down the prop-fighter without itself crashing on the obstacle in
    the middle of the battlefield or crashing with the prop-fighter. 
  * When the jet-fighter shoots down the prop-fighter, the jet-fighter wins, and a timer will be displayed to report 
    for how long the prop-fighter has survived the onslaught of the jet-fighter. 
  * When the jet-fighter crashes on the obstacle in the middle of the battlefield, the prop-fighter wins. 
  * When the prop-fighter crashes on the obstacle in the middle of the battlefield, the jet-fighter wins.
  * When the two fighters crash into each other, the prop-fighter wins. 
  * If the prop-fighter manages to survive for longer than one minute, the prop-fighter wins. 
* Implement the `PlayerStrategy` class in `Player/PlayerStrategy.py`. 
  * Implement the `decision()` method. The inputs and outputs of this method are specified in [Strategy.py](https://github.com/churinga/SuHackathon2024Winter/blob/dc97475feddcd60262c7038a1046900504b96681/Engine/Strategy.py#L21-L89). 
  * You can add any member to the `PlayerStrategy` class as needed, for example, to save states, or to calculate strategies. 
* The `decision()` method of your strategy class will be called every tick, which is around 25ms. There is no guarantee 
  the ticks are exactly 25ms apart, but it will be close. 
* It's ok for the `decision()` method to take longer than a tick to finish computing for the strategy of the current tick. 
  In case it takes longer, the jet-fighter simply skips decision-making, and maintains its current state until a new 
  command is received from the `decision()` method call. 
* If the `decision()` method throws any exception in the middle of the execution, its aborted, and this iteration of
  decision-making will be skipped. It won't affect other iterations in the future. 
* Participants are allowed to look at the game engine code to understand how the game runs, and to get specifications of
  screen size, jet-fighter and prop-fighter specs, etc. This is not considered as cheating. 
* Any other form of circumventing normal game mechanics or hacking the engine code will be considered as cheating, at Dad's 
  discretion, and once verified, will forfeit the participant's qualifications. 
* The competition will start in one-player mode, and Dad will control the prop-fighter manually while the participants'
  code will control the jet-fighter. Whoever wins 3 out of 5 rounds will be the final winner. 

## How to run the program

Install dependencies in the Python virtual environment as specified in `requirements.txt`. Start the competition program
by running the `tournament.py`. It requires a screen of size larger than `1600x1200` and a moderately fast CPU. Python 3.8
or above is recommended. 
