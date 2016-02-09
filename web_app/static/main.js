function update_view(data){
    $("#emojis").empty();
    console.log(data.length);
    $.each(data, function(index, value) {
        $("#emojis").append("<li>" + index + ": " + value + "</li>");
    });
}

// Polls every second
(function poll(){
   setTimeout(function(){
      $.ajax({ url: "http://127.0.0.1:5000/counts", success: function(data){
        console.log(data);
        update_view(data);
        poll();
      }, dataType: "json"});
  }, 1000);
})();
