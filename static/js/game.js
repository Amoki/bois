function RuleViewModel() {
  "use strict";
  var self = this;

  self.rule = ko.observable();

  self.nextTurn = function() {
    $.ajax("/next-turn/", {
      type: "post", contentType: "application/json",
      success: function(result) {
        $.getJSON("/last-turn/", function(rule) {
          self.rule(rule.string);
        });
      },
      error: function(err) {
        console.error(err);
      }
    });
  };

  self.nextTurn();

}

ko.applyBindings(new RuleViewModel());
