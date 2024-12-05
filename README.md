# Advent of Code
Just a personal tracking of all code shenanigans for Advent of Code.

## Session Setup
To use the automatic input fetching, you need to set up a file called `SESSION` in the main directory and populate it with your cookie session file contents. In Chrome, it's in `Inspect > Application > Storage > Cookies > https://adventofcode.com > session`.

## Usage
Use this to download the data for the day and set up the solution file.

```
python load_sleigh.py <year> <day>
```

Write your answers in the `first_star` and `second_star` functions in the file created for the current date in `solutions/`. Then run

```
python jingle_jangle.py <year> <day>
```

The two answers should print to the terminal, which you can paste into the submission box.
