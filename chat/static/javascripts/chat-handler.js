var socket = io.connect("http://" + document.domain + ":" + location.port);

socket.on("connect", function () {
  socket.emit("my event", {
    data: "User Connected",
  });
  var form = $("form").on("submit", function (e) {
    e.preventDefault();
    let user_input = $("input.chat-input").val();
    socket.emit("my event", {
      message: user_input,
    });
    $("input.message").val("").focus();
  });
});
socket.on("my response", function (msg) {
  console.log(msg);
  $("h3").remove();
  $("div.message_holder").append(
    '<div><b style="color: #000">' + msg.message + "</div>"
  );
});
