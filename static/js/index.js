function Player(params) {
  "use strict";
  var self = this;
  self.pk = ko.observable(params.pk);
  self.first_name = ko.observable(params.first_name);
  self.last_name = ko.observable(params.last_name);
  self.sex = ko.observable(params.sex);
}

function CreateGameViewModel() {
  "use strict";

  var self = this;

  self.availableCategories = ko.observableArray([]);

  self.selectedCategory = ko.observable();

  $.getJSON("/categories/", function(categories) {
      $.map(categories, function(category) {
        self.availableCategories.push(category);
      });
  });

  self.availableSex = [{
    value: 'm',
    printName: 'Homme'
  }, {
    value: 'f',
    printName: 'Femme'
  }];

  self.playerCreation = ko.observable(false);
  self.playerCreationFisrtName = ko.observable("");
  self.playerCreationLastName = ko.observable("");
  self.playerCreationSex = ko.observable(self.availableSex[0].value);

  self.selectedPlayers = ko.observableArray([]);

  self.addPlayer = function(player) {
    self.selectedPlayers.push(new Player(player || {}));
  };

  self.selectedPlayerOption = function(item) {
    self.addPlayer(item.value);
  };


  $.getJSON("/players/", function(players) {
    self.playerOptions = $.map(players, function(player) {
      return {
        label: player.first_name + ' ' + player.last_name,
        value: player,
      };
    });

    // Hack to create a first blank input with list of available players is loaded
    self.addPlayer();
  });



  self.removePlayer = function(player) {
    self.selectedPlayers.remove(player);

    // Can't have 0 item on the list
    if(self.selectedPlayers().length === 0) {
      self.addPlayer();
    }
  };

  self.createPlayer = function() {
    self.playerCreation(true);
  };

  self.cancelPlayerCreation = function() {
    self.playerCreation(false);
  };

  self.commitPlayer = function() {
    var player = {
      first_name: self.playerCreationFisrtName(),
      last_name: self.playerCreationLastName(),
      sex: self.playerCreationSex().value,
    };
    $.ajax("/player/", {
      data: ko.toJSON(player),
      type: "post", contentType: "application/json",
      success: function(result) {
        self.addPlayer(result);
      },
      error: function(err) {
        console.error(err);
      }
    });
    self.playerCreation(false);
  };


  var clearSelectedPlayers = function(selectedPlayers) {
    return selectedPlayers.filter(function(player) {
      if(!player.pk) {
        return false;
      }
      return true;
    }).map(function(player) {
      return player.pk;
    });
  };

  self.createGame = function() {
    $.ajax("/post-game/", {
      data: ko.toJSON({
        category : self.selectedCategory().pk,
        players: clearSelectedPlayers(self.selectedPlayers())
      }),
      type: "post", contentType: "application/json",
      success: function(data) {
        window.location.replace("/game");
      },
      error: function(err) {
        console.error(err);
      }
    });
  };
  return true;
}

ko.applyBindings(new CreateGameViewModel());
