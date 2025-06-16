import copy
from random import shuffle, random, choice
import math
from enum import Enum
from dataclasses import dataclass
from typing import List, Dict, Tuple, Optional
import os

def clear_console():
    if os.name == 'nt':  # For Windows
        os.system('cls')
    else:  # For macOS and Linux
        print("\033[H\033[2J", end="")

TRY_OR_DIE = 1_000_000_000
SATISFY_RULE = dict(max_win=False, bonus_3FC_3x=False, bonus_3FC_4x=False, bonus_3FC_5x=False, bonus_4FC=False, fists_4_more_max_win=False)
class SymbolType(Enum):
    # Low paying symbols
    TEN = "10"
    JACK = "J"
    QUEEN = "Q"
    KING = "K"
    ACE = "A"

    # High paying symbols (Fighters)
    RED_FIGHTER_MAN = "RFM"
    RED_FIGHTER_WOMAN = "RFW"
    BLUE_FIGHTER_MAN = "BFM"
    BLUE_FIGHTER_WOMAN = "BFW"

    # Special symbols
    WILD = "WILD"
    EWILD = "FIST"
    FIST_RED = "RED_F"
    FIST_BLUE = "BLUE_F"
    FS_SCATTER = "FS"

WILDS = [SymbolType.WILD, SymbolType.EWILD]

class Team(Enum):
    RED = "RED"
    BLUE = "BLUE"

@dataclass
class SpinResult:
    grid: List[List[SymbolType]]
    grid_orig: List[List[SymbolType]]
    wins: List[Dict]
    total_win: float
    wild_reel_activations: List[Dict]
    epic_drops: List[Dict]

    def to_json(self):
        return {
            "grid": self.grid,
            "wins": self.wins,
            "total_win": self.total_win,
            "wild_reel_activations": self.wild_reel_activations,
            "epic_drops": self.epic_drops
        }

@dataclass
class GameState:
    balance: float
    lines: int
    bet: float
    selected_team: Team
    fighter : SymbolType
    opposite_fighter : SymbolType
    in_bonus: bool
    bonus_type: str
    bonus_spins_left: int
    victory_level: int
    total_spins: int
    total_wins: float
    reel_win :float
    wild_win :float
    fist_wild_win :float
    THROWDOWN_win :float
    U_THROWDOWN_win :float
    max_win:float

