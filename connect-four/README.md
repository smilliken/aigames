## Connect Four

`runner.py` is a script that will coordinate a game of connect four between two bots.

Two example bots are included:

`example-rand.py`: chooses next move randomly.
`example-mod.py`: chooses next column successively.

To run a game between these two bots, just execute `runner.py`.

Or more generally: `./runner.py ./example-mod.py ./example-rand.py -r100`.

See `./runner.py -h` for more info.


### Write your own bot

In connect four, each player only has 7 choices (0-6) for each move. To interface with the runner,
your bot should alternate reading the opponent's move from STDIN and writing its move to STDOUT.

Make sure each move is terminated with a newline character, and that the buffer is manually
flushed, otherwise the runner will hang waiting for the buffer to be flushed.

If your bot gets the first turn, the runner will send `go!\n` as the initial input.
