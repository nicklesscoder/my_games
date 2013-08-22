function CardGame(game_data)
{
	// private variables
	this.game_data = game_data;
	this.cards = [];
//	this.card_value = ["1C","2C","3C","4C","5C","6C","7C","8C","1H","2H","3H","4H","5H","6H","7H","8H"];
	this.card_value = ["1","2","3","4","5","6","8","9","10","11","12","13","14","15","16","17"];
	this.started = false;
	// initialise

	var stage = document.getElementById("stage");
	var felt = document.createElement("div");
	felt.id = "felt";
	stage.appendChild(felt);

	// template for card
	var cardBack = document.createElement("div");
	cardBack.innerHTML = "<img src=\"/images/cards/b1fv.png\">";

	for(var i=0; i < 16; i++) {
		var newCard = cardBack.cloneNode(true);
		if(i < 4){
			newCard.fromtop = 15;
			newCard.fromleft = 190 + 40 * (i%4);
		}
		else if(i < 8){
			newCard.fromtop =  135 + 40 * (i%4);
			newCard.fromleft =  420;
		}
		else if(i < 12){
			newCard.fromtop =  375;
			newCard.fromleft = 190 + 40 * (i%4);
		}else {
			newCard.fromtop =  135 + 40 * (i%4);
			newCard.fromleft = 60;
		}

		felt.appendChild(newCard);
		this.cards.push(newCard);
	}
}

CardGame.prototype.moveToPlace = function(id) // deal card
{
	this.cards[id].matched = false;
	cardgame = this;
	with(this.cards[id].style) {
		angle = Math.floor( id/4 ) * 90;
		zIndex = "1000";
		top = this.cards[id].fromtop + "px";
		left = this.cards[id].fromleft + "px";
		WebkitTransform = MozTransform = OTransform = msTransform = "rotate(" + angle +"deg)";
		zIndex = "0";
		if(id >= 8 && id < 12){
			setTimeout(function() { cardgame.showCard(id);}, 1000);
		}
	}
}

CardGame.prototype.showCard = function(id) // turn card face up, check for match
{
//	if(id === card1) return;
	if(this.cards[id].matched) return;

	this.cards[id].firstChild.src = "/images/cards/" + this.card_value[id] + ".png";
	with(this.cards[id].style) {
		WebkitTransform = MozTransform = OTransform = msTransform = "scale(1.2) rotate(185deg)";
	}
	
}
CardGame.prototype.cardClick = function(id)
{
	if(this.started) {
		showCard(id);
	} else {
		// shuffle and deal cards
		this.card_value.sort(function() { return Math.round(Math.random()) - 0.5; });
		cardgame = this;
		for(i=0; i < 16; i++) {
			(function(idx) {
				setTimeout(function() { cardgame.moveToPlace(idx); }, idx * 100);
			})(i);
		}
		started = true;
	}
}

CardGame.prototype.distribute = function()
{
//	for(i=0; i < 16; i++) {
		this.cardClick(-1);
//	}
}
