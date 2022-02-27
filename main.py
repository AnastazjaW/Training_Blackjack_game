import random

class Account:

     def __init__(self, owner, balance):
         self.owner = owner
         self.balance = balance
         self.bet_amount = 0

     def bet(self):
         while True:
             try:
                 self.bet_amount = int(input('Please, place your bet: 1, 5, 10 or 20 '))
                 if self.bet_amount not in [1, 5, 10, 20]:
                     print('Wrong bet! Can be only 1, 5, 10 or 20')
                 elif self.balance < self.bet_amount:
                     print(f'There is no enough money. Your balance is {self.balance}')
                 else:
                     self.balance -= self.bet_amount
                     print(f'Your bet {self.bet_amount} is accepted ')
                     break
             except ValueError:
                 print('Please, enter integer')

     def add_money(self):
         self.balance += self.bet_amount*2

     def __str__(self):
         return f'There is {self.balance} on your account.'

suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5, 'Six': 6, 'Seven': 7, 'Eight': 8,
          'Nine': 9, 'Ten': 10, 'Jack': 10, 'Queen': 10, 'King': 10, 'Ace': 11}

class Card:

    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        self.value = values[rank]

    def __str__(self):
        return self.rank + ' of ' + self.suit

class Deck:

    def __init__(self):
        self.all_cards = []
        for suit in suits:
            for rank in ranks:
                self.all_cards.append(Card(suit, rank))

    def shuffle(self):
        random.shuffle(self.all_cards)

    def deal_one(self):
       return self.all_cards.pop(0)

    def take_one(self):
        player_card = self.all_cards[0]
        self.all_cards.pop(0)
        return player_card

class Player:

    def __init__(self, name):
        self.name = name
        self.players_cards = []
        self.one_card_value = 0
        self.player_points = 0
        self.aces = 0

    def add_cards_and_points(self, new_cards):
        self.players_cards.append(new_cards)
        list_of_points = []
        for i in range(len(self.players_cards)):
            list_of_points.append(self.players_cards[i].value)
        self.player_points = sum(list_of_points)
        if new_cards.rank == 'Ace':
            self.aces += 1
        while self.player_points > 21 and self.aces >= 1:
            self.player_points -= 10
            self.aces -= 1

    def str_shows_one_card(self):
        self.one_card_value = self.players_cards[1].value
        return self.name + ' has:\n' + "".join(str(self.players_cards[1])) + f'\n{self.one_card_value} points'


    def __str__(self):
        all_player_cards = '\n'.join(map(str, self.players_cards))
        return self.name + ' has:\n' + all_player_cards + f'\n{self.player_points} points'

def play_again():
    while True:
        ready_to_play = input('Do you want play again? Enter Yes or No').lower().strip()
        if ready_to_play == 'no':
            return False
        elif ready_to_play == 'yes':
            return  True
        else:
            print('Please, enter Yes or No!')


print("Welcome to Blackjack game!")
player_name = input('Please, enter your name ').strip()
player1 = Player(player_name)
dealer = Player('Dealer')
player_account = Account(player_name, 100)
dealer_account = Account('Dealer', 0)

while True:
    new_deck = Deck()
    new_deck.shuffle()
    print(player_account)
    player_account.bet()
    new_deck.deal_one()
    player1.add_cards_and_points(new_deck.take_one())
    dealer.add_cards_and_points(new_deck.take_one())
    player1.add_cards_and_points(new_deck.take_one())
    dealer.add_cards_and_points(new_deck.take_one())
    print(player1)
    print(dealer.str_shows_one_card())
    # Player's turn
    game_on = True
    while game_on:
        while player1.player_points < 21:
            hint_or_stand = input('Do you want hint or stand? Enter h if hint, s if stand').lower().strip()
            if hint_or_stand == 'h':
                player1.add_cards_and_points(new_deck.take_one())
                print(player1)
            elif hint_or_stand == 's':
                break
            else:
                print('Enter h or s')
        if player1.player_points > 21:
            print(player_name + ' lose! Dealer win!')
            print(player_account)
            game_on = False
            break
        if player1.player_points == 21:
            player_account.add_money()
            print(player_name + ' win!')
            print(player_account)
            game_on = False
            break

        # Dealer's turn
        while dealer.player_points < 17:
            dealer.add_cards_and_points(new_deck.take_one())
            print(dealer)
            if dealer.player_points == 21:
                print('Dealer win!')
                dealer_account.add_money()
                game_on = False
                break
            if dealer.player_points > 21:
                print(f'Dealer lose! {player_name} win!')
                player_account.add_money()
                game_on = False
                break
    if not play_again():
        break
    else:
        player1.players_cards = []
        dealer.players_cards = []
        continue







