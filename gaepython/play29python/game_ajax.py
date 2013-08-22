from play29 import BasePage
from webapp2_extras import json
from models.gamemodel import Game
from models import gamemodel

class BaseGameAJAX(BasePage):
    
    def Get(self):
        self.response.headers['Content-Type'] = 'text/javascript'
        
    def getUserPlayerNumber(self, game):
        return 0
    
    def isNextMoveOwnerAI(self, game ):
        return ((1 << game.nextMoveOwner) & game.playerAIs) > 0
    
    def getNextNonAIPlayer(self, game):
        return 0; 

class SinglePlayerGameCreator(BaseGameAJAX):
    
    def createSinglePlayerGame(self):
        game = Game(playerId0 = self.current_user["uid"], playerAIs = 14, publicGame = False, gameTypeIsSingle=True, canShowInLobby= False, nextMoveOwner=0, gameState=gamemodel.SET_START)
        return game
    
    def Get(self):
        BaseGameAJAX.Get(self)
        newGame = self.createSinglePlayerGame()
        newGame.put()
        self.response.write(str(newGame.key()));
        

class GameMoveHandler(BaseGameAJAX):
    
    def validateMove(self, game, move_num, move_type, move_str):
        return True
    
    def gameInServerState(self, game):
        return game.gameState in gamemodel.SERVER_STATE_TO_CMD
    
    def completeServerState(self, game):
        methodToCall = gamemodel.SERVER_STATE_TO_CMD[game.gameState]
        if methodToCall:
            methodToCall(game)

    def completeAIMove(self, game):
        methodToCall = gamemodel.AI_MOVERS[game.gameState]
        methodToCall(game)
    
    def userMove(self, game, move_type, move_str):
        methodToCall = gamemodel.USER_STATE_TO_CMD[game.gameState]
        methodToCall(game, move_type, move_str) 
    
    def Get(self):
        BaseGameAJAX.Get(self)
        movesFrom = int(self.request.get('moves_from'))
        game_key = self.request.get('game_key')
        game = Game.get(game_key)
        userPlayerNumber = self.getUserPlayerNumber(game)
        game_data_changed = False
        
        
        if self.isNextMoveOwnerAI(game):
            userPlayerNumber = self.getUserPlayerNumber(game)
            
            if self.getNextNonAIPlayer(game) == userPlayerNumber :
                
                while self.gameInServerState(game):
                    self.completeServerState(game)
                    game_data_changed = True
                
                while  self.isNextMoveOwnerAI(game):
                    self.completeAIMove(game)
                    game_data_changed = True
                
        if game_data_changed:
            game.put()
                
        self._returnResponse(game,movesFrom) 
    
            
        
    def Put(self):
        move_num = int(self.request.get('move_num'))
        game_key = self.request.get('game_key')
        move_type = self.request.get('move_type')
        move_str = self.request.get('move_str')
        game = Game.get(game_key)
        movesSaved = game.moveData
        if(len(movesSaved) == move_num) :
            if move_type == "server": 
                if move_str == game.gameState and self.gameInServerState(game):
                    while self.gameInServerState(game):
                        self.completeServerState(game)
                    game.put()
            elif self.validateMove(game, move_num, move_type, move_str):
                self.userMove(game, move_type, move_str)
                game.put()
        
        self._returnResponse(game,move_num)
        
    def _returnResponse(self, game, fromMoveNum):
        self.response.write(json.encode({'g': game.to_game_dict(), 'm':game.getMovesArrayFrom(fromMoveNum, 0)}))
            