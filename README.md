# Advent of Code
Just a personal tracking of all code shenanigans for Advent of Code.

## Session Setup
To use the automatic input fetching, you need to set up a file called `SESSION` in the main directory. Go to an Advent of Code puzzle site (like [2021, day 1](https://adventofcode.com/2021/day/1)) and login using whatever credentials you want. Then open the developer tools of your browser, go to the `Network` tab, go to the `Headers` tab, and then scroll down until you find a field called `cookies`. Copy and paste everything in `session=` and put it in the file. The file is ignored by Git for privacy.

## Usage
Use this to download the data for the day and set up the solution file.

```
python load_sleigh.py <year> <day>
```

Write your answers in the `first_star` and `second_star` functions in the file created for the current date in `solutions/`. Then run

```
python ho_ho_hack.py <year> <day>
```

The two answers should print to the terminal, which you can paste into the submission box.
