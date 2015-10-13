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
    var i=0;
    async.eachLimit(self.players(), 5, function(player, cb){
      $.ajax("/player/", {
        data: ko.toJSON({
          first_name : player.first_name,
          sex: player.sex
        }),
        type: "post", contentType: "application/json",
        success: function(data) {
          self.players()[i].pk(data.pk);
          i += 1;
          cb();
        },
        error: function(err) {
          cb(err);
        }
      });
    }, function(err) {
      if(err) {
        return console.log(err.responseText);
      }
      $.ajax("/post-game/", {
        data: ko.toJSON({
          category : self.selectedCategory().pk,
          players: clearSelectedPlayers(self.players())
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
