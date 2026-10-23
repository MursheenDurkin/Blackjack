# Blackjack

A terminal Blackjack game built in Python with colored card art, chip betting, double down, and session statistics.

## Features

- **Colored ASCII Card Art**: Box-drawing card borders with red Hearts/Diamonds and white Clubs/Spades
- **Chip Betting System**: Start with 1,000 chips, place bets each hand, try to grow your stack
- **Double Down**: Double your bet on the first two cards for one extra card
- **Blackjack Pays 3:2**: Natural 21 earns 1.5x your bet
- **Proper Dealer AI**: Dealer hits on 16 and below, stands on 17+
- **Session Statistics**: Tracks hands played, win rate, biggest win, peak chips, and final profit/loss
- **Auto-Reshuffle**: Deck automatically reshuffles when it runs low
- **Clean Interface**: Clear-screen transitions, formatted results, and colored feedback

## Preview

```
    ╔═══════════════════════════════════╗
    ║       B L A C K J A C K           ║
    ║      Terminal Card Game           ║
    ╚═══════════════════════════════════╝

  Chips: 1000    Bet: 100
  ─────────────────────────────────────────────

  DEALER
  ┌───────┐ ┌───────┐
  │K      │ │▒▒▒▒▒▒▒│
  │       │ │▒▒▒▒▒▒▒│
  │   ♠   │ │▒▒▒▒▒▒▒│
  │       │ │▒▒▒▒▒▒▒│
  │      K│ │▒▒▒▒▒▒▒│
  └───────┘ └───────┘
  Value: 10 + ?

  YOUR HAND
  ┌───────┐ ┌───────┐
  │A      │ │9      │
  │       │ │       │
  │   ♥   │ │   ♣   │
  │       │ │       │
  │      A│ │      9│
  └───────┘ └───────┘
  Value: 20

  [H]it | [S]tand | [D]ouble
```

## Requirements

- Python 3.7+
- **colorama** (optional, the game works without it, just no colors)

## Getting Started

1. **Clone the repository:**
   ```bash
   git clone https://github.com/MursheenDurkin/Blackjack.git
   cd Blackjack
   ```

2. **Install dependencies** (optional, for colored output):
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the game:**
   ```bash
   python blackjack.py
   ```

## How to Play

1. You start with **1,000 chips** and a minimum bet of **10**
2. Place your bet at the start of each hand
3. You and the dealer each receive two cards (one of the dealer's is hidden)
4. Choose to **Hit** (draw a card), **Stand** (keep your hand), or **Double Down** (double your bet, draw one card)
5. Try to get as close to **21** as possible without going over
6. The dealer reveals their hidden card and draws to 17
7. Closest to 21 wins, bust over 21 and you lose automatically

## Rules

| Rule | Detail |
|------|--------|
| Blackjack | Ace + 10-value card on initial deal, pays 3:2 |
| Ace value | Counts as 11, automatically adjusts to 1 if hand would bust |
| Dealer | Must hit on 16 and below, stands on 17+ |
| Double Down | Available on first two cards if you have enough chips |
| Push | Tie returns your bet |

## Project Structure

```
Blackjack/
├── blackjack.py        # Main game file
├── requirements.txt    # Python dependencies
├── .gitignore
└── README.md
```
