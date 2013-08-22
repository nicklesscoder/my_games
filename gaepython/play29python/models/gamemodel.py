from google.appengine.ext import db
import time
import random
import collections
from webapp2_extras import json

#GAME_STATES

WAITING_FOR_PLAYERS = "WAITING_FOR_PLAYERS"
SET_START = "SET_START"
SHUFFLE = "SHUFFLE"
DIST_1 = "DIST_1"
BID = "BID"
COLOR = "COLOR"
DIST_2 = "DIST_2"
PLAY_START = "PLAY_START"
IN_PLAY = "IN_PLAY"
PLAY_END = "PLAY_END"
SET_END = "SET_END"

#CARD_VAL
CARD_VALS = {
            14 : 1,
            13 : 0, 
            12 : 0,
            11 : 3,
            10 : 1,
            9  : 2,
            8  : 0,
            7  : 0
            }

CARD_TYPES = ["c", "h", "s" , "d"]

#move commands
def startSet(game):
    random.seed()
    distributer = random.randrange(6561) #3 ^ 8
    missed = ""
    game.cardsTakenByTeam0 = ""
    game.cardsTakenByTeam1 = ""
    vals = CARD_VALS.keys()
    for cardtype in CARD_TYPES:
        random.shuffle(vals);
        copyDist = distributer
        for val in vals:
            choice = copyDist%3;
            toappend = str(val) + cardtype + ","
            if choice == 2:
                missed += toappend
            elif choice == 1:
                game.cardsTakenByTeam1 += toappend 
            elif choice == 0:
                game.cardsTakenByTeam0 += toappend
            copyDist /= 3
                
    game.cardsTakenByTeam0  +=  missed
    game.addMove()
    game.gameState =  SHUFFLE
    
            
def shuffle(game):
    allcards = game.cardsTakenByTeam0 + game.cardsTakenByTeam1
    lstCards = allcards.split(",")
    lstCards.remove('')
    firstCut = random.randrange(32)
    secondCut = random.randrange(32)
    lstCards = collections.deque(lstCards)
    lstCards.rotate(firstCut)
    lstCards.rotate(secondCut)
    game.cardsTakenByTeam0 = ','.join(list(lstCards))
    game.cardsTakenByTeam1 = ""
    game.addMove()
    game.gameState =  DIST_1

def dist1(game):
    i = j = 0
    ndx = 0
    lstCards = game.cardsTakenByTeam0.split(",")
    while i < 4:
        curPlayer = (game.nextMoveOwner + i) % 4
        cards = ""
        j = 0
        while j < 4:
            cards += lstCards[ndx] + ","
            j += 1
            ndx += 1
        
        setattr(game, "cards" +  str(curPlayer), cards)    
        i+=1
    game.addMove()    
    game.gameState = BID


def dist2(game):
    i = j = 0
    ndx = 0
    lstCards = game.cardsTakenByTeam0.split(",")
    while i < 4:
        curPlayer = (game.nextMoveOwner + i) % 4
        cards = getattr(game, "cards" +  str(curPlayer))
        j = 0
        while j < 4:
            cards += lstCards[ndx] + ","
            j += 1
            ndx += 1
        
        setattr(game, "cards" +  str(curPlayer), cards)    
        i+=1
    game.addMove()    
    game.gameState = PLAY_START


def playStart():
    #resetAllThings
    pass

def setColorMove(game, move_type, move_str):
    if move_str in CARD_TYPES:
        game.addMove(game.gameStarter, game.nextMoveOwner, move_str)
        game.color = move_str
        game.colorPublic = False
        game.gameState = DIST_2
                                 

