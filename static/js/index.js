function Player(params) {
  "use strict";
  var self = this;
  self.pk = ko.observable();
  self.first_name = ko.observable(params.first_name || "");
  self.sex = ko.observable(params.sex || "m");
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

  self.players = ko.observableArray();

  self.addPlayer = function() {
    self.players.push(new Player({}));
  };

  self.addPlayer();

  var clearSelectedPlayers = function(players, cb) {
    var cleanPlayers = players.filter(function(player) {
      return (player.first_name() !== "");
    });
    async.map(cleanPlayers, function(player, cb) {
      $.ajax("/player/", {
        data: ko.toJSON({
          first_name : player.first_name,
          sex: player.sex
        }),
        type: "post", contentType: "application/json",
        success: function(data) {
          cb(null, data.pk);
        },
        error: function(err) {
          cb(err);
        }
      });
    }, function(err, results) {
      if(err) {
        return cb(err);
      }
      cb(null, results);
    });
  };

  self.createGame = function() {
    clearSelectedPlayers(self.players(), function(err, players) {
      if(err) {
        return console.log(err.responseText);
      }
      $.ajax("/post-game/", {
        data: ko.toJSON({
          category : self.selectedCategory().pk,
          players: players
        }),
        type: "post", contentType: "application/json",
        success: function(data) {
          window.location.replace("/game");
        },
        error: function(err) {
          console.log(err.responseText);
        }
      });
    });
  };

  return true;
}

ko.applyBindings(new CreateGameViewModel());
