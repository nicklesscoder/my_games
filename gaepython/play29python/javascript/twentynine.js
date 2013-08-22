var CARD_VALS = {
            14 : 1,
            13 : 0, 
            12 : 0,
            11 : 3,
            10 : 1,
            9  : 2,
            8  : 0,
            7  : 0
            };

var CARD_TYPES = ["c", "h", "s" , "d"];

function TwentyNine(gameData, myPlayerNumber) {
	this.gameData = gameData;
	this.myPlayerNumber = myPlayerNumber;
	this.nextMoveNum = 0;
	this.myCards = [];
	this.cardDobs = [];
	this.lastBidX2 = 34; 
};

TwentyNine.prototype = {};

TwentyNine.MOVE_APPLIER_MAP = {
		SET_START : "setStartMove",
		SHUFFLE : "shuffleMove",
		DIST_1 : "dist1Move",
		BID : "bidMove",
		COLOR : "colorMove",
		DIST_2 : "dist2Move",
		PLAY_START : "playStartMove",
		IN_PLAY : "playHandMove",
		PLAY_END : "playEndMove",
		SET_END : "setEndMove"
};

TwentyNine.UACT_APPLIER_MAP = {
		BID : "waitForBid",
		COLOR : "waitForSetColor",
		IN_PLAY : "waitToPlayHand",
};

TwentyNine.prototype.applyMove = function(move) {
	if(move.num == this.nextMoveNum){
		var applier = TwentyNine.MOVE_APPLIER_MAP[move.state];
		this[applier](move);
		this.nextMoveNum += 1;
		
	}else{
		alert("out of sync moves");
	}
};

TwentyNine.prototype.waitForUserAction = function(state) {
	var waitFn = TwentyNine.UACT_APPLIER_MAP[state];
	this[waitFn]();
};

TwentyNine.prototype.onMoveApplied = function() {
	setTimeout(function() { game.onMoveApplied(); }, 500);
};

/*** move appliers*****/
TwentyNine.prototype.setStartMove = function(move) {
	this.createCards();
	this.onMoveApplied();
};


TwentyNine.prototype.shuffleMove = function(move) {
	this.onMoveApplied();
}

TwentyNine.prototype.dist1Move = function(move) {
	this.myCards = move.params.split(",");

	for(i=0; i < 32; i++) {
		if(i % 8 < 4){
			this.moveToPlaceAfter(i, i * 100);
		}
	}
	for(i=16; i < 20; i++ ){
		this.showCardAfter(i, 3200);
	}
	
	setTimeout(this.onMoveApplied, 3200);
}

TwentyNine.prototype.bidMove = function(move) {
	this.showOthersBid(move.mover, move.param)
	setTimeout(this.hideOthersBid, 3200);
	setTimeout(this.onMoveApplied, 3200);
}


/******* user actions ***/
TwentyNine.prototype.waitForBid = function(){
	this.showBidUI();
}

TwentyNine.prototype.waitForSetColor = function(){
	$( "#setColorDialog" ).dialog( "open" );
}

/***** util functions ****/
TwentyNine.prototype.showBidUI = function(){
	var minVal = Math.floor(this.lastBidX2/2)
	if(this.lastBidX2 % 2 == 1){
		
		minVal += 1 ;
	}
	$( "#bidSlider" ).slider( "option", "min", minVal );
	$( "#bidSlider" ).slider( "option", "max", minVal + 10 );
	$( "#bidDialog" ).dialog( "open" );
};

TwentyNine.prototype.showOthersBid = function(mover, bidValX2){
	$( "#bidShowDialog" ).dialog( "open" );
	$("#bidOwner").text ("player " + mover);
	if(bidValX2 == -1){
		$("#bidValue").text("pass");
	}else{
		if( bidValX2 % 2 == 1){
			actVal = Math.floor(bidValX2/2); 
			value = actVal + "ditto";
		}else{
			value = Math.floor(bidValX2/2);
		}
		$("#bidValue").text(value);
		this.lastBidX2 = bidValX2;
	}
};

TwentyNine.prototype.hideOthersBid = function(mover, value){
	$( "#bidShowDialog" ).dialog( "close" );
};


TwentyNine.prototype.moveToPlaceAfter = function(idx, timeInt){
	cardgame = this;
	setTimeout(function() { cardgame.moveToPlace(idx); },timeInt);
}

TwentyNine.prototype.showCardAfter = function(idx, timeInt){
	cardgame = this;
	setTimeout(function() { cardgame.showCard(idx); },timeInt);
}

TwentyNine.prototype.createCards = function() {
	var stage = document.getElementById("stage");
	var felt = document.createElement("div");
	felt.id = "felt";
	stage.appendChild(felt);
	var cardBack = document.createElement("div");
	cardBack.innerHTML = "<img src=\"/images/cards/b1fv.png\">";

	for(var i=0; i < 32; i++) {
		var newCard = cardBack.cloneNode(true);
		if(i < 8){
			newCard.fromtop = 25;
			newCard.fromleft = 200 + 40 * (i%4);
		}
		else if(i < 16){
			newCard.fromtop =  175 + 40 * (i%4);
			newCard.fromleft =  500;
		}
		else if(i < 24){
			newCard.fromtop =  475;
			newCard.fromleft = 200 + 40 * (i%4);
		}else {
			newCard.fromtop =  175 + 40 * (i%4);
			newCard.fromleft = 25;
		}

		felt.appendChild(newCard);
		this.cardDobs.push(newCard);
	}
};

TwentyNine.prototype.moveToPack = function(id) // move card to pack
{
  hideCard(id);
  with(cardDobs[id].style) {
    zIndex = "1000";
    top = "100px";
    left = "-140px";
    WebkitTransform = MozTransform = OTransform = msTransform = "rotate(0deg)";
    zIndex = "0";
  }
};

TwentyNine.prototype.moveToPlace = function(id) // deal card
{
	with(this.cardDobs[id].style) {
		angle = Math.floor( id/4 ) * 90;
		zIndex = "1000";
		top = this.cardDobs[id].fromtop + "px";
		left = this.cardDobs[id].fromleft + "px";
		WebkitTransform = MozTransform = OTransform = msTransform = "rotate(" + angle +"deg)";
		zIndex = "0";
	}
};


TwentyNine.prototype.showCard = function(id) // turn card face up, check for match
{
	this.cardDobs[id].firstChild.src = "/images/cards/" + this.myCards[id - 16] + ".png";
};

TwentyNine.prototype.hideCard = function(id) // turn card face down
{
	this.cardDobs[id].firstChild.src = "/images/cards/b1fv.png";
	with(this.cardDobs[id].style) {
		WebkitTransform = MozTransform = OTransform = msTransform = "scale(1.0) rotate(180deg)";
	}
};

