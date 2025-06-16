# 🎰 Fist of Destruction Statistics Smulator

Welcome to the Fist of Destruction, a simulation tool built to analyze one of the most iconic slot games from Hacksaw Gaming. This game has captured the interest of crypto traders and electronic casino service providers alike, and this emulator aims to uncover its deepest statistical mechanics.

Based on 
[hacksawgaming.com](https://www.hacksawgaming.com/games/fist-of-destruction)


![Game View](_res/FOD_face.jpeg)

⸻
## Disclamer

In more then 8 houres form exhaustive_num_spins = 14_000_000
ALL all testing conditions began to be met, namely: 
1. Exceeding the maximum winning limit per spin
2. Dropping out the 3xFC symbol bonus from 3 to 5 multiplication
3. Dropping out 3xFC symbol bonus
4. Dropping out 4 Fists with exceeding the maximum winning limit per spin

**Spin 21,832,342 of 22,000,000, epoch: 18, balance 21,449,568.90 :**

**SATISFIED: {'max_win': True, 'bonus_3FC_3x': True, 'bonus_3FC_4x': True, 'bonus_3FC_5x': True, 'bonus_4FC': True, 'fists_4_more_max_win': True}**


## 🔍 Purpose
The emulator is designed to find the point at which all the conditions for the appearance of the rarest events of the game are met, namely, exceeding the winning limit of one spin of the drum and the loss of all bonus games.

After finding this point, the emulator checks that the conditions are maintained continuously for at least the next five iterations, in this case we can be sure that the obtained empirical data will not differ much from subsequent games.

This allows us to reduce the testing period and empirical determination of the percentage of the machine's payout.

Because for a simple analysis of the probability for the loss of all combinations at least once, more than 520,000,000 spins of the drum are needed, which is long enough with the help of such an algorithm, it is possible to reduce the process of empirical calculation of the game parameters to what is visible in this case 8.5 million spins of the drumWe checked whether the machine would be in the range of no more than 98% of the issue.

Despite the fact that game manufacturers limit the winnings of one spin due to the fear of going into the minus at the first issue, we, as real mathematicians, are not afraid of such events and therefore the emulator has disabled the limit on the maximum win per spin of the drum, so the game showed a win of 101080 times, which you can see in the emulation results.

This emulator is designed to:
- Identify extreme edge conditions, such as the appearance of rare bonus rounds and maximum win events.
- Validate consistency of these outcomes over multiple iterations.
- Empirically approximate key slot parameters such as RTP (Return To Player) with high efficiency.

⸻

## 🎯 Key Features
- ✅ Simulation of full game mechanics including bonus rounds, wild features, and maximum payout conditions.
- ✅ Detection of the payout threshold breach (e.g., one-spin win exceeding manufacturer-set limits).
- ✅ Stability check over five consecutive iterations to ensure statistical reliability.
- ✅ No maximum win cap to allow unbounded analysis of outlier payouts.
- ✅ Designed to reduce the number of spins required to analyze full game distribution from hundreds of millions to ~8.5 million.

⸻



With this emulator:
- You get accelerated convergence of key metrics.
- You can empirically validate payout percentage (~98% target zone) without needing full-scale industrial simulations.
- You get insight into unrestricted game behavior—including rare jackpot-scale wins (e.g., 101,080× payout observed).

⸻

## ⚙️ How It Works
1.	Simulates standard and bonus spins of the Fist of Destruction game.
2.	Monitors for:
	- Rare event triggers (e.g., Throwdown!, Ultimate Throwdown!).
	- Payout exceeding limits set by the original provider.
3.	After detecting such a point, verifies that:
	- Similar behavior continues for at least 5 iterations.
4.	Collects and logs statistical results to support further RTP and variance analysis.
