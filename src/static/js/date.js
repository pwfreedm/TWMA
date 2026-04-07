  function formatDate(date) {
    var month = (date.getMonth() + 1).toString().padStart(2, '0'); // Months are 0-indexed
    var day = date.getDate().toString().padStart(2, '0');
    return `${date.getFullYear()}-${month}-${day}`;
  }

  // Set the value of the input field to today's date
  window.onload = function() {
    document.getElementById("date").value = formatDate(new Date());
  }