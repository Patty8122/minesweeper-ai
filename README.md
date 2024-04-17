# MinesweeperAI Hackathon

Welcome to the MinesweeperAI hackathon! The objective of this challenge is to develop a MinesweeperAI capable of solving the Minesweeper game. We've provided you with the `runner.py` file that runs the Minesweeper game. You can either play the game manually or utilize the provided MinesweeperAI by clicking the "AI Move" button to make a move.

## Minesweeper Rules

Minesweeper is a classic single-player puzzle game where the player's goal is to uncover all cells on a rectangular grid without detonating any mines. Here are the basic rules:

1. **Objective**: Uncover all non-mine cells on the grid.
2. **Grid**: The game is played on a rectangular grid of cells, some of which contain mines.
3. **Numbers**: Each cell either contains a mine or a number indicating the count of mines in adjacent cells (including cells touching corners).
4. **Actions**: Players can uncover cells manually or utilize an AI to make moves.
5. **Safety**: Players can mark cells suspected to contain mines to avoid accidental clicks.
6. **Winning**: The game is won when all non-mine cells are uncovered.

## runner.py

You won't need to make any adjustments to the `runner.py` file. However, reviewing lines 162-223 is recommended to understand the mechanics of the Minesweeper game, particularly how moves are defined (specifically in lines 214-223).

## minesweeper.py

In the `minesweeper.py` file, your task is to update functions ending with `raise NotImplementedError`. Here's a description of key variables/classes:

- **Cell**: Represents the (y, x) location of a specific cell.
- **Count**: Indicates the number of mines adjacent to a cell or within a set of cells.
- **Sentence**: A class containing a set of adjacent cells and the count of mines within that set.

You'll implement the `MinesweeperAI` class, which contains all current knowledge and decides the next move. Utilize the `self.knowledge` list to determine safe moves. The `add_knowledge` function will be crucial for updating AI knowledge and making decisions.

## General Notes

- **Debugging**: If you use debugging techniques, remember to comment them out instead of deleting them.
- **Assistance**: If you have any questions, feel free to ask via chat, raise your hand, or return to the main breakout room for support.
- **No GPT Assistance**: You're not allowed to use any GPT or code assistance during this hackathon.
- **GPT Plus**: If you have GPT Plus, the provided custom GPT won't give direct code solutions. We encourage independent problem-solving.
- **Improvements**: If you finish early, consider enhancing the AI or modifying the game layout to showcase your solution.

Good luck with your MinesweeperAI development! We're excited to see your innovative approaches and problem-solving skills in action.