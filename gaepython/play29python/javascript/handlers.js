var handlers = {


  /**
   * Prepares a dialog for display, and displays it.
   */
  initAndDisplayDialog: function(dialog) {
    // Clear out any errors and text fields
    $(dialog).find(".error").hide();
    $(dialog).find(":text").val("");
    $(dialog).modal();
  },

  updateZebraTables: function() {
    $("table.zebra tr:even").addClass("even");
    $("table.zebra tr:odd").addClass("odd");
  },

  // Error handler for ajax requests
  retryOnFail: function (xhr, textStatus, errorThrown) {
	  var ajaxOptions = this;
	  FB.login(function(response) {
		  
	   if (response.authResponse) {
		   if (xhr.status == 410) {
			      // Whatever entity we are trying to access has been deleted
			      alert("Sorry, this game has been deleted.");
			      handlers.clickHandlers.enterLobby();
			      return;
			    }
			    // Just try sending the request again - if the server is down, this can
			    // lead to an infinite loop, so we put in a delay and try it every few
			    // seconds.
			    window.setTimeout(function() { $.ajax(ajaxOptions);}, 2*1000);
		   } else {
		     console.log('User cancelled login or did not fully authorize.');
		   }
		 });
    
  },

  dialogActive: function() {
    // Returns true if there's currently a dialog up - useful if we want to
    // avoid displaying multiple dialogs at once
    return ($.modal.impl && $.modal.impl.dialog && $.modal.impl.dialog.data);
  },


  /**
   * The handlers for click events
   */
  clickHandlers: {
	  playSingle: function() {
		  var options = {
			      url: "/single",
			      type: "GET",
			      dataType: "text",
			      success: function(data) {handlers.clickHandlers.goGame(data);},
			      error: function() {
			        alert("Could q not create game");
			      }
			    }
		$.ajax(options);
    },

    gotoMain: function() {
      window.location.href = "/";
    },

    enterLobby: function() {
      window.location.href = "/lobby";
    },

    inviteFriend: function() {
      handlers.initAndDisplayDialog("#inviteFriendDialog");
    },

    whatIsGame: function() {
    	handlers.initAndDisplayDialog("#whatIsGameDialog");
    },

    // Invoked when the user clicks on the "sendInvite" button in the dialog
    sendInvite: function() {
      lobby.sendInvite();
    },

    closeModal: function() {
      $.modal.close();
    },

    sendLobbyChat: function() {
      lobby.sendChat();
    },

    // Given a game key, switches to view that game
    goGame: function(gameKey) {
      window.location.href = "/game/" + gameKey;
    },

    sendGameChat: function() {
      game.sendChat();
    },

    offerNewGame: function() {
    	handlers.initAndDisplayDialog("#offerGameDialog");
    }
  }
};

