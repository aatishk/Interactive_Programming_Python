# http://www.codeskulptor.org/#user36_tDxcAchpmc_9.py

# Mini-project #6 - Blackjack

import simplegui
import random

# load card sprite - 949x392 - source: jfitz.com
CARD_SIZE = (73, 98)
CARD_CENTER = (36.5, 49)
card_images = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/cards.jfitz.png")

CARD_BACK_SIZE = (71, 96)
CARD_BACK_CENTER = (35.5, 48)
card_back = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/card_back.png")    

# initialize some useful global variables
in_play = False
outcome = ""
in_stand = False
reveal_dealer_score = False
dealer_score = 0
player_score = 0
message = ""

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0],\
                          pos[1] + CARD_CENTER[1]], CARD_SIZE)
        
# define hand class
class Hand:
    def __init__(self):
        self.cards = []	# create Hand object

    # return a string representation of a hand 
    def __str__(self):
        string = "Hand contains"
        for card in self.cards:
            string += " " + str(card)
        return string	

    def add_card(self, card):
        self.cards.append(card)	# add a card object to a hand

    def get_value(self):
        # compute the value of the hand, see Blackjack video
        # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
        hand_value = 0
        aces_flag = 0
        for card in self.cards:
            card_rank = card.get_rank()
            if card_rank == 'A':
                aces_flag = 1	
            hand_value += VALUES[card_rank]
        
        if aces_flag == 1:
            if hand_value + 10 <= 21:
                hand_value += 10
        
        return hand_value
   
    def draw(self, canvas, pos):
        # draw a hand on the canvas, use the draw method for cards
        for card in self.cards:
            card.draw(canvas,pos)
            pos[0] += 75
                
# define deck class 
class Deck:
    # create a Deck object
    def __init__(self):
        self.cards = []
        for suit in SUITS:
            for rank in RANKS:
                self.cards.append(Card(suit, rank))

    def shuffle(self):
        # shuffle the deck 
        return random.shuffle(self.cards)

    def deal_card(self):
        # deal a card object from the deck
        card = random.choice(self.cards)
        self.cards.remove(card)
        return card
    
    def __str__(self):
        # return a string representing the deck
        string = "Deck contains"
        for card in self.cards:
            string += " " + str(card)
        return string

#define event handlers for buttons
def deal():
    global outcome, in_play, in_stand, total_games, message, dealer_score, reveal_dealer_score
    
    global deck, player_hand, dealer_hand, canvas
    
    if in_play:
        dealer_score += 1
    
    deck = Deck()
    deck.shuffle()
    
    player_hand = Hand()
    dealer_hand = Hand()
    
    player_card1 = deck.deal_card()
    player_card2 = deck.deal_card()
    
    player_hand.add_card(player_card1)
    player_hand.add_card(player_card2)
    
    dealer_card1 = deck.deal_card()
    dealer_card2 = deck.deal_card()
    
    dealer_hand.add_card(dealer_card1)
    dealer_hand.add_card(dealer_card2)
    
    in_play = True
    in_stand = False
    reveal_dealer_score = False
    message = "Hit or Stand?"

def hit():
    # if the hand is in play, hit the player
    # if busted, assign a message to outcome, update in_play and score
    
    global player_hand, in_play, deck, dealer_score, message, in_stand
    
    if in_play:
        player_hand_value = player_hand.get_value()
        message = "Hit or Stand?"
        
        if player_hand_value <= 21:
            card = deck.deal_card()
            player_hand.add_card(card)
        
        player_hand_value = player_hand.get_value()
        
        if player_hand_value > 21:
            message = "Player is busted (Player hand > 21). New Deal?"
            dealer_score += 1
            in_play = False
            in_stand = False
       
def stand():   
    # if hand is in play, repeatedly hit dealer until his hand has value 17 or more
    # assign a message to outcome, update in_play and score
    
    global dealer_hand, in_play, deck, in_stand, dealer_score, player_score, message, reveal_dealer_score
    
    in_stand = True
    if in_play:
        dealer_hand_value = dealer_hand.get_value()
        
        while dealer_hand_value < 17:
            card = deck.deal_card()
            dealer_hand.add_card(card)
            dealer_hand_value = dealer_hand.get_value()
        
        if dealer_hand_value > 21:
        	message = "Dealer is busted (Dealer hand > 21). New Deal?"
        	player_score += 1
        else:
        	player_hand_value = player_hand.get_value()
        
        	if player_hand_value < dealer_hand_value:
        		message = "Player is busted (Dealer hand > Player hand). New Deal?"
        		dealer_score += 1
        	elif player_hand_value == dealer_hand_value:
        		message = "Player is busted (Dealer hand = Player hand). New Deal?"
        		dealer_score += 1
        	else:
        		message = "Dealer is busted (Player hand > Dealer hand). New Deal?"
        		player_score += 1
        
        in_play = False
        reveal_dealer_score = True

def reset():
    global dealer_score, player_score, total_games, in_play
    in_play = False
    dealer_score = player_score = 0
    deal()
    
# draw handler    
def draw(canvas):
    
    canvas.draw_text('**B  L  A  C  K  J  A  C  K**', (125, 40), 30, 'White')
    
    canvas.draw_text('D E A L E R', (50, 100), 30, 'Silver')
    canvas.draw_text('Score: ' + str(dealer_score) + "/" + str(dealer_score+player_score), \
                     (300, 100), 25, 'Silver', "monospace")
    dealer_hand.draw(canvas, [50, 130])
    
    if reveal_dealer_score:
        canvas.draw_text('Hand Value = ' + str(dealer_hand.get_value()), (50, 260), 20, 'Silver')
    
    center_message_color = "Lime"
    if not in_play:
    	center_message_color = "Red"
            
    canvas.draw_text(message, (50, 320), 20, center_message_color, "sans-serif") 
    
    canvas.draw_text('P L A Y E R', (50, 380), 30, 'Yellow')
    canvas.draw_text('Score: ' + str(player_score) + "/" + str(dealer_score+player_score), \
                     (300, 380), 25, 'Yellow', "monospace")
    player_hand.draw(canvas, [50, 410])
    canvas.draw_text('Hand Value = ' + str(player_hand.get_value()), (50, 540), 20, 'Yellow')
        
    if not in_stand:
        canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_BACK_SIZE, \
                          [50 + CARD_BACK_CENTER[0], 130 + CARD_BACK_CENTER[1]], CARD_BACK_SIZE)
    
    canvas.draw_polygon([(200, 560), (200, 620), (570, 620), (570, 560)], 3, 'Teal')
    
    canvas.draw_text('NET SCORE: ' + str(player_score - dealer_score) + "/" + \
                     str(dealer_score + player_score), (250, 600), 30, 'White', "monospace")

# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 650)
frame.set_canvas_background("Black")

#create buttons and canvas callback
frame.add_button("DEAL", deal, 150)
frame.add_button("HIT",  hit, 150)
frame.add_button("STAND", stand, 150)
frame.add_button("RESET COUNTERS", reset, 150)
frame.set_draw_handler(draw)

# get things rolling
deal()
frame.start()

# remember to review the gradic rubric
