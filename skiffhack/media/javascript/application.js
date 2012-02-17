$(document).ready(function(){

  // Temporary thing while people might still have the herokuapp.com
  // address.Needs to be on the right domain or browserid will fail.
  if (document.location.hostname === 'skiffprofile.herokuapp.com') {
    document.location = 'http://who.theskiff.org';
  }

  // Enable browserid loggin
  $('.browserid').bind('click', function(e) {
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

  // If we're in the profile list then ask the skiff presence system
  // for presence information.
  if ($('.profile-list').length > 0) {
    $.get("http://crane.papercreatures.com/recent",function(data) {
      $('body').addClass('presenceLoaded');
      $.each(data.recent, function(index,seen) {
        $('.e' + seen.hash).addClass("available");
      });
    },"jsonp");
  }

  $.timeago.settings.strings.prefixAgo = "Last seen at The Skiff ";
  if (PROFILE_USER_HASH) {
    $.get("http://crane.papercreatures.com/status/" + PROFILE_USER_HASH,function(data) {
      if (!data.known) {
        $('#attheskiff').text('');
      } else if (data.present) {
        $('#attheskiff').text('At the skiff now!').addClass('available');
      } else {
        $('#attheskiff').attr("title", data.last_seen).timeago();
      }
    },"jsonp");
  }
  
});
