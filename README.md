# Post's Correspondece Problem Recognizer

A threaded implementation of a recognizer for the Post Correspondence Problem.

## The problem

Given a finite sequence (X<sub>1</sub>, Y<sub>1</sub>),..., (X<sub>k</sub>, Y<sub>k</sub>) of pairs of nonempty strings.

Find a seqence i<sub>1</sub>...i<sub>l</sub>, such that X<sub>i1</sub>...X<sub>in</sub> =Y<sub>i1</sub>...Y<sub>in</sub>

## Implementation

Exhaustively searches for a match using multiple threads. Obviously loops infinitely if there is no solution for the problem 
instance.

## Launch

In the `pcp.config.json` file,

set `x` to [X<sub>1</sub>,...,X<sub>k</sub>] 

and `y` to [Y<sub>1</sub>,...,Y<sub>k</sub>] .

and Also specifiy the number of threads to use.

then : 

`python3 pcp_recognizer`
