###############################
# PROLOG SECTION
# blackjack.py
# A blackjack game created in Python
# (1/25/21)
# (David Reilly, Justin Chamoun, Mike Gamez)
# Possible future enhancements: N/A
# Unresolved bugs: N/A
###############################

#Game Logic, handles the cards, betting, and win or lose
# 1 asks player how many diamonds they want to bet and shows your total diamonds.
# 2 if the amount the player bets is more than the diamonds they have program will ask for another amount.
# 3 then the game deals the cards for both the player and Herobrine.
# 4 if the player decides to hit then the program will hand them another card.
# 5 the player also has the choice to stand, double down, or surrender.
# 6 the program will give you a message when you either win or bust
# 7 the program will then show how many diamonds you have left then ask if you want to play again.
# 8 if the user selects yes it will show a scoreboard that counts how many times you and herobrine have won and tied
# 9 if the user selects no then the program stops  
def main():
    p_win, d_win, draw = 0, 0, 0
    greet()
    p_chips = Chips()
    while True:
        cards_deck = Deck()
        cards_deck.shuffle()
        p_cards, d_cards = cards_deck.deal_cards()
        p_hand = Hand()
        p_hand.add_cards(p_cards)
        print("\n Your Total Diamonds ---> ", p_chips.total)
        bet_money = int(input(" Enter how many diamonds you want to bet: "))
        p_chips.bet = take_bet(bet_money, p_chips.total)
        print("\n")

        show_some(p_cards, d_cards, p_hand)
        global PLAYING
        while PLAYING:  # Recall var. from hit and stand function
            blackj_options(p_chips, cards_deck, p_hand, d_cards)
            if player_bust(p_hand, p_chips):
                d_win += 1
                print("\n -- PLAYER --> BUSTED [GAMEOVER]")
                break

        PLAYING = True

        if p_hand.value <= 21:
            d_hand = Hand()
            d_hand.add_cards(d_cards)
            while d_hand.value < 17:
                d_card = hits(cards_deck)
                d_hand.add_cards(d_card)
                if dealer_bust(d_hand, p_hand, p_chips):
                    p_win += 1
                    print("\n -- Herobrine --> BUSTED [GAMEOVER]\n")
                    break
            show_all(p_hand.cards, d_hand.cards, p_hand, d_hand)

            if push(p_hand, d_hand):
                draw += 1
                print("\n " + " PUSH ".center(12, "-"))
            elif player_wins(p_hand, d_hand, p_chips):
                p_win += 1
                print(" " + " PLAYER_WINS ".center(22, "-"))
            elif dealer_wins(p_hand, d_hand, p_chips):
                d_win += 1
                print(" " + " Herobrine WINS ".center(22, "-"))

        else:
            print("\n " + " Herobrine WINS ".center(22, "-"))

        print(f"\n >>> Available Diamonds >>> {p_chips.total} \n")

        ans = str(input(" Play again(YES/NO) : ")).lower()
        if ans != "yes" or p_chips.total < 1:
          
            if p_chips.total < 1:
                print(" NO MORE DIAMONDS !!! ")
            break
        clear_screen()
        greet2(str(p_win), str(d_win), str(draw))  # Score board location -> Top
        print("\n" + " ".ljust(30, "-"))
			
				
###############################
# PROCESSING INITIALIZATION SECTION
###############################
#This Section defines the cards and thei	
from random import choices, shuffle
from os import system, name			

SUITS = ("Hearts", "Diamonds", "Spades", "Clubs")
RANKS = (
    "2",
    "3",
    "4",
    "5",
    "6",
    "7",
    "8",
    "9",
    "10",
    "Jack",
    "Queen",
    "King",
    "Ace",
)
VALUES = {
    "2": 2,
    "3": 3,
    "4": 4,
    "5": 5,
    "6": 6,
    "7": 7,
    "8": 8,
    "9": 9,
    "10": 10,
    "Jack": 10,
    "Queen": 10,
    "King": 10,
    "Ace": 11,
}
PLAYING = True

class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return self.rank + " of " + self.suit


class Deck:
    """ Creating a Deck of cards and
    Deal two cards to both player and dealer. """

    def __init__(self):
        self.deck = []
        self.player = []
        self.dealer = []
        for suit in SUITS:
            for rank in RANKS:
                self.deck.append((suit, rank))

    def shuffle(self):
        shuffle(self.deck)

    def deal_cards(self):
        self.player = choices(self.deck, k=2)
        self.delete_cards(self.player)
        self.dealer = choices(self.deck, k=2)
        self.delete_cards(self.dealer)  # Delete Drawn Cards
        return self.player, self.dealer

    def delete_cards(self, total_drawn):
        """ Delete Drawn cards from the Decks """

        try:
            for i in total_drawn:
                self.deck.remove(i)
        except ValueError:
            pass


class Hand:
    """ Adding the values of player/dealer cards 
    and change the values of Aces acc. to situation. """

    def __init__(self):
        self.cards = []
        self.value = 0
        self.aces = 0

    def add_cards(self, card):
        self.cards.extend(card)
        for count, ele in enumerate(card, 0):
            if ele[1] == "Ace":
                self.aces += 1
            self.value += VALUES[ele[1]]
        self.adjust_for_ace()

    def adjust_for_ace(self):
        while self.aces > 0 and self.value > 21:
            self.value -= 10
            self.aces -= 1


