// Polls every second
(function poll(){
   setTimeout(function(){
    console.log('yo');
      $.ajax({ url: "http://127.0.0.1:5000/counts", success: function(data){
        console.log(data);
        poll();
      }, dataType: "json"});
  }, 1000);
})();
