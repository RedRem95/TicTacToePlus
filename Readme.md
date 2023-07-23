# TicTacToe Plus

## Description

This project implements an advanced variant of TicTacToe.

### Game
Like in TicTacToe you win when you have a full row, column or diagonal. But unlike in TicTacToe each player has different
keystones to play with. If you place a 1 on a field another player could place a 2 or higher on it, so higher keystones beat
lower ones. This gives more tactical depth, complexity and removes the very simple nature of TicTacToe.
Per default each player gets keystones 1, 2 and 3 and 3 of each. So if you place a 3 your opponent can not beat it and its safe
but by limiting the amount its still a tactical choice.

To play standard TicTacToe you could give each player just one keystone 5 times.

## Table of Contents (Optional)

If your README is long, add a table of contents to make it easy for users to find what they need.

- [Installation](#installation)
- [Usage](#usage)
- [Credits](#credits)
- [License](#license)
- [Planned Features](#planned-features)

## Installation

``` bash
pip install git+https://github.com/RedRem95/TicTacToePlus.git
```

## Usage

### Play

You can either play as 2 human players or against the AI.
The play entrypoint takes 2 arguments `-p1` and `-p2`. For each you can either provide `human` for a human to play or 
a path to a trained `model.zip` to let the AI play

```bash
play_tttp -p1 human -p2 /path/to/model.zip
```

### train

Currently only training and running PPO models is supported.
In the future it should be possible to use a variety of algorithms but not yet.

```bash
train_tttp -t /path/to/target -s 1000000
```

## Credits

Huge thanks to the stable-baselines3 project

## License

GPL3 [LICENSE](LICENSE).

## Planned Features

This project is meant to be a starting point for simple AI implementations, with or without Machine Learning.

So the API to use TicTacToePlus in different other projects with greatly improve