class Chips:
    """ Player/dealer chips for making bets
    and Adding/Deducting amount in/from Player's total. """

    def __init__(self):
        self.total = 1000
        self.bet = 0
        self.winnings = 0

    def win_bet(self):
        self.total += self.bet
        self.winnings += 1

    def loss_bet(self):
        self.total -= self.bet
        self.winnings += 1

player_name = input(" What is your name crafter?: ")      
def take_bet(bet_amount, player_money):
    try:
        while bet_amount > player_money or bet_amount <= 0:
            bet_amount = int(input(" Enter amount again : "))
        return bet_amount

    except TypeError:
        return "Invalid bet amount"
###############################
# PROCESSING SECTION
# Branching code:
# Looping code:
###############################
def success_rate(card, obj_h):
    """ Calculate Success rate of 'HIT' new cards """

    rate = 0
    diff = 21 - obj_h.value
    if diff != 0:
        rate = (VALUES[card[0][1]] / diff) * 100

    if rate < 100:
        print(f"[ WIN(hit) : {int(rate)}% | LOSS(hit) : {100-int(rate)}% ]")
    elif rate > 100:
        l_rate = int(rate - (rate - 99))  # Round to 99
        if card[0][1] == "Ace":
            l_rate -= 99
        print(f"[ WIN(hit) : {100-l_rate}% | LOSS(hit) : {l_rate}% ]")
    else:
        print(f"[ GOLD IN YOUR HAND!!!!]")


def hits(obj_de):
    new_card = [obj_de.deal_cards()[0][0]]
    # obj_h.add_cards(new_card)
    return new_card

hit = "h"
stand = "st"
surrender = "su"
double = "dd"
def blackj_options(p_chips, obj_de, obj_h, dealer_card):
    global PLAYING
    next_card = hits(obj_de)
    success_rate(next_card, obj_h)
    choice = str(input(f"[ HIT(h) | STAND(st) | SURRENDER(su) | DOUBLE DOWN(dd) ] : ")).lower()
    print("\n")
    if choice == hit:
        # hits(obj_de, obj_h)
        obj_h.add_cards(next_card)
        show_some(obj_h.cards, dealer_card, obj_h)

    elif choice == stand:
        PLAYING = False

    elif choice == surrender:
        p_chips.bet = p_chips.bet / 2
        PLAYING = False
        obj_h.value += 21

    elif choice == double:
        if p_chips.bet * 2 <= p_chips.total:
            p_chips.bet *= 2
            next_d_card = hits(obj_de)
            obj_h.add_cards(next_d_card)
            PLAYING = False
        else:
            print(" --You can't Double Down, Not enough Diamonds--")
    else:
        print(" --Invalid Choice--")


def show_all(player_cards, dealer_cards, obj_h, obj_d):
    print(f" \n PLAYER_CARDS [{obj_h.value}] : {player_cards}")
    print(f" DEALER_CARDS [{obj_d.value}] : {dealer_cards} \n \n")

def show_some(player_cards, dealer_cards, obj_h):
        print(f"\n {player_name}'s Cards [{obj_h.value}]:\n {player_cards}")
        print(f"\n Herobrine's Cards [{VALUES[dealer_cards[1][1]]}]:\n {[dealer_cards[1]]} \n \n")
				
###############################
# CLEANUP, TERMINATION, and EXIT
# SECTION
###############################
# End game Scenarios (Win/Lose Conditions)
def player_bust(obj_h, obj_c):
    if obj_h.value > 21:
        obj_c.loss_bet()
        return True
    return False


def player_wins(obj_h, obj_d, obj_c):
    if any((obj_h.value == 21, obj_h.value > obj_d.value and obj_h.value < 21)):
        obj_c.win_bet()
        return True
    return False


def dealer_bust(obj_d, obj_h, obj_c):
    if obj_d.value > 21:
        if obj_h.value < 21:
            obj_c.win_bet()
        return True
    return False


def dealer_wins(obj_h, obj_d, obj_c):
    if any((obj_d.value == 21, obj_d.value > obj_h.value and obj_d.value < 21)):
        obj_c.loss_bet()
        return True
    return False


def push(obj_h, obj_d):
    if obj_h.value == obj_d.value:
        return True
    return False


def player_surrender(obj_c):
    obj_c.loss_bet()
    return True


#######################################
#Panel Message when game loads to introduce

def clear_screen():
    system("cls" if name == "nt" else "clear")


def greet():
    print(" " + "".center(40, "_"), "|" + "".center(40, " ") + "|", sep="\n")
    print(
        "|" + "Welcome to MineJack".center(40, " ") + "|",
        "|" + "Created by DragonCraft".center(40, " ") + "|",
        "|" + "(A Poor Minecraft Blackjack rip-off)".center(40, " ") + "|",
        "|" + "".center(40, "_") + "|",
        sep="\n",
    )


def greet2(p_count, d_count, draw_c):
    print(" " + "".center(30, "_"))
    print(
        "|" + player_name .ljust(20, " ") + "|",
        "_Herobrine__".center(10, " ") + "|",
        "_DRAW__".rjust(15, " ") + "|",
        sep="_",
    )
    print(
        "|"
        + "".center(15, " ")
        + "|"
        + "".center(15, " ")
        + "|"
        + "".center(15, " ")
        + "|"
    )
    print(
        "|"
        + p_count.center(15, "_")
        + "|"
        + d_count.center(15, "_")
        + "|"
        + draw_c.center(15, "_")
        + "|"
    )
print("|" {player_name}  {p_count}"")
main()