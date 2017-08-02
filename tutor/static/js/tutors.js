
$(document).ready(() => {
  let websocket = null;

  function setUserOnlineOffline(username, online) {
    const elem = $(`#user-${username}`);
    if (online) {
      elem.attr('class', 'btn btn-success');
    } else {
      elem.attr('class', 'btn btn-danger');
    }
  }

  function setupChatWebSocket() {
    websocket = new WebSocket(`${baseWsServerPath + sessionKey}/`);

    websocket.onopen = function websocketOpen() {
      const onOnlineCheckPacket = JSON.stringify({
        type: 'list-check-online',
        session_key: sessionKey,
      });
      websocket.send(onOnlineCheckPacket);
    };


    window.onbeforeunload = function websocketClose() {
      websocket.close();
    };


    websocket.onmessage = function websocketMessage(event) {
      const packet = JSON.parse(event.data);

      switch (packet.type) {
        case 'new-dialog':
          break;
        case 'user-not-found':
          // TODO: dispay some kind of an error that the user is not found
          break;
        case 'gone-online':
          for (let i = 0; i < packet.usernames.length; i += 1) {
            setUserOnlineOffline(packet.usernames[i], true);
          }
          break;
        case 'gone-offline':
          setUserOnlineOffline(packet.username, false);
          break;
        default:
          console.error('error: ', event);
      }
    };
  }
  setupChatWebSocket();
});
