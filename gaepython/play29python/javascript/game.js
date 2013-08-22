var game = {
		/******** Game States ********/
		WAITING_FOR_PLAYERS : "WAITING_FOR_PLAYERS",
		SET_START : "SET_START",
		SHUFFLE : "SHUFFLE",
		DIST_1 : "DIST_1",
		BID : "BID",
		COLOR : "COLOR",
		DIST_2 : "DIST_2",
		PLAY_START : "PLAY_START",
		IN_PLAY : "IN_PLAY",
		PLAY_END : "PLAY_END",
		SET_END : "SET_END",
		SERVER_MOVE_STATES : null,


		moveList: [],
		movesToApply: [],
		gamedata: null,
		myPlayerNumber: 0,
		ownerUid: 0,
		twentynine: null,
		
		/********** functions ************/
		setAllData: function(uid, gamedata) {
			game.gamedata = gamedata;
			game.myPlayerNumber = 0;
			game.twentynine = new TwentyNine(gamedata, game.myPlayerNumber)
			game.ownerUid = uid;
			game.SERVER_MOVE_STATES = [game.SET_START, game.SHUFFLE, game.DIST_1, game.DIST_2, game.PLAY_START, game.PLAY_END];
			   // Start refreshing the page as soon as we are loaded
			   game.refreshBoard();
			  

			//   // Corner-ify items
			//   $('.timeDisplay').corner({autoPad:true, validTags:["div"]});
			//   $('.waitingForOpponent').corner({autoPad:true, validTags:["div"]});
			//   $('.yourTurn').corner({autoPad:true, validTags:["div"]});

			   // TODO: Set onbeforeunload() handler to catch when user navigates away
			   // so we can warn the user first if he has a game in progress
		},
		
		refreshBoard: function() {
		    // hit the ajax handler to load our game data
		    var options = {
		      url: "/move",
		      dataType: "json",
		      type: "POST",
		      data: {moves_from: game.moveList.length, game_key:game.gamedata.key},
		      error: handlers.retryOnFail,
		      success: game.onServerResponse
		    };
		    $.ajax(options);
		  },
		  
		  putMove: function(move_type, move_str) {
			  var options = {
				      url: "/move",
				      dataType: "json",
				      type: "PUT",
				      data: {move_num: game.moveList.length, game_key:game.gamedata.key, move_type: move_type, move_str:move_str},
				      error: handlers.retryOnFail,
				      success: game.onServerResponse
				    };
				    $.ajax(options);
		  },
		  
		  onServerResponse: function(response){
			  game.updateGame(response.m);
			  game.gamedata = response.g;
		  },
		
		  // Handle a game update from the server - update our game state, then
		  // update the ui.
		  updateGame: function(moves) {
			if(moves.length > 0){
				movesToApply = moves;
				game.applyMoves();
			}  
			else{
				if(game.gamedata.nextMoveOwner == game.myPlayerNumber){
					if(game.SERVER_MOVE_STATES.indexOf(game.gamedata.gameState) >= 0){
						game.putMove("server", game.gamedata.gameState);
					}else{
						//wait For User Input
						game.waitForUserAction();
						
					}
				}else{
					setTimeout(game.refreshBoard, 500);
				}
			}
		  },
		  
		  applyMoves: function() {
			  var move = movesToApply.shift();
			  game.twentynine.applyMove(move);
			  game.moveList.push(move);
			  game.gamedata.nextMoveOwner = move.nextMover
		  },
		  
		  onMoveApplied: function(){
			  game.updateGame(movesToApply);
		  },
		  
		  waitForUserAction:function(){
			  game.twentynine.waitForUserAction(game.gamedata.gameState);
		  },
		  
		  bid:function(val){
			  game.putMove(game.BID, val);
		  },
		  
		  setColor:function(suit){
			  game.putMove(game.COLOR, suit);
		  }

};




