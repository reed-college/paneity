/*
 * Gives the tutorchat page it's functionality
 * This code relies on the base_ws_server_path and session_key
 * variables being set before this file is loaded 
 */
$(document).ready(function () {
    // tell user they have no messages
    if ($("#old-message-div").html().replace(/\s/g,'') == ""){
        $("#new-message-div").html($("#no-messages-template").html());
    }

    // This will make it so that when you click on a row,
    // it takes you to that conversation
    $(".clickable-row").click(function() {
        window.open($(this).data("href"), '_blank');
    });

    var websocket = null;

    function setupChatWebSocket() {
        websocket = new WebSocket(base_ws_server_path + session_key + "/");

        websocket.onopen = function (event) {

            var onOnlineCheckPacket = JSON.stringify({
                type: "check-online",
                session_key: session_key,
            });
            var onConnectPacket = JSON.stringify({
                type: "online",
                session_key: session_key

            });

            console.log('connected, sending:', onConnectPacket);
            websocket.send(onConnectPacket);
            console.log('checking online opponents with:', onOnlineCheckPacket);
            websocket.send(onOnlineCheckPacket);
        };


        window.onbeforeunload = function () {

            var onClosePacket = JSON.stringify({
                type: "offline",
                session_key: session_key,
            });
            console.log('unloading, sending:', onClosePacket);
            websocket.send(onClosePacket);
            websocket.close();
        };


        websocket.onmessage = function (event) {
            var packet;

            try {
                packet = JSON.parse(event.data);
                console.log(packet)
            } catch (e) {
                console.log(e);
            }

            if (packet.type == "new-message") {
                var username = packet['sender_name'];
                // remove no message div and any message div with the same username
                $("#no-messages-element").remove()
                $("#"+username+"-element").remove()
                // add new message to new message div
                var newm = $("#new-message-template").html().replace(/\[username\]/g, username);
                console.log(newm);
                newm = newm + $("#new-message-div").html();
                $("#new-message-div").html(newm);
                isNewMessage = true;
                flash();
            }
        }
    }

    setupChatWebSocket();
});

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

// flashes the title once there is a new message
async function flash() {
    var oldtitle = document.title;
    while (isNewMessage) {
        await sleep(1000);
        document.title="New Message";
        await sleep(1000);
        document.title=oldtitle;
    }
}

// stop flashing once window is in focus
$(window).on("blur focus", function(e) {
    var prevType = $(this).data("prevType");

    if (prevType != e.type) {   //  reduce double fire issues
        switch (e.type) {
            case "blur":
                break;
            case "focus":
                isNewMessage = false;
                break;
        }
    }
    $(this).data("prevType", e.type);
})