def bidMove(game, move_type, move_str):
    bidVal = int(move_str)
    bidValX2 = bidVal * 2
    nextBidX2 = game.getNextBidValueX2()
    changeToColorState = False
    if nextBidX2 % 2 == 1 and bidValX2 + 1 == nextBidX2:
        bidValX2 =  nextBidX2
        
    if bidValX2 >= nextBidX2:
        if game.bidOwner == -1:
            game.bidOwner = game.nextMoveOwner
            game.bidValX2 = bidValX2
            nextMover = (1 + game.nextMoveOwner)%4
                
        else:
            nextBidder = game.bidOwner
            game.bidOwner = game.nextMoveOwner
            game.bidValX2 = bidValX2
            nextMover = nextBidder
            
        
            
    elif game.bidOwner == -1:
        nextMover = (1 + game.nextMoveOwner)%4
        bidValX2 = -1
    else:
        
        numPasserFromGameStarted = (4 - game.gameStarter + game.nextMoveOwner)%4
        numBidOwnerFromGameStarted = (4 - game.gameStarter + game.bidOwner)%4
        
        if numBidOwnerFromGameStarted > numPasserFromGameStarted:
            nextMover = (1 + game.bidOwner)%4
        else:
            nextMover = (1 + game.nextMoveOwner)%4
            
        if nextMover == game.gameStarter:
            if game.bidOwner == -1:
                game.bidOwner = game.nextMoveOwner
                game.bidValX2 = 35
                bidValX2 = 35
            
            nextMover = game.bidOwner
            changeToColorState = True
    
    game.addMove(nextMover, game.nextMoveOwner, bidValX2)        
    if changeToColorState:
        game.gameState = COLOR
            
        
            
def getMaxBid(cardAnalysis):
    maxBid = -1
    if(cardAnalysis.hasColorJ and cardAnalysis.numberColor > 2):
        maxBid = 17 + (cardAnalysis.colorPoints - 3)
        maxBid = 17
        maxBid += int(cardAnalysis.numberColor/2)
        if(cardAnalysis.hasOtherJ):
            maxBid += 1
    elif cardAnalysis.numberColor == 4:
        maxBid = 19
        
    return maxBid
    
           
                
def aiBidMove(game):
    nextBid = int(game.getNextBidValueX2()/2)
    cardAnalysis = CardAnalysis(getattr(game, "cards" +  str(game.nextMoveOwner)) )
    maxBid = getMaxBid(cardAnalysis)
    if(maxBid >= nextBid):
        bidMove(game, BID, int(nextBid/2))
    else:
        bidMove(game, BID, -1)
    
    
                
            
            
AI_MOVERS = {
             BID: aiBidMove,
             }    
    
    

SERVER_STATE_TO_CMD = {SET_START : startSet, 
                             SHUFFLE : shuffle, 
                             DIST_1 : dist1,
                             DIST_2 : dist2, 
                             PLAY_START : playStart, 
                             PLAY_END : None
                             }
USER_STATE_TO_CMD = {
                     BID: bidMove,
                     COLOR: setColorMove
                     }


def relative_string(elapsed):
    """ Takes a time delta and expresses it as a relative string """
    if elapsed < 2 * 60:
        result = "1 minute ago"
    elif elapsed < 60 * 60:
        result = "%d minutes ago" % (elapsed / 60)
    elif elapsed < 2 * 60 * 60:
        result = "1 hour ago"
    elif elapsed < 24 * 60 * 60:
        result = "%d hours ago" % (elapsed / (60 * 60))
    elif elapsed < 48 * 60 * 60:
        result = "1 day ago"
    else:
        result = "%d days ago" % (elapsed / (24 * 60 * 60))
    return result

