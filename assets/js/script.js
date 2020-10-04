$("#submitButton").click(function() {
  // Prep some data and POST ?
  $("#postTarget").attr("disabled", true);
  const postUrl = $("#postTarget").val();

  const postData = {
    type: "AF",
    amount: $("#amount").val(),
    position: {
      longitude: $("#longitude").val(),
      latitude: $("#latitude").val()
    },
    target: $("#target").val(),
    authKey: $("#apiToken").val()
  };
  $.ajax({
    url: postUrl,
    type: "POST",
    data: JSON.stringify(postData),
    cache: false,
    processData: false,
    contentType: "application/json",
    success: function(data) {
      window.alert("Successfully created dummy data.");
    },
    error: function() {
      console.log("error");
      window.alert(error);
    }
  });
  $("#postTarget").removeAttr("disabled");
});
