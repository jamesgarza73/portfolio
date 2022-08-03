#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 13 18:05:22 2020

@author: jamesgarza1
"""
# Declare libraries needed to be used in the code
import random
#import mysql.connector

# This is the Card class that will be used to create a card with suit, rank and value
# There is alos the function to deal with an ace in the player's hand. Legacy code.
class Card():
    '''This class function gets the stock data either from the local computer or online. Returns a dataframe of the 
    one minute stock data.

    Args:
    symbol (string): this is the symbol of the data that is needed.
    source (string): This string is for either online or local hard drive access of stock one minute data.
    user (string): This is the number in the future you want to predict out.

    Returns:
    df (dataframe): stock data by the symbol requested in dataframe sorted by date.  Indicators will be added later.

    Notes: 
    '''
    def __init__(self, suit, rank, available = True, highest_value = True):
        self.suit = suit
        self.rank = rank
        self.available = available
        self.highest_value = highest_value

    def __str__(self):
        return "[ " + self.suit + " / " + self.rank + " ]"
        
    def get_value(self):
        '''This function gets the stock data either from the local computer or online. Returns a dataframe of the 
        one minute stock data.
    
        Args:
        symbol (string): this is the symbol of the data that is needed.
        source (string): This string is for either online or local hard drive access of stock one minute data.
        user (string): This is the number in the future you want to predict out.
    
        Returns:
        df (dataframe): stock data by the symbol requested in dataframe sorted by date.  Indicators will be added later.
    
        Notes: 
        '''
        if (self.rank == "2" or self.rank == "3" or
            self.rank == "4" or self.rank == "5" or
            self.rank == "6" or self.rank == "7" or
            self.rank == "8" or self.rank == "9" or
            self.rank == "10"):
            val = int(self.rank)
        elif (self.rank == "Jack" or self.rank == "Queen" or
              self.rank == "King"):
            val = 10
        elif (self.rank == "Ace"):
            if self.highest_value:
                val = 11
            else:
                val = 1
        return val
# The deck Class will create a deck of 52 cards and also has a random card method
class Deck():
    def __init__(self):
        self.cards = []
        suits = ["HEARTS", "CLUBS", "SPADES", "DIAMONDS"]
        ranks = ["Ace", "2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King"]
        for suit in suits:
            for rank in ranks:
                self.cards.append(Card(suit, rank))
                
    def get_random_card(self):
        while True:
            index = random.randint(0,51)
            if self.cards[index].available:
                self.cards[index].available = False
                return self.cards[index]
# Each player will be assigned a hand and I had to use this instead of putting this
# into the player class because the hand needs to renew the hand on every game
class Hand():
    def __init__(self):
        self.cards = []
        self.handValue = 0 
        self.blackJack = False
        self.bust = False
    # method to add a card to the hand in tracked in cards
    def addCard(self, card): 
        self.cards.append(card)
    # method to put the cards in the hand into a string to send to the database
    def printCards(self, cards):
        s = ""
        for i in range(len(cards)):
            s = s + "Suit: " + cards[i].suit + " Rank: " + cards[i].rank + ", "
        return s
# There are only a few things in the player class as I have made many classes
class Player():
    def __init__(self, account):
        self.hand = Hand()
        self.account = account
        self.name = None 
        self.bet = 0 
        self.prize = 0
    # method to get players name
    def getPlayerName(self):
        while True:
            try:
                name = input("Enter Player Name: ")
            except ValueError:
                print("Name can only be text. ")
            if len(name) > 3:
                return name
                break
            else:
                print("Name must be at least 4 charectors long. ")
    # I had originally put takeBet into game but it is better here because if you want
    # to add more players it has to be a player player class to keep track of each players bet.            
    def takeBet(self):  
        while True:
            try:
                print('This is how much you have in your account to bet: ' + str(self.account))
                self.bet = int(input("How much would you like to bet? "))
            except ValueError:
                print("Bet must be an integer only! Try again! ")
            else: 
                if self.bet > self.account:
                    print("Your Bet cannot exceed your account!!")
                    print("")
                elif self.bet < 1:
                    print("Your Bet has to be greater than 1!!")
                    print("")
                else:
                    return self.bet
                    break
# THe game class will track the game and keep all the information to pass onto the database    
class Game():
    def __init__(self, dealer, player, deck, results):
        self.result = None 
        self.dealer = dealer
        self.player = player
        self.deck = deck
        self.results = results
    # This method evaluates each player hand and returns handvalue to the players hand
    def handValuation(self, cards):
        handValue = 0
        ace = 0
        # I had to do this loop to see first what the hand value is and secondly see if 
        # there are any aces and if so then need to change the hand values to comply with 
        # the rules of the game.  This way is a bit longer but had to do it to comply with 
        # the legacy code.
        for i in range(len(cards)):
            handValue += Card.get_value(cards[i])
            if cards[i].rank == 'Ace':
                ace += 1
        # Once we have an ace and the hand value is above 21 then change the value of the aces.
        if ace > 0 and handValue > 21:
            handValue = 0
            for i in range(len(cards)):
                if cards[i].rank =='Ace':
                    cards[i].highest_value = False
                handValue += Card.get_value(cards[i])
        return handValue
    # This method shows the hand in the begining of the game with the dealers card hidden.  I also
    # use this method on the hit or stand method.
    def showSomeCards(self):
        print()
        print(self.dealer.name, " hand is: ")
        print("<hidden card>")
        print(self.dealer.hand.cards[0])
        print()
        print(self.player.name, " hand is: ")
        print(*self.player.hand.cards, sep="\n")
        print()
    # This method shows all the cards but will be done at the end of the game to verify results.
    def showAllCards(self):
        print()
        print(self.dealer.name, "Dealer's Hand:")
        print(*self.dealer.hand.cards, sep="\n")
        print("Dealer's Hand Total is =",self.dealer.hand.handValue)
        print()
        print(self.player.name, "Hand: ")
        print(*self.player.hand.cards, sep= '\n')
        print("Player's Hand Total is = ", self.player.hand.handValue)
        
        print()    
        # Inform Player of their chips total and thier prize
        print("\nPlayers account stands at", self.player.account)
        print("Players prize is = ", self.player.prize)
        print("")
        
    # This method is for the player to decide if they want another card then to hit or stay with thier
    # existing cards only.  Also put in checks to make sure the user enters only an h or s
    def hitOrStand(self):
        while True:
            x = input("Would you like to 'Hit' or 'Stand'? Enter 'h' or 's'? ")
            if x == 'h':
                self.player.hand.addCard(self.deck.get_random_card())
                self.player.hand.handValue = self.handValuation(self.player.hand.cards)
                if self.player.hand.handValue > 21:
                    self.player.hand.bust = True
                    break
                Game.showSomeCards(self)
                continue
            elif x == 's':
                print()
                print("Player stands. Dealer is hitting. ")
                break
            else:
                print()
                print("entry can only be 'h' or 's', please try again.")
                continue
            break
    # This method is if used to calculate the prize if the player wins
    def winBet(self):
        self.player.prize = self.player.bet * 2
        self.player.account += self.player.prize
    # This method is if used to calculate the prize if the player loses
    def loseBet(self):
        self.player.prize = self.player.bet * -1
        self.player.account += self.player.prize
    # This method is if used to calculate the prize if the player has a blackjack with an Ace
    def blackJack(self):
        self.player.prize = self.player.bet * 2.5
        self.player.account += self.player.prize
    # This method is if used to calculate the prize if the player ties with the dealer
    def push(self):
        self.player.prize = 0 
    
    def playAgain(self):
        while True:
            # Ask if the player would like to play again loop till the proper response with checks in place
            newGame = input("would you like to play another game? Enter 'y' or 'n'? ")
            print("")
            if newGame == 'y' or newGame == 'Y':
                if self.player.account <= 0:
                    print(self.player.name, " account is bankrupt you can no longer play!! ")
                    playing = False
                    break
                else:
                    playing = True
                    break
            elif newGame == 'n' or newGame == 'N':
                print(self.player.name, 'Thanks for playing! ')
                playing = False
                break
        return playing
        
    # This method goes through the winner and the loser with evaluating player and dealer.
    # I did go a bit crazy with the classes but I think it is cleaner to put the if statements 
    # in the least a method but I decided to go with class since I got the hang of it.     
    def winner(self):
        if self.player.hand.bust: # player busts!! no need to continue game
            print(self.player.name, "Busts!!!!")            
            self.loseBet()
            self.result = 'Player busts and Dealer wins'
        
        # dealer keeps hitting till either its hand is above 17 or bust
        while self.dealer.hand.handValue < 17 and not self.player.hand.bust:
            self.dealer.hand.addCard(self.deck.get_random_card())
            self.dealer.hand.handValue = self.handValuation(self.dealer.hand.cards)
            if self.dealer.hand.handValue > 21:
                print("Dealer busts!!")
                self.result = 'Dealer busts and Player wins'
                self.dealer.hand.bust = True
                break
        # check different winning scenarios
        # dealer's hand has busted and players hand is less than 21 but does not have a 21 either
        if self.dealer.hand.bust and self.player.hand.handValue != 21 and not self.player.hand.bust:
            print("Dealer busts & Player wins!! ")
            self.winBet()
            self.result = 'Player Win, Dealer Busts'
            
        # Dealer's hand has busted, player has a 21 with one being an Ace so they win 2.5 prize on their bet
        elif self.dealer.hand.bust and self.player.hand.handValue == 21 and len(self.player.hand.cards) == 2:
            print("Dealer busts and player has a BlackJack!! ")
            self.blackJack()
            self.result = 'Player wins by 21 and dealer loses'
        
        # Dealer's hand has busted and player has 21 without an ace 
        elif self.dealer.hand.bust and self.player.hand.handValue == 21:
            print("Dealer busts and player wins!! ")
            self.winBet()
            self.result = 'Player wins by 21 and dealer loses'
            
        # Dealer's hand is less than 21 but players hand is 21 and has done this with two cards one being and Ace
        # so they win 2.5 prize on their bet
        elif not self.dealer.hand.bust and self.player.hand.handValue == 21 and len(self.player.hand.cards) == 2:
            print("Dealer loses and player wins!! ")
            self.blackJack()
            self.result = 'Player wins by 21 and dealer loses'
        
        # Dealer's hand is less than 21 and player's hand is 21 but without an Ace therfore prize is 2 times their bet
        elif not self.dealer.hand.bust and self.player.hand.handValue == 21:
            print("Dealer loses and player wins!! ")
            self.winBet()
            self.result = 'Player wins by 21 and dealer loses'
            
        # Dealer's hand is less than 22 and greater than players hand and both are less than or equal to 21
        elif self.dealer.hand.handValue > self.player.hand.handValue and not self.dealer.hand.bust:
            print("Dealer wins and player loses!! ")
            self.loseBet()
            self.result = 'Dealer wins and Player loses'
        
        # Dealer's hand is less than the player but players hand is not 21 but less than or equal to 21
        elif self.dealer.hand.handValue < self.player.hand.handValue and not self.player.hand.bust:
            print("Dealer loses and player wins!! ")
            self.winBet()
            self.result = 'Dealer loses Player wins'
        
        # It is a tie which is a push nobody wins or loses
        elif not self.player.hand.bust and not self.dealer.hand.bust :
            print("Push!! Nobody wins or loses!! ")
            self.push()
            self.player.prize = 0
            self.result = 'Push'
                   
    def gameResults(self):
        '''This function gets the stock data either from the local computer or online. Returns a dataframe of the 
        one minute stock data.
    
        Args:
        symbol (string): this is the symbol of the data that is needed.
        source (string): This string is for either online or local hard drive access of stock one minute data.
        user (string): This is the number in the future you want to predict out.
    
        Returns:
        df (dataframe): stock data by the symbol requested in dataframe sorted by date.  Indicators will be added later.
    
        Notes: 
        '''
        # put the cards into strings to put into the dataframe
        dealerCards = self.player.hand.printCards(self.dealer.hand.cards)
        playerCards = self.player.hand.printCards(self.player.hand.cards)
        data = [] # Blank array to store the data to go into dataframe
        
        # record data into a dataframe
        data = [self.player.name, self.player.account, self.player.bet, self.result, self.player.prize, 
                self.dealer.hand.handValue, self.player.hand.handValue, dealerCards, 
                playerCards]
        dfLength = len(self.results)
        self.results.loc[dfLength] = data
        return self.results
    
    # This method sends the results of the games to the database.    
    def SQLconnect(self):    
        conn = mysql.connector.connect(host='52.50.23.197',
                               port='3306',
                               user='James_sba19053',
                               password='sba19053',
                               database='James_sba19053')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM RESULTS")
        cursor.fetchall()
        rc = cursor.rowcount
        print("")
        print("Number of games played :", str(len(self.results)))
        print("Number of rows in table before database updated: ", rc) #verify how many rows exist
        # this loop iterates through all the results and writes them to the database
        for i in range(len(self.results)):
            sql = "INSERT INTO RESULTS (playerName, accountValue, betAmount,resultOfGame, prize, DealerHand, PlayerHand, dealerCards, playerCards) VALUES (%s, %s, %s, %s,%s, %s, %s, %s, %s)"
            val = (self.results.iloc[i,0], self.results.iloc[i,1], self.results.iloc[i,2], self.results.iloc[i,3], 
                  self.results.iloc[i,4], self.results.iloc[i,5], self.results.iloc[i,6], self.results.iloc[i,7], self.results.iloc[i,8])
            cursor.execute(sql, val)
            conn.commit()
        
        """
        # Run this first to view databases:
        cursor.execute("SHOW DATABASES")
        for x in cursor:
            print(x)
            
        # Second I did this to add the table to the database
        cursor.execute("CREATE TABLE RESULTS(playerName VARCHAR(255), accountValue INT, betAmount INT,resultOfGame VARCHAR(255), prize INT, DealerHand INT, PlayerHand INT, dealerCards VARCHAR(255), playerCards VARCHAR(255))")
        cursor.execute("SHOW TABLES")
        for x in cursor:
            print(x)
            
        for x in cursor:
            print(x) 
          
        cursor.execute("SELECT * FROM RESULTS")
        myresult = cursor.fetchall()
        for x in myresult:
          print(x)
            
        """
        cursor.execute("SELECT * FROM RESULTS")
        cursor.fetchall()
        rc = cursor.rowcount
        print("Number of rows in table after database updated: ", rc) #verify how many were sent to database
        print("Database has been updated with player results!")
        conn.close()