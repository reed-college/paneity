$(document).ready(() => {
  /* global usersCheckList:false */

  const opponentUsername = '';

  let websocket = null;

  function setUserOnlineOffline(username, online) {
    const elem = $(`#user-${username}`);
    if (online) {
      elem.attr('class', 'circle online');
    } else {
      elem.attr('class', 'circle offline');
    }
  }

  function setupChatWebSocket() {
    websocket = new WebSocket(`${baseWsServerPath + sessionKey}/${opponentUsername}`);

    websocket.onopen = function websocketOpen() {
      const onOnlineCheckPacket = JSON.stringify({
        type: 'list-check-online',
        session_key: sessionKey,
        // Send the users we want to check the status of
        users_list: usersCheckList,
        // need opponentUsername in order to get this websocket
        username: opponentUsername,
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
          console.log(packet);
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
