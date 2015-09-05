/********************
  INIT VARS
  INIT AJAX CSRF
********************/
var csrftoken = Cookies.get('csrftoken');
function csrfSafeMethod(method) {
  // these HTTP methods do not require CSRF protection
  return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
  beforeSend: function(xhr, settings) {
    if(!csrfSafeMethod(settings.type) && !this.crossDomain) {
      xhr.setRequestHeader("X-CSRFToken", csrftoken);
    }
  }
});




ko.bindingHandlers.autoComplete = {
  // Only using init event because the
  // Jquery.UI.AutoComplete widget will take care of the update callbacks
  init: function(element, valueAccessor, allBindings, viewModel, bindingContext) {
    // valueAccessor = { selected: mySelectedOptionObservable, options: myArrayOfLabelValuePairs }
    var settings = valueAccessor();

    var selectedOption = settings.selected;
    var options = settings.options;

    var updateElementValueWithLabel = function(event, ui) {
      // Stop the default behavior
      event.preventDefault();

      // Update the value of the html element with the label
      // of the activated option in the list (ui.item)
      $(element).val(ui.item.label);

      // Update our SelectedOption observable
      if(typeof ui.item !== "undefined") {
        // ui.item - id|label|...
        selectedOption(ui.item);
      }
    };

    $(element).autocomplete({
      source: options,
      select: function(event, ui) {
        updateElementValueWithLabel(event, ui);
      },
    });
  }
};
