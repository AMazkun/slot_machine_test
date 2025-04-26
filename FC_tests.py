import math
import random

# SLOT MACHINE SETUP
# FRUIT COCKTAIL
from FC import symbols, paytable, paylines, ROWS, COLS, wild, NUM_PAYLINES

population = []

# зробити барабан
def make_population():
    for symbol, probability in symbols.items():
        population.extend([symbol] * int(probability * 200))  # Створюємо "пул" символів
    random.shuffle(population)

# SPIN GENERATION
def згенерувати_комбінацію(кількість_барабанів=5):
    """Генерує випадкову комбінацію символів на барабанах."""
    return [random.choice(population) for _ in range(кількість_барабанів)]

def подивитися_виграш_символу(символ, попередній_виграш, кількість_однакових):
    if кількість_однакових in paytable.get(символ, {}):
        return max(попередній_виграш, paytable[символ][кількість_однакових])
    else:
        return попередній_виграш

# CALC WIN
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
    кількість_однакових = 1
    поточний_символ = комбінація[0]
    for i in range(1, len(комбінація)):
        if поточний_символ == wild:
            поточний_символ = комбінація[i]
        if комбінація[i] == wild or комбінація[i] == поточний_символ:
            кількість_однакових += 1
        else:
            виграш = подивитися_виграш_символу(поточний_символ, виграш, кількість_однакових)
            кількість_однакових = 1
            поточний_символ = комбінація[i]

    # Перевірити у кінці
    виграш = подивитися_виграш_символу(поточний_символ, виграш, кількість_однакових)
    # Додаємо комбінації виключно з диких символів
    if кількість_однакових != COLS or поточний_символ != wild: # щоб повторно не добавляти лише одну комбінацію з дикого символа
        виграш += wild_combination_win(комбінація)
    return виграш

# STATIC ANALYSES
# Перевірка правильності таблиці вірогідностей
def check_total_symbol_probabylity():
    total_probability = 0
    for key in symbols.keys():
        total_probability += symbols[key]

    print(f"Перевірка загальної вірогідності: {total_probability}")


# Перевірка таблиці виграшів
# Розрахунок загального середнього виграшу
def calculate_expected_payout(payouts, probabilities):
    expected_payout = 0
    for symbol, prob in probabilities.items():
        wild_probability = probabilities[wild] if symbol != wild else 0
        if symbol in payouts:
            for match_count, payout in payouts[symbol].items():
                prob_corrected = prob + wild_probability
                total_prob = pow(prob_corrected, match_count) * pow(1 - prob_corrected, COLS - match_count)
                #correction = 1 if match_count == COLS else (COLS - match_count + 1) / кількість_барабанів
                #total_prob *= correction
                correction = 1
                combination_payout = total_prob * payout * (COLS - match_count + 1)
                print(f"{symbol} of {match_count}, prob+wild {prob_corrected:.2f}, total_prob {total_prob:.6f}, correction: {correction}, payout: {combination_payout:.6f}")
                expected_payout += combination_payout
        print()
    return expected_payout

def check_machine_tables():
    check_total_symbol_probabylity()
    # Виконання розрахунку загального середнього виграшу
    average_payout = calculate_expected_payout(paytable, symbols)
    print(f"Очикуваний середній виграш: {average_payout:.4f}")
    #input("Press Enter to continue...\n")
    return average_payout

def simple_test_01():
    комбінація = ['🍹', '🍉', '🍉', '🍉', '🍹']
    win = визначити_виграш(комбінація)
    print(f" {комбінація} : {win}")

    комбінація = ['🍹', '🍹', '🍉', '🍉', '🍉']
    win = визначити_виграш(комбінація)
    print(f" {комбінація} : {win}")

    комбінація = ['🍉', '🍉', '🍉', '🍹', '🍹']
    win = визначити_виграш(комбінація)
    print(f" {комбінація} : {win}")

    комбінація = ['🍹', '🍉', '🍉', '🍉', '🍐']
    win = визначити_виграш(комбінація)
    print(f" {комбінація} : {win}")

    комбінація = ['🍐', '🍉', '🍉', '🍉', '🍹']
    win = визначити_виграш(комбінація)
    print(f" {комбінація} : {win}")

    комбінація = ['🍉', '🍉', '🍉', '🍐', '🍐']
    win = визначити_виграш(комбінація)
    print(f" {комбінація} : {win}")

    комбінація = ['🍐', '🍉', '🍉', '🍉', '🍐']
    win = визначити_виграш(комбінація)
    print(f" {комбінація} : {win}")

    комбінація = ['🍐', '🍐', '🍉', '🍉', '🍉']
    win = визначити_виграш(комбінація)
    print(f" {комбінація} : {win}")

    exit(0)


