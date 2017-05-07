'use strict';

var LightTableFilter = (function(Arr) {

  var _input;

  function _onInputEvent(e) {
    _input = e.target;
    var tables = document.getElementsByClassName(_input.getAttribute('data-table'));
    Arr.forEach.call(tables, function(table) {
      Arr.forEach.call(table.tBodies, function(tbody) {
        Arr.forEach.call(tbody.rows, _filter);
      });
    });
  }

  function _filter(row) {
    var text = row.textContent.toLowerCase(), val = _input.value.toLowerCase();
    row.style.display = text.indexOf(val) === -1 ? 'none' : 'table-row';
  }

  return {
    init: function() {
      var inputs = document.getElementsByClassName('light-table-filter');
      Arr.forEach.call(inputs, function(input) {
        input.oninput = _onInputEvent;
      });
    }
  };
})(Array.prototype);

document.addEventListener('readystatechange', function() {
  if (document.readyState === 'complete') {
    LightTableFilter.init();
  }
});



function searchTable(){
  // Declare variables
  var input, filter, table, tr, td, i;
  input = document.getElementById("txtSearch");
  filter = input.value.toUpperCase();
  table = document.getElementById("listUsers");
  tr = table.getElementsByTagName("tr");

  // Loop through all table rows, and hide those who don't match the search query
  for (i = 0; i < tr.length; i++) {
    td = tr[i].getElementsByTagName("td")[0];
    if (td) {
      if (td.innerHTML.toUpperCase().indexOf(filter) > -1) {
        tr[i].style.display = "";
      } else {
        tr[i].style.display = "none";
      }
    }
  }
};
