# SLOT MACHINE SETUP
# FRUIT COCKTAIL

# Symbol probabilities
wild = "🍹"
symbols = {
    "🍒": 0.35,
    "🍋": 0.23,
    "🍑": 0.15,
    "🍏": 0.10,
    "🍐": 0.07,
    "🍉": 0.05,
    wild: 0.03,  # Wild symbol
    "🍓": 0.02  # Scatter (not used for line wins as noted)
}

# Define the paytable: value for each symbol and number of symbols in a row
# Format: {symbol: {3: payout_for_3, 4: payout_for_4, 5: payout_for_5}}
paytable = {
    "🍒": {3: 2, 4: 3, 5: 10},
    "🍋": {3: 3, 4: 5, 5: 20},
    "🍑": {3: 5, 4: 10, 5: 50},
    "🍏": {3: 10, 4: 30, 5: 100},
    "🍐": {3: 20, 4: 50, 5: 200},
    "🍉": {3: 30, 4: 100, 5: 500},
    wild: {3: 50, 4: 100, 5: 500},
    "🍓": {3: 200, 4: 1000, 5: 5000},
}

# Define the size of the slot machine
ROWS = 3
COLS = 5
NUM_PAYLINES = 9  # Typical number of paylines for Fruit Cocktail

# Define winning paylines (simplified version with 9 common paylines)
paylines = [
    [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4)],  # Top horizontal
    [(1, 0), (1, 1), (1, 2), (1, 3), (1, 4)],  # Middle horizontal
    [(2, 0), (2, 1), (2, 2), (2, 3), (2, 4)],  # Bottom horizontal
    [(0, 0), (1, 1), (2, 2), (1, 3), (0, 4)],  # V shape
    [(2, 0), (1, 1), (0, 2), (1, 3), (2, 4)],  # Inverted V shape
    [(0, 0), (0, 1), (1, 2), (2, 3), (2, 4)],  # Diagonal top-left to bottom-right
    [(2, 0), (2, 1), (1, 2), (0, 3), (0, 4)],  # Diagonal bottom-left to top-right
    [(1, 0), (0, 1), (0, 2), (0, 3), (1, 4)],  # Top zigzag
    [(1, 0), (2, 1), (2, 2), (2, 3), (1, 4)]  # Bottom zigzag
]
