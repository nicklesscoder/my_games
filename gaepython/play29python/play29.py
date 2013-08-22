import webapp2
from google.appengine.ext.webapp.util import run_wsgi_app
from base_handler import BasePage
from game_ajax import SinglePlayerGameCreator, GameMoveHandler
from models.gamemodel import Game
from webapp2_extras import json

config = {}
config['webapp2_extras.sessions'] = dict(secret_key='kKKKKKKKKK*')


class MainPage(BasePage):
    
    def Get(self):
        template_values = self.getBaseTemplateVals()
        #self.renderTemplate('test.html', template_values)
        self.renderTemplate('main.html', template_values)


class LobbyPage(BasePage):
    
    def get(self):
        self.forceLogin()
        template_values = {}
        self.addUserParamsToTemplateValues(template_values)
        self.renderTemplate('lobby.html', template_values)
        
class BaseGamePage(BasePage):
    pass
    
        

class GamePage(BaseGamePage):

    def get(self):
        template_values = self.getBaseTemplateVals()
        game_key = self.request.path.strip('/').split('/')[-1]
        game_data = Game.get(game_key)
        template_values['game_data'] = json.encode(game_data.to_game_dict())
        self.renderTemplate('game.html', template_values)



application = webapp2.WSGIApplication(
                                      [
                                       ('/', MainPage),
                                       ('/lobby', LobbyPage),
                                       ('/game/.*', GamePage),
                                       #('/lobby_ajax.*', lobby_ajax.LobbyHandler),
                                       ('/single', SinglePlayerGameCreator),
                                       ('/move', GameMoveHandler)
                                       ],
                                      debug=True,
                                      config=config
                                      )

def main():
    run_wsgi_app(application)

if __name__ == '__main__':
    main()
