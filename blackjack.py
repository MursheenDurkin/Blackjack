#!/usr/bin/env python3
"""
Blackjack - A terminal card game with betting, colored cards, and statistics.
Features: Chip betting, double down, colored suit display, session statistics.
"""

import random
import os
import time

# ─── Color Setup (graceful fallback if colorama not installed) ────────────────

try:
    from colorama import Fore, Style, init
    init(autoreset=True)
except ImportError:
    class _NoColor:
        """Stub so the game works without colorama — just no colors."""
        def __getattr__(self, _):
            return ""
    Fore = Style = _NoColor()

# ─── Constants ────────────────────────────────────────────────────────────────

TITLE = f"""{Fore.CYAN}
    ╔═══════════════════════════════════╗
    ║       B L A C K J A C K           ║
    ║      Terminal Card Game           ║
    ╚═══════════════════════════════════╝{Style.RESET_ALL}"""

SUITS = ["Hearts", "Diamonds", "Clubs", "Spades"]
RANKS = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
SUIT_SYMBOLS = {"Hearts": "♥", "Diamonds": "♦", "Clubs": "♣", "Spades": "♠"}

STARTING_CHIPS = 1000
MIN_BET = 10

# ─── Utility Functions ────────────────────────────────────────────────────────

def clear():
    """Clear the terminal screen."""
    os.system("cls" if os.name == "nt" else "clear")


def divider(width=45):
    """Print a horizontal divider."""
    print(f"  {Fore.CYAN}{'─' * width}{Style.RESET_ALL}")


def header(text, width=45):
    """Print a formatted section header."""
    print(f"\n  {Fore.CYAN}{'─' * width}")
    print(f"    {text}")
    print(f"  {'─' * width}{Style.RESET_ALL}")

# ─── Deck & Card Functions ───────────────────────────────────────────────────

def create_deck():
    """Create and shuffle a standard 52-card deck."""
    deck = [(rank, suit) for rank in RANKS for suit in SUITS]
    random.shuffle(deck)
    return deck


def card_value(rank):
    """Return the point value of a single card rank."""
    if rank in ("J", "Q", "K"):
        return 10
    if rank == "A":
        return 11
    return int(rank)


def hand_value(hand):
    """Calculate hand total, adjusting Aces from 11 to 1 as needed."""
    total = sum(card_value(r) for r, _ in hand)
    aces = sum(1 for r, _ in hand if r == "A")
    while total > 21 and aces:
        total -= 10
        aces -= 1
    return total


def is_blackjack(hand):
    """Check if a two-card hand is a natural 21."""
    return len(hand) == 2 and hand_value(hand) == 21

# ─── Card Display ────────────────────────────────────────────────────────────

def card_art(rank, suit, hidden=False):
    """Return 7 lines of ASCII art for one card."""
    if hidden:
        return [
            "┌───────┐",
            "│▒▒▒▒▒▒▒│",
            "│▒▒▒▒▒▒▒│",
            "│▒▒▒▒▒▒▒│",
            "│▒▒▒▒▒▒▒│",
            "│▒▒▒▒▒▒▒│",
            "└───────┘",
        ]
    sym = SUIT_SYMBOLS[suit]
    color = Fore.RED if suit in ("Hearts", "Diamonds") else Fore.WHITE
    r = Style.RESET_ALL
    return [
        f"{color}┌───────┐{r}",
        f"{color}│{rank:<2}     │{r}",
        f"{color}│       │{r}",
        f"{color}│   {sym}   │{r}",
        f"{color}│       │{r}",
        f"{color}│     {rank:>2}│{r}",
        f"{color}└───────┘{r}",
    ]


def show_hand(hand, label, hide_second=False):
    """Display a hand of cards side-by-side with a value line."""
    print(f"\n  {Fore.CYAN}{label}{Style.RESET_ALL}")
    arts = []
    for i, (rank, suit) in enumerate(hand):
        if hide_second and i == 1:
            arts.append(card_art(rank, suit, hidden=True))
        else:
            arts.append(card_art(rank, suit))
    for row in range(7):
        print("  " + " ".join(art[row] for art in arts))
    if not hide_second:
        val = hand_value(hand)
        if val > 21:
            color = Fore.RED
        elif val == 21:
            color = Fore.GREEN
        else:
            color = Fore.WHITE
        print(f"  {color}Value: {val}{Style.RESET_ALL}")
    else:
        print(f"  Value: {card_value(hand[0][0])} + ?")


