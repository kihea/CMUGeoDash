## CMUGeoDash
A geometry dash "clone" made in CMU CS Academy's Sandbox
You can find a live demo without building (with a few errors) [here](https://academy.cs.cmu.edu/sharing/lavenderBlushGiraffe5183)
Due to CMU's physics, there may be collision bugs that are out of my control

# Dependencies
```
pip install cmu-graphics
```

# Levels
You can add custom levels by editing ```app.levels```
The syntax for code serialization is as follows
```
b#, where # is any number 1-9, creates # blocks in a stack at current position of the level (index starts at 0, a little ahead of the player's start)
h#, ^^                       , creates # 'heightened' blocks in a stack at current index
>#, ^^                       , skips # blocks, moving the index of the decoding algorithm forward by # blocks
^#, ^^                       , skips # blocks in height, not moving the index forward, but upward. The next entity creation starts at the same block number except # numbers higher
e,                           , creates a spike block at the current position, then moves the index forward once
S,                           , changes the player model to a ship
C,                           , changes the player model to a cube
s#, where # is any number 1-5, changes the player's speed accordingly
j,                           , creates a jump pad at the current position, then moves the index forward once
J,                           , creates a jump orb at the current position, then moves the index forward once
```