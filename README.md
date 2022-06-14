# WordleBot

A bot to play Wordle at https://www.nytimes.com/games/wordle/index.html

Currently in development.

## Setup

`pip install pillow`
`pip install pyautogui`

## Running

```
usage: wordle.py [-h] [-w ALLOWED_WORDS] [-v] {bot,sim} ... dictionary

positional arguments:
  {bot,sim}
    bot                 run Wordle browser bot
    sim                 run Wordle simulation
  dictionary            word dictionary file

options:
  -h, --help            show this help message and exit
  -w ALLOWED_WORDS, --allowed-words ALLOWED_WORDS
                        allowed words dictionary file
  -v, --verbose         use verbose logging
```

### Wordle Bot

The Wordle bot will attempt to solve the daily Wordle puzzle from
https://www.nytimes.com/games/wordle/index.html

After running the script, the Worlde bot will start to enter a guess after 3
seconds. At this point, the browser should be open and navigated to the Wordle
site.

`python wordle.py bot -l LETTER_COORDS -b BOARD_COORDS dictionary`

`-l LETTER_COORDS` is the screen coordinates of the center position of the 'ENTER'
key on Wordle's on screen keyboard, formatted as 'x,y'

`-b BOARD_COORDS` is the screen coordinates of the bottom left area of the top
left board square, formatted as 'x,y'

`dictionary` is the word dictionary the Wordle bot will use to try and solve the
puzzle

#### Manual

```
usage: wordle.py bot [-h] -l LETTER_COORDS -b BOARD_COORDS [-s START]

options:
  -h, --help            show this help message and exit
  -l LETTER_COORDS, --letter-coords LETTER_COORDS
                        screen coords of center of 'enter' button, format as
                        '-cx,y' or '--letter-coords=x,y'
  -b BOARD_COORDS, --board-coords BOARD_COORDS
                        screen coords of top left board space, format as
                        '-cx,y' or '--board-coords=x,y'
  -s START, --start START
                        choose a word to start the puzzle with
  -d DELAY, --delay DELAY
                        delay in seconds between script execution and bot start up
```

#### Run Script

The run script will run the Wordle bot without worrying about the required
arguments. An optional argument may be provided to specify the puzzle starting
word. The script should work and is set up for standard 1920x1080 monitors
with the default browser zoom (Chrome). The script also expects the
'possible_words.txt' file to be in the 'res' directory. After running the
script, quickly open the browser tab containing Wordle.

`./run.sh [start_word]`

### Wordle Simulation

The Wordle simulation will play pseudo Wordle games and report statistics and
data collected from the set of simulation games.

`python wordle.py sim [-i ITERATIONS] dictionary`

`-i ITERATIONS` is the amount of Wordle games to play in the simulation

`dictionary` is the word dictionary the simulation will use to play Wordle games

#### Manual

```
usage: wordle.py sim [-h] [-i ITERATIONS] [-f FIRST] [-g GOAL]

options:
  -h, --help            show this help message and exit
  -i ITERATIONS, --iterations ITERATIONS
                        number of Wordle games to run
  -f FIRST, --first FIRST
                        run simulation with the same first guess each iteration
  -g GOAL, --goal GOAL  run simulation with same goal word each iteration
```
