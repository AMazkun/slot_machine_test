# 🎰 Real Money Slot Machine Simulators

This repository contains two high-performance emulators for real-money slot machines:

- 🍓 `FruitCocktail/` — A simulator of the classic Fruit Cocktail slot game.
- 🥊 `FistOfDestruction/` — A detailed emulator of Hacksaw Gaming’s modern hit, Fist of Destruction.

These simulators are designed for statistical research, probability modeling, and testing of rare in-game events such as bonus features, win limits, and payout distributions.

---

## 🎯 Purpose

These tools serve as research-grade simulators for slot game developers, crypto gaming analysts, and mathematicians. With them, you can:

- Run large-scale spin simulations
- Analyze RTP (Return to Player) and volatility
- Trigger and verify rare features or max payout events
- Bypass artificial limits for raw statistical exploration
- Reduce empirical validation time dramatically

---

## 🔍 Fist of Destruction Emulator

Inspired by the original game by [Hacksaw Gaming](https://www.hacksawgaming.com/games/fist-of-destruction), this emulator:

- 5x4 reel layout
- Removes the max win limit for full analysis
- Verifies appearance of all bonus features (Throwdown!, Ultimate Throwdown!)
- Tests for stability across 5+ consecutive iterations
- Achieved RTP ~98% after only 8.5 million spins
- Manufecture per sping limitation is **10,000x**
- Observed a max payout of **101,080×** the base bet

## 🍓 Fruit Cocktail Emulator

A faithful reimplementation of the beloved retro slot. This simulator includes:

- Classic 5x3 reel layout
- Configurable reel strips and symbols
- Bonus round detection
- Full payout evaluation logic
- RTP and payout curve simulation tools



🎯 “Slot simulations aren’t about luck. They’re about modeling probability, optimizing logic, and mastering the math behind the spin.”
— The Creator