def show_table(player, dealer, hide_dealer=True, chips=None, bet=None):
    """Render the full table: title, chip info, both hands."""
    clear()
    print(TITLE)
    if chips is not None:
        print(f"  {Fore.YELLOW}Chips: {chips}{Style.RESET_ALL}    "
              f"{Fore.WHITE}Bet: {bet}{Style.RESET_ALL}")
        divider()
    show_hand(dealer, "DEALER", hide_second=hide_dealer)
    show_hand(player, "YOUR HAND")

# ─── Game Logic ───────────────────────────────────────────────────────────────

def get_bet(chips):
    """Prompt the player for a valid bet amount."""
    while True:
        try:
            raw = input(f"\n  Place your bet ({MIN_BET}-{chips}): ").strip()
            bet = int(raw)
            if MIN_BET <= bet <= chips:
                return bet
            print(f"  {Fore.RED}Bet must be between {MIN_BET} and {chips}.{Style.RESET_ALL}")
        except ValueError:
            print(f"  {Fore.RED}Enter a number.{Style.RESET_ALL}")


def player_turn(deck, player, dealer, chips, bet):
    """
    Handle the player's turn (hit / stand / double down).
    Returns (hand, final_bet, busted).
    """
    while True:
        show_table(player, dealer, hide_dealer=True, chips=chips, bet=bet)
        val = hand_value(player)

        if val >= 21:
            return player, bet, val > 21

        options = ["[H]it", "[S]tand"]
        can_double = len(player) == 2 and chips >= bet * 2
        if can_double:
            options.append("[D]ouble")
        print(f"\n  {' | '.join(options)}")

        choice = input(f"  {Fore.CYAN}> {Style.RESET_ALL}").strip().lower()

        if choice in ("h", "hit"):
            player.append(deck.pop())

        elif choice in ("s", "stand"):
            return player, bet, False

        elif choice in ("d", "double") and can_double:
            bet *= 2
            player.append(deck.pop())
            show_table(player, dealer, hide_dealer=True, chips=chips, bet=bet)
            time.sleep(0.5)
            return player, bet, hand_value(player) > 21

        else:
            print(f"  {Fore.RED}Invalid choice.{Style.RESET_ALL}")
            time.sleep(0.5)


def dealer_turn(deck, dealer, player, chips, bet):
    """Reveal the dealer's hand and draw to 17."""
    show_table(player, dealer, hide_dealer=False, chips=chips, bet=bet)
    time.sleep(0.8)

    while hand_value(dealer) < 17:
        dealer.append(deck.pop())
        show_table(player, dealer, hide_dealer=False, chips=chips, bet=bet)
        print(f"\n  {Fore.YELLOW}Dealer hits...{Style.RESET_ALL}")
        time.sleep(0.8)

    dv = hand_value(dealer)
    if dv <= 21:
        print(f"\n  {Fore.YELLOW}Dealer stands on {dv}.{Style.RESET_ALL}")
        time.sleep(0.5)


def resolve(player, dealer, bet, player_bj):
    """Determine outcome. Returns (message, chip_payout)."""
    pv = hand_value(player)
    dv = hand_value(dealer)
    dealer_bj = is_blackjack(dealer)

    if player_bj and dealer_bj:
        return "Push — both have Blackjack!", 0
    if player_bj:
        return "BLACKJACK! Pays 3:2!", int(bet * 1.5)
    if dealer_bj:
        return "Dealer has Blackjack!", -bet
    if pv > 21:
        return "Bust! You lose.", -bet
    if dv > 21:
        return "Dealer busts! You win!", bet
    if pv > dv:
        return "You win!", bet
    if dv > pv:
        return "Dealer wins.", -bet
    return "Push — it's a tie!", 0


