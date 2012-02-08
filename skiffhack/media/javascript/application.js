$(document).ready(function(){

  // Enable browserid loggin
  $('#browserid').bind('click', function(e) {
    e.preventDefault();
    navigator.id.getVerifiedEmail(function(assertion) {
      if (assertion) {
        var $e = $('#id_assertion');
        $e.val(assertion.toString());
        $e.parent().submit();
      }
    });
  });
  
  // If logging in from The Skiff AND we have permission to track the
  // current user then call out to the presence server.
  if(AT_THE_SKIFF && TRACK_PRESENCE) {
    $.ajax({
      type :'POST',
      url : 'http://192.168.11.10:5000/ident',
      contentType: 'application/json',
      data: JSON.stringify({ hash: CURRENT_USER_HASH}),
      dataType: 'json'
    });
  }

  // Ask the skiff presence system for presence information.
  $.get("http://crane.papercreatures.com/recent",function(data) {
    $.each(data.recent, function(index,seen) {
      console.log(seen.hash);
      $('.e' + seen.hash).addClass("available");
    });
  },"jsonp");
  
});
