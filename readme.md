# Mesa Checkers

## Rules

### Setup
1. 6x6 board grid
2. White and black rocks, optionally purple rocks
3. Rocks are flat, can be piled on board and on top of each other while holding firm (think lego)
4. Each player chooses a color, first to play is picked

### Game loop

1. Active player makes a turn 
2. Win condition check 
3. Pass turn to other player

### Player turn rules

1. Put a single rock of your color on the board
   1. You cannot put the rock on top of a rock of opponent's color
   2. You cannot put the rock on a pile of 4 rocks (optionally put a purple rock on top of such piles)
   3. The pile on which you put your rock this turn is the active pile
2. Make a move (optional)
   1. From the top of the active pile, select one or more rocks of your color in a row
   2. Choose an orthogonally bordering target pile with height less than the lowest selected rock
   3. Move the selected rocks onto the target pile
   4. If your active pile has a rock of your color on top, the target pile becomes the active pile; you may move again (go to 2.1)

### Win conditions

You win if each of the 4 corner piles either has a height of 4 or has a rock of your color on top.

## Mesa Checkers ASCII game

Engine and renderer for Mesa Checkers in Python.

- Model: state and engine contract definitions.
- Controller: rules checking engine.
- View: rendering layer which knows how to render state.