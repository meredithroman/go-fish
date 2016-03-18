import random

class Card(object):

    _card_names = {1: 'Ace', 
                   2: 'Two', 
                   3: 'Three', 
                   4: 'Four', 
                   5: 'Five', 
                   6: 'Six', 
                   7: 'Seven', 
                   8: 'Eight', 
                   9: 'Nine', 
                   10: 'Ten', 
                   11: 'Jack', 
                   12: 'Queen', 
                   13: 'King'
                   }

    def __init__(self, suit, number):
        self.suit = suit
        self.number = number

    def display_name(self):
        card_name = self._card_names.get(self.number)
        return card_name + " of " + self.suit.capitalize()


class Deck(object):

    cards = []
    
    def __init__(self):
        suits = ('clubs', 'diamonds', 'hearts', 'spades')
        for suit in suits:
            for i in range(1,14):
                card = Card(suit,i)
                self.cards.append(card)

    def shuffle(self):
        random.shuffle(self.cards)

class Hand(object):

    def __init__(self, game):
        self.sets = []
        self.game = game
        self.deck = self.game.deck
        self.cards = self.deck.cards[0:7]
        del self.deck.cards[0:7]

    def draw(self):
        try:
            self.cards.append(self.deck.cards.pop())
        # if the deck is empty, do nothing
        except IndexError:
            pass

    def show_cards(self):
        idx = 0
        for card in self.cards:
            print str(idx) + ": " + card.display_name()
            idx += 1

    def check_for_set(self):
        for i in range(1,14):
            possible_set = [c for c in self.cards if c.number == i]
            if len(possible_set) == 4:
                self.sets.append(possible_set)
                self.cards = [c for c in self.cards if c not in possible_set]
                self.game.num_sets += 1
                return True
        return False

class Game(object):

    num_sets = 0

    def __init__(self):
        self.deck = Deck()
        self.deck.shuffle()

        self.player_hand = Hand(self)
        self.bot_hand = Hand(self)

    def guess(self, card_num, opponent_hand):
        matches = []
        for card in opponent_hand.cards:
            if card.number == card_num:
                idx = opponent_hand.cards.index(card)
                matches.append(opponent_hand.cards.pop(idx))
        return matches

    def remaining_sets(self):
        return 13 - self.num_sets

# TODO: refactor
game = Game()

player_set = game.player_hand.check_for_set()
if player_set:
    print "You got a set! There are %d sets still available."  % game.remaining_sets()

bot_set = game.bot_hand.check_for_set()
if bot_set:
    print "Your opponent got a set! There are %d sets still available."  % game.remaining_sets()

while game.num_sets < 13:
    
    player_turn = True
    while player_turn:
        print "\nThis is your hand:\n"
        game.player_hand.show_cards()
        user_input = raw_input("\nEnter the number of the card you want to play: ")
        try:
            card = game.player_hand.cards[int(user_input)]
            guess = game.guess(card.number, game.bot_hand)
            game.player_hand.cards.extend(guess)
            if guess:
                for card in guess:
                    print "\nYou stole " + card.display_name() + "!"
            elif not guess:
                print "\nGo Fish!"
                game.player_hand.draw()
                player_turn = False
            player_set = game.player_hand.check_for_set()
            if player_set:
                print "\nYou got a set! There are %d sets still available."  % game.remaining_sets()
            if not game.player_hand.cards:
                game.player_hand.draw()
            if not game.remaining_sets():
                player_turn = False
        except:
            print "\nPlease enter a valid number."

    opponent_turn = True
    while opponent_turn:
        try:
            card = random.choice(game.bot_hand.cards)
        # if bot is out of cards, draw one
        except IndexError:
            game.bot_hand.draw()
        guess = game.guess(card.number, game.player_hand)
        game.bot_hand.cards.extend(guess)
        if guess:
            for card in guess:
                print "\nYour opponent stole " + card.display_name() + "!"
        elif not guess:
            print "\nYour opponent went fishing!"
            game.bot_hand.draw()
            opponent_turn = False
        bot_set = game.bot_hand.check_for_set()
        if bot_set:
            print "\nYour opponent got a set! There are %d sets still available."  % game.remaining_sets()
        if not game.bot_hand.cards:
            game.bot_hand.draw()
        if not game.remaining_sets():
            opponent_turn = False

num_player_sets = len(game.player_hand.sets)
num_bot_sets = len(game.bot_hand.sets)
if num_player_sets > num_bot_sets:
    print "\nCongratulations, you won with %d sets to your opponent's %d sets." % (num_player_sets, num_bot_sets)
elif num_player_sets < num_bot_sets:
    print "\nYou lost with %d sets to your opponent's %d sets." % (num_player_sets, num_bot_sets)