@dataclass
class FistOfDestructionEmulator:
    num_spins: int
    max_win_grid : [[]]
    max_win_limit : int = 0
    max_win_times : int = 10_000
    multiplier_options = [2, 3, 4, 5, 6, 7, 8, 9, 10, 15, 20, 25, 50, 100, 200]
    satisfied = SATISFY_RULE

    def __init__(self):
        self.max_win_spin = None
        self.setup_paytable()
        self.setup_symbol_weights()
        self.setup_paylines()
        self.ordinary_reel = self.generate_reel_strip(self.base_weights)
        self.bonus_reel = self.generate_reel_strip(self.bonus_weights)

    def setup_paytable(self):
        """Define symbol payouts based on GDD"""
        self.paytable = {
            # Low paying symbols (all same payouts)
            SymbolType.TEN: {3: 0.1, 4: 0.6, 5: 1.5},
            SymbolType.JACK: {3: 0.1, 4: 0.6, 5: 1.5},
            SymbolType.QUEEN: {3: 0.1, 4: 0.6, 5: 1.5},
            SymbolType.KING: {3: 0.1, 4: 0.6, 5: 1.5},
            SymbolType.ACE: {3: 0.2, 4: 0.6, 5: 1.5},

            # High paying symbols (all same payouts)
            SymbolType.RED_FIGHTER_MAN: {3: 1.0, 4: 3.0, 5: 8.0},
            SymbolType.RED_FIGHTER_WOMAN: {3: 1.0, 4: 3.0, 5: 8.0},
            SymbolType.BLUE_FIGHTER_MAN: {3: 1.0, 4: 3.0, 5: 8.0},
            SymbolType.BLUE_FIGHTER_WOMAN: {3: 1.0, 4: 3.0, 5: 8.0},
        }

    def setup_symbol_weights(self):
        """Define symbol distribution weights for base game and bonus"""
        # Base game weights (adjust these to match your theoretical model)
        self.base_weights = {
            SymbolType.TEN: 100,
            SymbolType.JACK: 100,
            SymbolType.QUEEN: 100,
            SymbolType.KING: 100,
            SymbolType.ACE: 100,
            SymbolType.RED_FIGHTER_MAN: 5,
            SymbolType.RED_FIGHTER_WOMAN: 5,
            SymbolType.BLUE_FIGHTER_MAN: 5,
            SymbolType.BLUE_FIGHTER_WOMAN: 5,
            SymbolType.WILD: 4,
            SymbolType.FIST_RED: 10,
            SymbolType.FIST_BLUE: 10,
            SymbolType.FS_SCATTER: 6,
        }

        # Bonus game weights (more fists and wilds)
        self.bonus_weights = {
            SymbolType.TEN: 100,
            SymbolType.JACK: 100,
            SymbolType.QUEEN: 100,
            SymbolType.KING: 100,
            SymbolType.ACE: 100,
            SymbolType.RED_FIGHTER_MAN: 60,
            SymbolType.RED_FIGHTER_WOMAN: 60,
            SymbolType.BLUE_FIGHTER_MAN: 60,
            SymbolType.BLUE_FIGHTER_WOMAN: 60,
            SymbolType.WILD: 30,
            SymbolType.FIST_RED: 40,
            SymbolType.FIST_BLUE: 40,
            SymbolType.FS_SCATTER: 10,
        }

    def setup_paylines(self):
        """Define the 40 fixed paylines"""
        # Standard 40-line pattern for 5x4 grid
        self.paylines = [
                            # Straight lines
                            [0, 0, 0, 0, 0],  # Top row
                            [1, 1, 1, 1, 1],  # Second row
                            [2, 2, 2, 2, 2],  # Third row
                            [3, 3, 3, 3, 3],  # Bottom row

                            # Zigzag patterns (simplified - add more complex patterns as needed)
                            [0, 1, 2, 1, 0],
                            [1, 0, 1, 2, 3],
                            [2, 3, 2, 1, 2],
                            [3, 2, 1, 2, 3],
                            [0, 1, 0, 1, 0],
                            [1, 2, 3, 2, 1],

                            # Additional patterns to reach 40 lines
                            # (You can expand this with your specific payline configuration)
                        ] + [[i % 4, (i + 1) % 4, (i + 2) % 4, (i + 3) % 4, i % 4] for i in range(30)]

        self.paylines = self.paylines[:40]  # Ensure exactly 40 lines

    def generate_reel_strip(self, weights: Dict[SymbolType, int]) -> List[SymbolType]:
        """Generate a weighted random reel strip"""
        symbols = []
        for symbol, weight in weights.items():
            symbols.extend([symbol] * weight)
        shuffle(symbols)
        print("Prepared reel:")
        print([x.name for x in symbols])
        print("\n")
        return symbols

    def team_fist(self) -> SymbolType:
        return SymbolType.FIST_RED if self.game_state.selected_team == Team.RED else SymbolType.FIST_BLUE

    def count_my_fists(self, grid) -> int:
        fists = 0
        fist = self.team_fist()
        for reel in grid:
            for symbol in reel:
                if symbol == fist:
                    fists += 1

        return 1 if fists < 3 else fists

    def spin_reels(self, is_bonus: bool = False) -> List[List[SymbolType]]:
        """Generate a 5x4 grid of symbols"""
        reel_strip = self.bonus_reel if is_bonus else self.ordinary_reel

        grid = []
        for reel in range(5):
            column = []
            for row in range(4):
                column.append(choice(reel_strip))
            grid.append(column)

        return grid

    def check_scatter_trigger(self, grid: List[List[SymbolType]]) -> Tuple[int, str]:
        """Check for scatter triggers and return count and bonus type"""
        scatter_count = 0
        for reel in grid:
            for symbol in reel:
                if symbol == SymbolType.FS_SCATTER:
                    scatter_count += 1

        if scatter_count >= 4:
            return scatter_count, "ULTIMATE_THROWDOWN"
        elif scatter_count >= 3:
            return scatter_count, "THROWDOWN"
        else:
            return scatter_count, ""

    def calculate_fist_multipliers(self, grid: List[List[SymbolType]], selected_team: Team) -> List[Dict]:
        """Calculate Wild Reel expansions and multipliers"""
        activations = []

        # Check for fist symbols of selected team
        fist_symbol = SymbolType.FIST_RED if selected_team == Team.RED else SymbolType.FIST_BLUE

        for reel_idx in range(5):
            reel = grid[reel_idx]

            found_only_once = False
            for fist_row_idx, symbol in reversed(list(enumerate(reel))):
                if symbol == fist_symbol and fist_row_idx > 0:

                    # Count opponents and wilds in the reel
                    for check_row, check_symbol in enumerate(reel[:fist_row_idx]):
                        if check_symbol == self.game_state.opposite_fighter or check_symbol == SymbolType.WILD:
                            # Expand the fist to wild across the entire reel
                            for i in range(fist_row_idx+1):
                                grid[reel_idx][i] = SymbolType.EWILD

                            # Determine multiplier based on punches
                            # Use weighted selection based on punch count
                            max_mult_idx = min(fist_row_idx, len(self.multiplier_options) - 1)
                            multiplier = choice(self.multiplier_options[:max_mult_idx + 3])  # Some randomness

                            activations.append({
                                'reel': reel_idx,
                                'fist_position': fist_row_idx,
                                'multiplier': multiplier,
                            })
                            found_only_once = True
                            break

                if found_only_once:
                    break

        return activations

    def calculate_payline_wins(self, grid: List[List[SymbolType]]) -> List[Dict]:
        """Calculate all payline wins"""
        wins = []

        for line_idx, payline in enumerate(self.paylines[: self.game_state.lines]):
            symbols_on_line = []
            for reel_idx, row in enumerate(payline):
                if reel_idx < len(grid) and row < len(grid[reel_idx]):
                    symbols_on_line.append(grid[reel_idx][row])

            # Check for wins (left to right)
            if len(symbols_on_line) >= 3:
                win_info = self.check_line_win(symbols_on_line)
                if win_info['payout'] > 0:
                    win_info['payline'] = line_idx
                    win_info['positions'] = [(i, payline[i]) for i in range(win_info['count'])]
                    wins.append(win_info)

        return wins

    def check_line_win(self, symbols: List[SymbolType]) -> Dict:
        """Check a single payline for wins"""
        if len(symbols) < 3:
            return {'symbol': None, 'count': 0, 'payout': 0}

        # Find the first non-wild symbol to use as the base symbol
        base_symbol = None
        for sym in symbols:
            if sym not in WILDS:
                base_symbol = sym
                break

        # If all symbols are wild, treat as the highest paying symbol or handle specially
        #if base_symbol is None:
        #    base_symbol = symbols[0]  # or your highest paying symbol

        # Count consecutive matching symbols from left
        count = 0
        for sym in symbols:
            if sym == base_symbol or sym in WILDS:
                count += 1
            else:
                break

        # Calculate payout
        payout_multiplier = 0
        if count >= 3 and base_symbol in self.paytable:
            payout_multiplier = self.paytable[base_symbol].get(min(count, 5), 0)
            self.game_state.reel_win += payout_multiplier

        # Check if this specific winning combination contains wilds
        winning_symbols = symbols[:count]
        if SymbolType.WILD in winning_symbols:
            self.game_state.wild_win += payout_multiplier

        return {
            'symbol': base_symbol,
            'count': count,
            'payout': payout_multiplier
        }

    def apply_fist_multipliers(self, wins: List[Dict], fist_activations: List[Dict]) -> float:
        """Apply fist multipliers to wins"""
        total_multiplier = 1.0

        for activation in fist_activations:
            # Check if this fist affects any wins
            for win in wins:
                for pos in win['positions']:
                    if pos[0] == activation['reel']:  # If win is on the same reel as fist
                        total_multiplier += activation['multiplier'] - 1  # Additive stacking
                        break

        return total_multiplier


    def trigger_epic_drop(self, victory_level: int, grid: List[List[SymbolType]]) -> Dict:
        """Trigger Epic Drop based on victory level"""

        # Place fists randomly on the grid
        positions = []
        available_positions = [(r, c) for r in range(5) for c in range(4)]

        for _ in range(min(fist_count, len(available_positions))):
            pos = random.choice(available_positions)
            available_positions.remove(pos)
            positions.append(pos)

            # Place fist on grid
            fist_type = SymbolType.FIST_RED if random.random() < 0.5 else SymbolType.FIST_BLUE
            grid[pos[0]][pos[1]] = fist_type

        return {
            'fist_count': fist_count,
            'positions': positions,
            'victory_level': victory_level
        }

    def simulate_spin(self, game_state: GameState) -> SpinResult:
        """Simulate a complete spin"""
        # Generate base grid
        grid = self.spin_reels(game_state.in_bonus)

        # Check for scatter triggers
        scatter_count, bonus_type = self.check_scatter_trigger(grid)

        # Handle bonus triggers
        if scatter_count >= 3 and not game_state.in_bonus:
            game_state.in_bonus = True
            game_state.bonus_type = bonus_type
            game_state.bonus_spins_left = 10
            game_state.victory_level = 4 if bonus_type == "ULTIMATE_THROWDOWN" else self.count_my_fists(grid)
            if bonus_type == "THROWDOWN":
                if game_state.victory_level == 3:
                    self.satisfied['bonus_3FC_3x'] = True
                elif game_state.victory_level == 4:
                    self.satisfied['bonus_3FC_4x'] = True
                elif game_state.victory_level == 5:
                    self.satisfied['bonus_3FC_5x'] = True
            elif bonus_type == "ULTIMATE_THROWDOWN":
                self.satisfied['bonus_4FC'] = True
            game_state.victory_points = {'RED': 0, 'BLUE': 0}
            #print("Bonus win", bonus_type)

        # Handle retriggers during bonus
        elif scatter_count >= 2 and game_state.in_bonus:
            additional_spins = 4 if scatter_count >= 3 else 2
            game_state.bonus_spins_left += additional_spins
            #print("Bonus add spins", bonus_type, game_state.bonus_spins_left)

        # Calculate fist multipliers and wild reel expansions
        grid_orig = copy.deepcopy(grid)
        fist_activations = self.calculate_fist_multipliers(grid, game_state.selected_team)

        # Calculate victory points (only in bonus)
        epic_drops = []

        if game_state.in_bonus:

            # Check for epic drops (every 3 victory points)
            total_points = sum(game_state.victory_points.values())
            if total_points >= 3 and total_points % 3 == 0:
                epic_drop = self.trigger_epic_drop(game_state.victory_level, grid)
                epic_drops.append(epic_drop)
                game_state.victory_level += 1

                # Recalculate fist activations after epic drop
                fist_activations.extend(self.calculate_fist_multipliers(grid, game_state.selected_team))

        # Calculate payline wins
        wins = self.calculate_payline_wins(grid)

        # Apply fist multipliers
        total_win = sum(win['payout'] for win in wins)
        # Apply win cap !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        #total_win = min(total_win, self.max_win_limit)

        if fist_activations:
            multiplier = self.apply_fist_multipliers(wins, fist_activations)
            total_win *= multiplier
            game_state.fist_wild_win += multiplier

        # Update game state
        game_state.balance += total_win
        game_state.total_spins += 1

        if game_state.in_bonus:
            game_state.bonus_spins_left -= 1
            total_win *= game_state.victory_level
            if game_state.bonus_type == "THROWDOWN":
                game_state.THROWDOWN_win += game_state.victory_level
            else:
                game_state.U_THROWDOWN_win += game_state.victory_level

            #print("Bonus win", game_state.bonus_type, game_state.victory_level, total_win)
            if game_state.bonus_spins_left <= 0:
                game_state.in_bonus = False
                game_state.bonus_type = ""
                game_state.victory_level = 0

        if fist_activations.__len__() == 4 and total_win >= self.max_win_limit:
            self.satisfied['fists_4_more_max_win'] = True
        game_state.total_wins += total_win

        spin_result = SpinResult(
            grid=grid,
            grid_orig = grid_orig,
            wins=wins,
            total_win=total_win,
            wild_reel_activations=fist_activations,
            epic_drops=epic_drops
        )

        return spin_result

    @staticmethod
    def print_grids(spin, print_wins = False) -> None:
        def int_grid_print(grid) -> None:
            for row in range(4):
                row_symbols = [grid[reel][row].value for reel in range(5)]
                print(f"  {' | '.join(f'{sym:>8}' for sym in row_symbols)}")

        if spin.grid_orig is not None:
            print(f"ORIGINAL GRID: ")
            int_grid_print(spin.grid_orig)
        print(f"GRID: ")
        int_grid_print(spin.grid)

        print(f"  Win: x{spin.total_win:.2f}")
        if len(spin.wild_reel_activations) > 0:
            print(f"  Fist Activations: {len(spin.wild_reel_activations)}")
        else:
            print("\n")
        #        if reduce(lambda x, y: x + y, spin["victory_points"].values()) > 0:
        #            print(f"  Victory points: {spin['victory_points']}")
        #        else:
        #            print()
        if print_wins:
            for win in spin.wins:
                print(f"\t Line {win['payline']:2d} : {win['symbol'].name} x{win['count']} = {win['payout']} : {win['positions']}")

    def print_spin(self, epoch, spin) -> None:
        clear_console()
        print(f"\nSpin {spin['spin_number']:,} of {self.num_spins:,}, epoch: {epoch}, balance {self.game_state.balance:,.2f} :")
        print(f"SATISFIED: {self.satisfied}")
        self.print_grids(spin['spin'], print_wins=False)
        if spin['bonus_active']:
            print(f"  BONUS: {spin['bonus_type']}")
        else:
            print("\n")

    def run_simulation(self, epoch : int, rule, a_team : Team, a_fighter, a_opposite_fighter, num_spins: int, lines: int, bet: float = 1.0, initial_balance: float = 1000000.0) -> Dict:
        """Run a complete simulation"""
        self.num_spins = num_spins
        self.satisfied = copy.deepcopy(rule)
        self.max_win_limit = int(bet * self.max_win_times)
        if lines > len(self.paylines):
            raise ValueError(
                f"Selected lines {lines} bigger then paylines{self.paylines}"
            )

        if initial_balance < bet*lines:
            raise ValueError(
                f"Balance {initial_balance:,.2f} too low"
            )

        self.game_state = GameState(
            balance=initial_balance,
            lines = lines,
            bet=bet,
            selected_team=a_team,
            fighter= a_fighter,
            opposite_fighter= a_opposite_fighter,
            in_bonus=False,
            bonus_type="No bonus",
            bonus_spins_left=0,
            victory_level=0,
            total_spins=0,
            total_wins=0.0,
            reel_win=0.0,
            wild_win=0.0,
            fist_wild_win=0.0,
            THROWDOWN_win=0.0,
            U_THROWDOWN_win=0.0,
            max_win=0.0
        )

        results = {
            'spins': [],
            'statistics': {
                'total_spins': 0,
                'total_bet': 0.0,
                'total_win': 0.0,
                'bonus_triggers': 0,
                'epic_drops': 0,
                'max_win': 0.0,
                'rtp': 0.0,
                'hit_frequency': 0.0,
            }
        }

        winning_spins = 0
        wins = []
        results['epic_drops'] = 0

        def do_spin_internal(spin_num, wins, winning_spins):
            if self.game_state.balance < bet:
                return
            self.game_state.balance -= bet
            spin_result = self.simulate_spin(self.game_state)

            if spin_result.total_win > 0:
                winning_spins += 1

            wins.append(spin_result.total_win)
            # max one sping win
            if spin_result.total_win > self.game_state.max_win:
                self.game_state.max_win = spin_result.total_win
                self.max_win_spin = spin_result
            if spin_result.total_win >= self.max_win_limit:  # if we already overcome limit
                self.satisfied['max_win'] = True

            if spin_result.total_win > 3000.0:
                self.print_spin(epoch, {
                    'spin_number': spin_num + 1,
                    'spin' : spin_result,
                    'bonus_active': self.game_state.in_bonus,
                    'bonus_type': self.game_state.bonus_type
                })

            # Update statistics
            results['max_win'] = self.game_state.max_win
            if spin_result.epic_drops:
                results['epic_drops'] += len(spin_result.epic_drops)


            #print(f"============ SPING OVER win={spin_result.total_win} bonus => {self.game_state.bonus_type}: {self.game_state.bonus_spins_left} =================== ")

        if num_spins != TRY_OR_DIE:
            for spin_num in range(num_spins):
                do_spin_internal(spin_num, wins, winning_spins)
        else:
            num_spins = 1
            while not all(self.satisfied.values()):
                do_spin_internal(num_spins, wins, winning_spins)
                num_spins += 1

        # Final statistics
        total_bet = num_spins * bet
        mean_win = self.game_state.total_wins / num_spins
        variance = sum((win - mean_win) ** 2 for win in wins) / num_spins

        results.update({
            'total_spins': num_spins,
            'total_bet': total_bet,
            'total_win': self.game_state.total_wins * self.game_state.bet,
            'reel_win': self.game_state.reel_win,
            'wild_win': self.game_state.wild_win,
            'fist_wild_win': self.game_state.fist_wild_win,
            'THROWDOWN_win': self.game_state.THROWDOWN_win,
            'U_THROWDOWN_win': self.game_state.U_THROWDOWN_win,
            'rtp': (self.game_state.total_wins / total_bet) * 100 if total_bet > 0 else 0,
            'hit_frequency': (winning_spins / num_spins) * 100 if num_spins > 0 else 0,
            'rmsm_volatility' : math.sqrt(variance),
            'max_win' : self.game_state.max_win,
            'max_win_spin' : self.max_win_spin,
        })

        return results