class Game(db.Model):

    playerId0 = db.StringProperty()
    playerId1 = db.StringProperty()
    playerId2 = db.StringProperty()
    playerId3 = db.StringProperty()
    
    #playerAIs bitmasked with player number
    playerAIs = db.IntegerProperty(default=0, required=True);
    
    publicGame = db.BooleanProperty(default=False, required=True)
    
    canShowInLobby = db.BooleanProperty(default=True, required=True) 
    
    gameTypeIsSingle = db.BooleanProperty(required=True)
    
    # timestamp is updated on create
    created = db.DateTimeProperty(auto_now_add=True)
    
    # timestamp is updated on every refresh
    lastModified = db.DateTimeProperty(auto_now=True)
    
    # Description of the state of this game. See the GAME_STATE values
    gameState = db.StringProperty(required=True, default=WAITING_FOR_PLAYERS)
    
    scoreTeam0 = db.IntegerProperty(default=0)
    scoreTeam1 = db.IntegerProperty(default=0)

    cards0 = db.StringProperty()
    cards1 = db.StringProperty()
    cards2 = db.StringProperty()
    cards3 = db.StringProperty()
    
    cardsTakenByTeam0 = db.StringProperty()
    cardsTakenByTeam1 = db.StringProperty()
    
    bidValX2 = db.IntegerProperty(default=-1, required = True );
    bidOwner = db.IntegerProperty(default=-1, required = True)
    color = db.StringProperty();
    colorPublic = db.BooleanProperty(default = False)
    
    #nextMoveOwner is player number (one of 0,1,2,3)
    nextMoveOwner = db.IntegerProperty(default = 0)
    gameStarter = db.IntegerProperty(default = 0)
    moveData = db.StringListProperty(default=[])
    

    def get_creation_time(self):
        """ Returns the creation time, rendered as a string. We could do timezone
            math, but for now (because it's easy) we'll just emit a time delta
            (e.g. "15 minutes ago")
        """
        elapsed = time.time() - time.mktime(self.created.timetuple())
        return relative_string(elapsed)

    def get_last_modified(self):
        """ Returns the last modification date as a reasonably formatted string """
        elapsed = time.time() - time.mktime(self.last_modified.timetuple())
        return relative_string(elapsed)
    
    
    def to_lobby_dict(self):
        result = {}
        result['key']           = str(self.key())
        result["playerId0"]     = self.playerId0
        result["playerId1"]     = self.playerId1
        result["playerId2"]     = self.playerId2
        result["playerId3"]     = self.playerId3
        result["playerAIs"]     = self.playerAIs
        result["publicGame"]    = self.publicGame
        result["canShowInLobby"]= self.canShowInLobby
        result["gameTypeIsSingle"]  = self.gameTypeIsSingle
#         result["created"]       = relative_string(self.created) 
#         result["lastModified"]  = relative_string(self.lastModified) 
        result["gameState"]     = self.gameState 
        return result
        
    def to_game_dict(self):
        result = self.to_lobby_dict()
        result["scoreTeam0"]    = self.scoreTeam0 
        result["scoreTeam1"]    = self.scoreTeam1
        result["bidValX2"]      = self.bidValX2
        result["bidOwner"]      = self.bidOwner
        result["colorPublic"]   = self.colorPublic
        result["nextMoveOwner"] = self.nextMoveOwner
        
        if(self.colorPublic) :
            result["color"]      = self.color
            
        return result;
    
    def getLastMove(self):
        moveStr = self.moveData[-1]
        move = json.decode(moveStr)
        return move
            
    
    def addMove(self, nextMover = 0, mover=None, param=None):
        move = {
                "num" : len(self.moveData),
                "state" : self.gameState,
                "mover" : mover,
                "param" : param,
                }
        moveStr = json.encode(move)
        self.moveData.append(moveStr)
        self.nextMoveOwner = nextMover 
        
    def getMovesArrayFrom(self, movesFrom, playerNum):
        moves = []
        for strMove in self.moveData[movesFrom:] :
            move = json.decode(strMove)
            if (move["state"] == DIST_1 or move["state"] == DIST_2):
                move["params"] = getattr(self, "cards" +  str(playerNum)) 
            moves.append(move)
            
        return moves
    
    def getNextBidValueX2(self):
        if self.bidValX2 == -1:
            return 35
        return self.bidValX2 + 1
        

class CardAnalysis:
    def __init__(self, cards):
        self.hasColorJ = False
        self.numberColor = 0
        self.color = ""
        self.colorPoints = 0
        self.hasOtherJ = False
        number = ''
        suit = ''
        suitToCards = {
                       'c' : [],
                       's' : [],
                       'h' : [],
                       'd' : []
                       }
        numJs = 0;
        maxSuit = None
        for c in cards:
            if c.isdigit():
                number+=c
            elif c != ",":
                suit = c
            else:
                if(number == "11"):
                    numJs += 1
                suitToCards[suit].append(int(number))
                if(len(suitToCards[suit]) > 2):
                    maxSuit = suit
                number = ''
                suit = ''
            
        if maxSuit is None:
            return
        else:
            self.color = maxSuit
            self.numberColor = len(suitToCards[maxSuit])
            for number in suitToCards[maxSuit]:
                if numJs > 0:
                    if number == 11:
                        self.hasColorJ = True
                        if numJs > 1:
                            self.hasOtherJ = True    
                    
                self.colorPoints += CARD_VALS[number]
            
                
                
            
        
    
    