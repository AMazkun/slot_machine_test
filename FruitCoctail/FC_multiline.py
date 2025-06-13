import os
from time import sleep

import numpy as np
from tensorflow.python.framework.test_util import skip_if

from FC import symbols, paytable, paylines, ROWS, COLS, wild, NUM_PAYLINES

def spin_reels():
    """Simulate spinning the reels based on symbol probabilities."""
    symbols_keys = list(symbols.keys())
    probabilities = list(symbols.values())

    reels = []
    for _ in range(COLS):
        # For each reel, select ROWS symbols based on probabilities
        reel = np.random.choice(symbols_keys, size=ROWS, p=probabilities)
        reels.append(reel)

    # Convert to a grid format where grid[row][col] gives the symbol
    grid = []
    for i in range(ROWS):
        row = []
        for j in range(COLS):
            row.append(reels[j][i])
        grid.append(row)

    return grid


def evaluate_payline(grid, payline):
    """Evaluate if a payline has a winning combination."""
    # Get symbols on the payline
    symbols_on_line = [grid[row][col] for row, col in payline]

    win, symbol = визначити_виграш(symbols_on_line)

    return win, symbol

# CALC WIN

def подивитися_виграш_символу(символ, попередній_виграш, кількість_однакових):
    if кількість_однакових in paytable.get(символ, {}):
        return max(попередній_виграш, paytable[символ][кількість_однакових])
    else:
        return попередній_виграш

def wild_combination_win(комбінація):
    виграш = 0
    кількість_однакових = 1 if комбінація[0] == wild else 0
    for i in range(1, len(комбінація)):
        if комбінація[i] == wild:
            кількість_однакових += 1
        else:
            виграш = подивитися_виграш_символу(wild, виграш, кількість_однакових)
            кількість_однакових = 0

    # Перевірити у кінці
    виграш = подивитися_виграш_символу(wild, виграш, кількість_однакових)
    return виграш

def визначити_виграш(комбінація):
    """Визначає виграш на основі комбінації та таблиці виплат."""
    виграш = 0
    win_symbol = ''
    кількість_однакових = 1
    поточний_символ = комбінація[0]
    for i in range(1, len(комбінація)):
        if поточний_символ == wild:
            поточний_символ = комбінація[i]
        if комбінація[i] == wild or комбінація[i] == поточний_символ:
            кількість_однакових += 1
        else:
            виграш_ = подивитися_виграш_символу(поточний_символ, виграш, кількість_однакових)
            win_symbol = поточний_символ if виграш_ > 0 else win_symbol
            виграш = виграш_
            кількість_однакових = 1
            поточний_символ = комбінація[i]

    # Перевірити у кінці
    виграш_ = подивитися_виграш_символу(поточний_символ, виграш, кількість_однакових)
    win_symbol = поточний_символ if виграш_ > виграш else win_symbol
    виграш = виграш_

    # Додаємо комбінації виключно з диких символів
    if кількість_однакових != COLS or поточний_символ != wild: # щоб повторно не добавляти лише одну комбінацію з дикого символа
        виграш += wild_combination_win(комбінація)
    return виграш, win_symbol

def calculate_expected_payouts(num_spins=10000):
    """Calculate the expected payout per bet based on Monte Carlo simulation."""
    total_payout = 0
    total_bet = 0

    for _ in range(num_spins):
        grid = spin_reels()
        spin_payout = 0

        # Check each payline for winning combinations
        for payline in paylines:
            win, _ = evaluate_payline(grid, payline)
            spin_payout += win

        total_payout += spin_payout
        total_bet +=  NUM_PAYLINES

    # Calculate RTP (Return to Player) assuming 1 credit bet per payline
    payout_per_bet = total_payout / total_bet
    return payout_per_bet


def calculate_theoretical_payout():
    """Calculate the theoretical payout percentage based on symbol probabilities."""
    symbols = list(symbols.keys())

    # Calculate probability of each possible combination on a payline
    total_probability = 0
    total_expected_value = 0


    # Theoretical RTP for a single payline
    theoretical_rtp = total_expected_value * 100  # Convert to percentage

    return theoretical_rtp

def spin_and_show():
    grid = spin_reels()

    # Print the reels grid for visualization
    for row in grid:
        print(" | ".join(row))
    print("-" * 25)

    # Calculate payouts for each payline in this spin
    total_win = 0
    for i, payline in enumerate(paylines):
        win, symbol = evaluate_payline(grid, payline)
        if win > 0:
            print(f"Payline {i + 1} {symbol} wins: {win}")
            total_win += win
    print(f"Total win for this spin: {total_win}")
    #print("-" * 25)
    print()

def run_spins():
    for i in range(0, number_of_spins):
        print("\033[H\033[3J", end="")
        print("Spin:", i)
        spin_and_show()
        sleep(0.2)

# STATISTICA
number_of_tests = 100_000_000
number_of_spins = 20
skip_spin = 1

if __name__ == "__main__":
    print(f"\nFRUIT COCKTAIL MULILINE SIMULATION: {NUM_PAYLINES} lines")

    if skip_spin == 0:
        run_spins()

    # Calculate expected payout through simulation
    print(f"SIMULATING : {number_of_tests} spins")
    print("Please wait ...")
    exp_payout_per_bet = calculate_expected_payouts(number_of_tests)
    rtp = exp_payout_per_bet * 100  # Convert to percentage

    print(f"Expected payout per bet (simulated): {exp_payout_per_bet :.4f}")
    print(f"Return to Player (RTP) percentage: {rtp:.2f}%")

    # Calculate theoretical payout (simplified)
    #theo_rtp = calculate_theoretical_payout()
    #print(f"Theoretical RTP for a single payline: {theo_rtp:.2f}%")