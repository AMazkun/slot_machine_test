import json
from typing import Dict
import datetime

from FOD_SIM import FistOfDestructionEmulator
from FOD_SIM import Team, SymbolType, SpinResult, SATISFY_RULE

TARGET_OVERALL_RTP = 98.00

class ResultEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, SymbolType):
            return obj.value  # Convert Enum to string
        if isinstance(obj, SpinResult):
            return obj.to_json()
        return super().default(obj)

def iteration(exhaustive_num_spins, epoch, lines, bet) -> (bool, Dict):
    print(f"\n=== SAMPLE SPINS ===")
    results = emulator.run_simulation(epoch, rule=SATISFY_RULE,
                                      a_team=Team.RED, a_fighter=SymbolType.RED_FIGHTER_MAN,
                                      a_opposite_fighter = SymbolType.BLUE_FIGHTER_WOMAN,
                                      initial_balance=exhaustive_num_spins,
                                      num_spins=exhaustive_num_spins, lines=lines, bet=bet)
    return all(emulator.satisfied.values()) , results

def print_summary_statistics(results) -> None:
    # Print summary statistics
    total_win = results['total_win']
    print(f"\n\n=== SIMULATION RESULTS ===")
    print(f"Total Spins:  {results['total_spins']:,} final balance ${emulator.game_state.balance:,.2f}")
    print(f"Total Bet: $ {results['total_bet']:,.2f}")
    print(f"Total Win: \t\t\t${total_win:,.2f}")
    print(f"Total wild_win: \t$ {results['wild_win']:,.2f} \tof {(results['wild_win'] / total_win * 100.0):.2f} %")
    print(f"Total fist_wild_win: \t$ {results['fist_wild_win']:,.2f} \tof {(results['fist_wild_win'] / total_win * 100):.2f} %")
    print(f"Total bonus_THROWDOWN: \t$ {results['THROWDOWN_win']:,.2f} \tof {(results['THROWDOWN_win'] / total_win * 100):.2f} %")
    print(f"Total ULTIMA_THROWDOWN: \t$ {results['U_THROWDOWN_win']:,.2f} \tof {(results['U_THROWDOWN_win'] / total_win * 100):.2f} %")
    print(f"RTP:  {results['rtp']:.2f}%")
    print(f"Hit Frequency:  {results['hit_frequency']:.2f}%")
    print(f"Max Win: $ {results['max_win']:,.2f} ( {results['max_win']:.2f}x bet)")
    print(f"Epic Drops:  {results['epic_drops']}")

    # Test theoretical calculations
    print(f"\n=== THEORETICAL VALIDATION ===")
    print(f"Target RTP: {TARGET_OVERALL_RTP:.2f}%")
    print(f"Actual RTP:  {results['rtp']:.2f}%")
    print(f"Difference: {abs(TARGET_OVERALL_RTP - results['rtp']):.2f}%")
    print(f"Target Hit Frequency: ~23%")
    print(f"RMSM volatility:  {results['rmsm_volatility']:.4f}")
    print(f"Actual Hit Frequency:  {results['hit_frequency']:.2f}%")
    print(f"Max Win Cap: 10,000x (${10000 * 1.0:,.2f} at $1 bet)")
    print(f"Achieved Max Win:  {results['max_win']:,.2f}x")
    print(f"Max Win GRID:\n")
    emulator.print_grids(results['max_win_spin'], print_wins = True)
    print(f"======================================================\n")

def to_stable():
    max_win = 10000
    lines = 40
    bet = 1.0
    exhaustive_num_spins = 14_000_000
    epoch = 1
    max_win_stable = 0

    results = []
    while max_win_stable < 5:
        # Run a simulation
        print("\tRunning Fist of Destruction simulation... iteration : ")
        # Show some example spins
        stable, result = iteration(exhaustive_num_spins, epoch, lines, bet)
        if stable:
            max_win_stable += 1
            results.append(result)
        else:
            exhaustive_num_spins += 500_000
            max_win_stable = 0

        epoch += 1

    print("\nEMULATION FINISHED")
    print(f"\n\nSTABLE ACHIVED at {exhaustive_num_spins:,}")

    for result in results:
        print("\n\n")
        print_summary_statistics(result)

    now = datetime.datetime.now()
    unique_filename = "FOD_SIM_" + now.strftime("%Y%m%d_%H%M%S") + ".txt"
    with open(unique_filename, "w") as file:
        json.dump(results, file, cls=ResultEncoder,  indent=2)

def once():

    lines = 40
    bet = 1.0
    exhaustive_num_spins = 30_000_000
    epoch = 1

    print("\tRunning Fist of Destruction simulation... iteration : ")
    stable, result = iteration(exhaustive_num_spins, epoch, lines, bet)
    if stable:
        print("\n\tStable reached")
    else:
        print("\n\tStable not reached")

    print_summary_statistics(result)

    now = datetime.datetime.now()
    unique_filename = "FOD_SIM_ONCE_" + now.strftime("%Y%m%d_%H%M%S") + ".txt"
    with open(unique_filename, "w") as file:
        json.dump(result, file, cls=ResultEncoder,  indent=2)

# Example usage and testing
import time
if __name__ == "__main__":
    emulator = FistOfDestructionEmulator()
    start_timestamp = time.time()
    start_datetime = datetime.datetime.fromtimestamp(start_timestamp)

    # TESTS
    once()
    #to_stable()

    end_timestamp = time.time()
    end_datetime = datetime.datetime.fromtimestamp(end_timestamp)
    print(f":: TEST BEGAN: {start_datetime.strftime('%Y-%m-%d %H:%M:%S')} ENDS: {end_datetime.strftime('%Y-%m-%d %H:%M:%S')}")

    duration_seconds = end_timestamp - start_timestamp
    total_seconds_int = int(duration_seconds)
    hours = total_seconds_int // 3600
    minutes = (total_seconds_int % 3600) // 60
    seconds = total_seconds_int % 60
    milliseconds = int((duration_seconds - total_seconds_int) * 1000)
    print(f"::\tDURATION: {hours} h {minutes} min {seconds} sec {milliseconds} mc")