# TESTS SETUP
test_iterations = 2
баланс = 1000000
ставка_на_спін = 1
show_wins = 0

if __name__ == "__main__":

    make_population() # Зробити барабан

    average_payout = check_machine_tables()
    #simple_test_01()
    print("-" * 25)

    # Приклад симуляції кількох обертань
    загальний_виграш_ = 0
    сумма_ставок_ = 0

    print(f"\nSIMULATING : {test_iterations} tests with {баланс} client balans")

    for i in range(test_iterations):
        print("Please wait ...")

        #STATISTICS
        zeros_couter = 0
        wins_list =[]
        поточний_баланс = баланс
        загальний_виграш = 0
        сумма_ставок = 0
        спін = 0

        while поточний_баланс > 0:
            поточний_баланс -= ставка_на_спін
            сумма_ставок += ставка_на_спін
            спін += 1
            комбінація = згенерувати_комбінацію()

            виграш_за_спін = визначити_виграш(комбінація) * ставка_на_спін
            загальний_виграш += виграш_за_спін
            поточний_баланс  += виграш_за_спін
            if виграш_за_спін > 0:
                wins_list.append(виграш_за_спін)
            else:
                zeros_couter += 1

            if show_wins and виграш_за_спін > 500:
                print(f"Спін: {спін}  {комбінація}, win: {виграш_за_спін}")

        #print(f"\nСтавка на спін {ставка_на_спін}")
        print(f"\nИтерация {i}\n=============")
        print(f"\nЗа {спін} спинів та {сумма_ставок} ставок загальний виграш склав: {загальний_виграш} кредитів.")

        # STATISTIC CALC
        загальний_виграш_ += загальний_виграш
        сумма_ставок_ += сумма_ставок

        arithmetic_mean = загальний_виграш / спін
        variance_of_wins = zeros_couter * arithmetic_mean * arithmetic_mean
        for val in wins_list:
            variance_of_wins += (val - arithmetic_mean) ** 2

        variance_of_wins = math.sqrt (variance_of_wins / (спін - 1))
        max_win = max(wins_list)
        attraction = max_win / variance_of_wins
        hit_frequency = len(wins_list) / спін

        dirty_income = сумма_ставок - загальний_виграш
        # Показники повернення гравцеві (RTP): Theoretical RTP / Actual RTP
        print(f"Очикуваний середній виграш за ставку: {average_payout:.4f} реально: {(загальний_виграш / сумма_ставок):.4f}")
        print(f"hit frequency: {hit_frequency : .4f}")
        print(f"dirty income: {dirty_income}")

        print(f"arithmetic mean: {arithmetic_mean:.6f}  variance of wins: {variance_of_wins:.4f}")
        print(f"maximum one-time win: {max_win} attration: {attraction:.2f}")


        # OTHER
        """
        Середня тривалість ігрової сесії (Average Session Length): 
        Середня кількість спинів або час
        Середня ставка на спін (Average Bet per Spin): 
        Максимальна та мінімальна ставка (Maximum and Minimum Bet): 
        Час затримки (Latency): Час між дією гравця (натисканням кнопки "пуск") та відображенням результату.
        Помилки та збої (Errors and Bugs): 
        """

        print("====================================\n\n")


    print(f"\nGRAND TOTAL:\n====================")
    print(f"Середня реальна видача: {(загальний_виграш_ / сумма_ставок_):.4f}")
    print(f"")

