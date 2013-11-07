This is a mostly-untested implementation of naive Monte Carlo tree
search.  It uses almost all of the allotted 1 second, so games can be
slow.

Run `make` to build, `make test` to go a round against clever.py.

TODO:
* Parallelize -- tree search is embarrassingly parallel.
* Pre-cache the first few moves.  Our first 7 moves can be played
  perfectly with a 1MB or so lookup table.
* Check that we perform well enough on the endgame.  Consider
  switching to minimax for the endgame.
* Add control for space usage -- on a fast machine without much memory
  we can end up in swap right now.
* Re-consider current strategy of marking ties as 50% win rate.  That
  seems dumb in retrospect.
* Make `calc_score` faster, or compute it less often.  Figure out the
  correct constant.
* Add actual knowledge of Connect-4 strategy to help prune the tree.