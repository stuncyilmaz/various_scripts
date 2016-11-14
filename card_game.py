
import numpy as np
import argparse
class MyBoards:
    """
    Class for the board state
    """
    def __init__(self):
        # list of all cards: [ [suite, value, open/closed/removed], [...], ...   ]
        self.all_cards = [] 
        # list of indexes for open cards
        self.open_indexes = []
        # list of indexes for closed clards
        self.closed_indexes = [i for i in range(52)]
        # list of indexes for removed cards
        self.removed_indexes = []
        
    def get_initial_boards(self):
        """
        prepare and shuffle cards, start of the play
        """
        cards_numbers = [ i for i in range(13) ]
        all_cards = []
        for suit in ["c", "d", "h", "s"]:
            for my_number in cards_numbers:
                all_cards.append(  [suit, my_number] )
                
        # initially all cards are closed for the player
        # a card can be open, closed or removed
        all_cards = [ [elt[0], elt[1], "closed"]  for elt in all_cards]
        np.random.shuffle(all_cards)
        self.all_cards = all_cards
        
    def remove_card_at_index(self, my_index):
        """
        removes the card at index my_index, so that 
        the entry in self.all_cards is modified to "removed"
        """
        self.all_cards[my_index][2] = "removed"
        self.removed_indexes.append(my_index)
        self.closed_indexes = [elt for elt in self.closed_indexes if not elt == my_index]
        self.open_indexes = [elt for elt in self.open_indexes if not elt == my_index]

    def open_card_at_index(self, my_index):
        """
        opens the card at index my_index, so that 
        the entry in self.all_cards is modified to "open"
        """
        if my_index not in self.closed_indexes:
            print "cannot open, already open or removed or out of index"
            return False
        self.all_cards[my_index][2] = "open"
        self.open_indexes.append(my_index)
        self.closed_indexes = [elt for elt in self.closed_indexes if not elt == my_index]
        return True
        
    def is_match(self, ind1, ind2):
        """
        checks if the cards at indexes ind1 and ind2 match
        """
        return self.all_cards[ind1][1] == self.all_cards[ind2][1]

        
class Player:
    """
    class for individual player.
    """
    def __init__(self):
        """
        mathced pairs for player. list of lists.
        each element in teh list is of the form 
        [[suite1, value1, removed], [suite2, value2, removed]]
        """
        # keep track of the matched pairs for the player
        # the length of this list is the count of matched cards
        self.matched_pairs = []
        
    def play(self, board, my_index):
        
        """
        when the player opens a card, if it matches an open card, the player 
        opens that opened card automatically, so that there is a match.
        """
        if my_index in board.open_indexes:
            print "already open"
            return False
        
        if board.open_card_at_index(my_index):
            print "opened card" 
            print board.all_cards[my_index] 
        else:
            return False
        # ind_open: the index  of the card from the previously opened card list
        # that matches the currently opened card. If it is False, there is no matching card
        ind_open = self.pair_found(board, my_index)
        # if there is a match
        if ind_open is not False:
            self.matched_pairs.append( [board.all_cards[my_index], board.all_cards[ind_open]  ]  )
            board.remove_card_at_index( my_index)
            board.remove_card_at_index( ind_open)
            print "pair found" 
            print self.matched_pairs[-1] 
            return "pair found"
        return True
    
    def pair_found(self, board, ind):
        """
        does ind pair with any opened cards?
        
        """
        for ind_open in board.open_indexes:
            if ind_open == ind:
                continue
            if board.is_match(ind, ind_open):
                return ind_open
        return False
               
    
    def show_closed_cards(self, board):
        """
        shows close cards indexes
        """
        return board.closed_indexes

    
    def show_matched_pairs(self):
        return self.matched_pairs
        



# ********************** Functions for the game ********************** 
def get_index(mystr):

    for i in range(3):
        try:
            my_index = input(mystr)
            my_index =  int(my_index)
            return my_index
        except:
            print "type int"
    print "too many wrong input"
    raise Exception


# Functions for the game
def one_game(player, board):
    # one hand for the player
    """
    one hand for the player
    open two cards. if the first card matches
    an already opened card, the program automatically
    matched the two and you do not need to open the already
    opened card
    """
    print "closed card indexes" 
    print player.show_closed_cards(board)

    my_index =  get_index("open first card: ")

    res = player.play(board, my_index)
    while res == False:
        my_index =  get_index("try first card again: ")
        res = player.play(board, my_index)
    if res == "pair found":
        return True
    my_index =  get_index("open second card: ")
    res = player.play(board, my_index)
    while res == False:
        my_index =  get_index("try second card again: ")
        res = player.play(board, my_index)
    if res == "pair found":
        return True
    return False
    

def one_game_robot(player, board):
    # one hand for the player
    """
    one hand for the robot
    open two cards. if the first card matches
    an already opened card, the program automatically
    matches the two and teh robot does not need to open the already
    opened card
    """

    my_index =  np.random.choice(board.closed_indexes)
    res = player.play(board, my_index)
    if res == "pair found":
        return True
    my_index =  np.random.choice(board.closed_indexes)
    res = player.play(board, my_index)
    if res == "pair found":
        return True
    return False

def play_game( robot_player = True, human_player = True ):
    
    """
    initialize the board and play the game
    if robot = True, robot is in the game
    if human = True, human is in the game
    """
    
    board = MyBoards()
    board.get_initial_boards()

    player = Player()
    robot = Player()

    robot_matches = 0
    player_matches = 0
    
    while len(board.removed_indexes) < 52:

        if human_player:
            print "*** human playing ***" 
            print "" 
            pair_found_player = True
            while pair_found_player and len(board.removed_indexes) < 52:
                pair_found_player = one_game(player, board)
                player_matches = len(player.show_matched_pairs())
                print "player matches =  %i"%player_matches 
                print "" 
            print "" 

        if robot_player:
            print "*** robot playing ***" 
            print ""
            pair_found_robot = True
            while pair_found_robot and len(board.removed_indexes)< 52:
                pair_found_robot = one_game_robot(robot, board)
                robot_matches = len(robot.show_matched_pairs())
                print "robot matches =  %i"%robot_matches
                print ""
            print ""

    print "******************************"
    if robot_player:
        print "robot score: %i"%robot_matches 
    if human_player:
        print "human score: %i"%player_matches 
    print "******************************"



parser = argparse.ArgumentParser()
parser.add_argument("--h", nargs='?', const=True, type=bool)
parser.add_argument("--r", nargs='?', const=True, type=bool)
args = parser.parse_args()
if args.h ==  True:
    human_player =  True
else:
    human_player = False
if args.r ==  True:
    robot_player =  True
else:
    robot_player = False


if __name__ == '__main__':
    play_game( robot_player = robot_player, human_player = human_player)