def play_hand(deck, chips, stats):
    """Play a single hand of Blackjack. Returns updated chip count."""
    # Reshuffle when deck runs low
    if len(deck) < 15:
        deck.clear()
        deck.extend(create_deck())

    clear()
    print(TITLE)
    print(f"  {Fore.YELLOW}Chips: {chips}{Style.RESET_ALL}\n")

    bet = get_bet(chips)

    # Deal initial cards
    player = [deck.pop(), deck.pop()]
    dealer = [deck.pop(), deck.pop()]

    player_bj = is_blackjack(player)
    busted = False

    if not player_bj:
        player, bet, busted = player_turn(deck, player, dealer, chips, bet)

    # Dealer plays unless player busted
    if not busted and not player_bj:
        dealer_turn(deck, dealer, player, chips, bet)
    elif player_bj:
        # Just reveal the dealer's cards
        show_table(player, dealer, hide_dealer=False, chips=chips, bet=bet)
        time.sleep(0.5)

    # Final reveal
    show_table(player, dealer, hide_dealer=False, chips=chips, bet=bet)

    msg, payout = resolve(player, dealer, bet, player_bj)

    # Display result
    if payout > 0:
        print(f"\n  {Fore.GREEN}{'═' * 38}")
        print(f"    {msg}  (+{payout} chips)")
        print(f"  {'═' * 38}{Style.RESET_ALL}")
        stats["won"] += 1
        stats["biggest_win"] = max(stats["biggest_win"], payout)
    elif payout < 0:
        print(f"\n  {Fore.RED}{'═' * 38}")
        print(f"    {msg}  ({payout} chips)")
        print(f"  {'═' * 38}{Style.RESET_ALL}")
        stats["lost"] += 1
    else:
        print(f"\n  {Fore.YELLOW}{'═' * 38}")
        print(f"    {msg}")
        print(f"  {'═' * 38}{Style.RESET_ALL}")
        stats["pushed"] += 1

    stats["played"] += 1
    new_chips = chips + payout
    stats["peak"] = max(stats["peak"], new_chips)
    return new_chips


def show_final_stats(stats, chips):
    """Display end-of-session statistics."""
    played = stats["played"]
    rate = f"{stats['won'] / played * 100:.0f}%" if played > 0 else "N/A"
    header("SESSION STATISTICS")
    print(f"""
  Hands Played  : {Fore.WHITE}{played}{Style.RESET_ALL}
  Wins          : {Fore.GREEN}{stats['won']}{Style.RESET_ALL}
  Losses        : {Fore.RED}{stats['lost']}{Style.RESET_ALL}
  Pushes        : {Fore.YELLOW}{stats['pushed']}{Style.RESET_ALL}
  Win Rate      : {Fore.CYAN}{rate}{Style.RESET_ALL}
  Biggest Win   : {Fore.GREEN}+{stats['biggest_win']} chips{Style.RESET_ALL}
  Peak Chips    : {Fore.YELLOW}{stats['peak']}{Style.RESET_ALL}
  Final Chips   : {Fore.CYAN}{chips}{Style.RESET_ALL}
""")

# ─── Entry Point ──────────────────────────────────────────────────────────────

def main():
    """Main game loop."""
    stats = {
        "played": 0, "won": 0, "lost": 0, "pushed": 0,
        "biggest_win": 0, "peak": STARTING_CHIPS,
    }
    chips = STARTING_CHIPS
    deck = create_deck()

    try:
        clear()
        print(TITLE)
        print(f"  You start with {Fore.YELLOW}{STARTING_CHIPS}{Style.RESET_ALL} chips.")
        print(f"  Minimum bet: {Fore.WHITE}{MIN_BET}{Style.RESET_ALL}")
        print(f"\n  Rules: Dealer stands on 17. Blackjack pays 3:2.")
        print(f"  Double down available on your first two cards.\n")
        input(f"  Press {Fore.CYAN}Enter{Style.RESET_ALL} to play... ")

        while chips >= MIN_BET:
            chips = play_hand(deck, chips, stats)

            if chips < MIN_BET:
                print(f"\n  {Fore.RED}Out of chips! Game over.{Style.RESET_ALL}")
                break

            print(f"\n  {Fore.CYAN}Chips: {chips}{Style.RESET_ALL}")
            again = input(f"\n  Play again? [Y/n]: ").strip().lower()
            if again in ("n", "no"):
                break

        # Session summary
        clear()
        show_final_stats(stats, chips)
        profit = chips - STARTING_CHIPS
        if profit > 0:
            print(f"  {Fore.GREEN}Profit: +{profit} chips!{Style.RESET_ALL}")
        elif profit < 0:
            print(f"  {Fore.RED}Loss: {profit} chips.{Style.RESET_ALL}")
        else:
            print(f"  {Fore.YELLOW}Broke even!{Style.RESET_ALL}")
        print(f"\n  {Fore.CYAN}Thanks for playing Blackjack!{Style.RESET_ALL}\n")

    except KeyboardInterrupt:
        print(f"\n\n  {Fore.CYAN}Thanks for playing!{Style.RESET_ALL}\n")


if __name__ == "__main__":
    main()
