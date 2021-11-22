# Declare libraries needed to be used in the code including my own library.
import pandas as pd
import BlackJackSupport as bkjk

# Start my BlackJack game
playing = True # Variable to continue loop till the player no longer wants to play
count = 0 # this keeps track of starting the game
while playing:
    if count == 0: # Go through this only once at the begining of the game
        # Print an opening statement and only run once at the beginning of the game
        print("Welcome to my Blackjack game!!")
        columnNames = ["Player Name","Account Value", "Bet Amount","Result of Game","Prize","Dealer Hand",
               "Player Hand","Dealer Cards","Player Cards"]
        results = pd.DataFrame(columns = columnNames) #Empty dataframe to put all the data in. I like this
        # type of way to save the data as it looks like an excel spreadsheet.
        dealer = bkjk.Player(0) # Create a dealer with 0 in account
        dealer.name = 'Dealer' # Dealer name
        player = bkjk.Player(1000) # Create a player with 1000 in acccount can create a loop here
        #if I want to add ore players
        player.name  = player.getPlayerName() # This is where I ask the player to input thier name
        count = 1 # change count so we will not repeat this in the multiple games
    deck = bkjk.Deck() #create a deck because it is new everytime a new game starts
    game = bkjk.Game(dealer, player, deck,results) # Create a game to keep track of the game
    player.takeBet() # Take player bet
    player.hand = bkjk.Hand() # Create a players hand
    player.hand.addCard(deck.get_random_card()) # Deal a card
    player.hand.addCard(deck.get_random_card()) 
    player.hand.handValue = game.handValuation(player.hand.cards) #Evaluate players hand    
    dealer.hand = bkjk.Hand() # Create dealer hand
    dealer.hand.addCard(deck.get_random_card()) # Deal a card
    dealer.hand.addCard(deck.get_random_card()) 
    dealer.hand.handValue = game.handValuation(dealer.hand.cards) # Evaluate dealers hand
    # print one card for dealer and print player cards
    game.showSomeCards() 
    game.hitOrStand() 
    game.winner() # Get results of BlackJack winner
    game.showAllCards()
    # Get the data to track the results of the game
    results = game.gameResults()
    # Ask player if they want to play again
    playing = game.playAgain() 
# Call mySQL class to save game results to database
#game.SQLconnect() # send data now!