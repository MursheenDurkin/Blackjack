import random
# from colorama import Fore, Style # Uncomment if you install colorama

# ASCII Art templates for cards
# We'll use a dictionary for suits to get special characters
SUIT_SYMBOLS = {
    'Hearts': '♥',
    'Diamonds': '♦',
    'Clubs': '♣',
    'Spades': '♠'
}

CARD_TEMPLATE = [
    "+-------+",
    "| {}     |",
    "|       |",
    "|   {}   |",
    "|       |",
    "|     {} |",
    "+-------+"
]

def create_deck():
    """
    Creates a standard deck of 52 playing cards.
    Each card is represented as a tuple: (rank, suit).
    """
    suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
    ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']
    deck = [(rank, suit) for rank in ranks for suit in suits]
    return deck

def shuffle_deck(deck):
    """Shuffles the given deck of cards in-place."""
    random.shuffle(deck)

def deal_card(deck):
    """Deals a single card from the deck."""
    if not deck:
        print("Reshuffling the deck!")
        deck.extend(create_deck()) # Add new cards if deck is empty
        shuffle_deck(deck)
    return deck.pop() # Removes and returns the last item

def get_card_value(card):
    """
    Returns the numerical value of a card.
    Handles face cards (Jack, Queen, King) as 10 and Ace as 11 (initially).
    """
    rank = card[0]
    if rank in ['Jack', 'Queen', 'King']:
        return 10
    elif rank == 'Ace':
        return 11 # Ace is initially 11, handled later for 1 if needed
    else:
        return int(rank)

def calculate_hand_value(hand):
    """
    Calculates the total value of a hand, handling Aces (1 or 11).
    """
    value = 0
    num_aces = 0
    for card in hand:
        card_value = get_card_value(card)
        value += card_value
        if card[0] == 'Ace':
            num_aces += 1

    # Adjust for Aces if hand value is over 21
    while value > 21 and num_aces > 0:
        value -= 10 # Change an Ace from 11 to 1
        num_aces -= 1
    return value

def get_ascii_card(card, hidden=False):
    """
    Generates ASCII art for a single card.
    If hidden is True, generates a blank card.
    """
    if hidden:
        return [
            "+-------+",
            "|░░░░░░░|",
            "|░░░░░░░|",
            "|░░░░░░░|",
            "|░░░░░░░|",
            "|░░░░░░░|",
            "+-------+"
        ]

    rank = card[0]
    suit = SUIT_SYMBOLS[card[1]] # Get the symbol for the suit

    # Adjust rank for display if it's '10' (needs more space)
    display_rank_top = rank.ljust(2) if rank == '10' else rank.ljust(1)
    display_rank_bottom = rank.rjust(2) if rank == '10' else rank.rjust(1)

    # You could add color here using Colorama:
    # if card[1] in ['Hearts', 'Diamonds']:
    #     color_code = Fore.RED
    # else:
    #     color_code = Fore.BLACK # Or just use default
    # return [
    #     color_code + CARD_TEMPLATE[0] + Style.RESET_ALL,
    #     color_code + CARD_TEMPLATE[1].format(display_rank_top) + Style.RESET_ALL,
    #     color_code + CARD_TEMPLATE[2] + Style.RESET_ALL,
    #     color_code + CARD_TEMPLATE[3].format(suit) + Style.RESET_ALL,
    #     color_code + CARD_TEMPLATE[4] + Style.RESET_ALL,
    #     color_code + CARD_TEMPLATE[5].format(display_rank_bottom) + Style.RESET_ALL,
    #     color_code + CARD_TEMPLATE[6] + Style.RESET_ALL
    # ]
    # For now, without colorama:
    return [
        CARD_TEMPLATE[0],
        CARD_TEMPLATE[1].format(display_rank_top),
        CARD_TEMPLATE[2],
        CARD_TEMPLATE[3].format(suit),
        CARD_TEMPLATE[4],
        CARD_TEMPLATE[5].format(display_rank_bottom),
        CARD_TEMPLATE[6]
    ]


def display_hand(hand, player_name, hide_one=False):
    """
    Displays the cards in a hand using ASCII art.
    If hide_one is True (for dealer's initial hand), conceals the first card.
    """
    print(f"\n{player_name}'s hand:")

    if not hand: # Handle empty hand case
        print("  (No cards)")
        return

    # Get ASCII art for each card in the hand
    card_arts = []
    for i, card in enumerate(hand):
        if hide_one and i == 1: # Hide the second card for the dealer
            card_arts.append(get_ascii_card(card, hidden=True))
        else:
            card_arts.append(get_ascii_card(card, hidden=False))

    # Print the cards row by row to display them side-by-side
    for row_idx in range(len(CARD_TEMPLATE)):
        line = ""
        for card_art in card_arts:
            line += card_art[row_idx] + "  " # Add space between cards
        print(line)

    if not hide_one or (hide_one and player_name == "Your"): # Always show player's total, and dealer's total when revealed
        print(f"  Total value: {calculate_hand_value(hand)}")


def play_blackjack():
    """Main function to play a round of Blackjack."""
    print("Welcome to Blackjack!")

    deck = create_deck()
    shuffle_deck(deck)

    player_hand = []
    dealer_hand = []

    # Initial deal
    player_hand.append(deal_card(deck))
    dealer_hand.append(deal_card(deck))
    player_hand.append(deal_card(deck))
    dealer_hand.append(deal_card(deck))

    # Player's turn
    player_bust = False
    while True:
        display_hand(player_hand, "Your")
        display_hand(dealer_hand, "Dealer's", hide_one=True) # Hide one of dealer's cards

        player_value = calculate_hand_value(player_hand)

        if player_value == 21:
            display_hand(player_hand, "Your") # Show full hand for Blackjack
            print("Blackjack! You win!")
            break
        elif player_value > 21:
            display_hand(player_hand, "Your") # Show full hand when busting
            print("Bust! Your hand is over 21. You lose.")
            player_bust = True
            break

        choice = input("Do you want to [h]it or [s]tand? ").lower()
        if choice == 'h':
            player_hand.append(deal_card(deck))
        elif choice == 's':
            print("You chose to stand.")
            break
        else:
            print("Invalid choice. Please enter 'h' or 's'.")

    # Dealer's turn (only if player hasn't busted)
    if not player_bust:
        print("\nDealer's turn:")
        display_hand(dealer_hand, "Dealer's", hide_one=False) # Reveal dealer's second card

        while calculate_hand_value(dealer_hand) < 17:
            print("Dealer hits...")
            dealer_hand.append(deal_card(deck))
            display_hand(dealer_hand, "Dealer's", hide_one=False)

        dealer_value = calculate_hand_value(dealer_hand)

        if dealer_value > 21:
            print("Dealer busts! You win!")
        else:
            # Compare hands to determine winner
            print("\n--- Final Hands ---")
            display_hand(player_hand, "Your")
            display_hand(dealer_hand, "Dealer's")

            if player_value > dealer_value:
                print("You win!")
            elif dealer_value > player_value:
                print("Dealer wins!")
            else:
                print("It's a push! (Tie)")

    print("\nThanks for playing Blackjack!")

# Run the game
if __name__ == "__main__":
    play_blackjack()