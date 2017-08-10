try {
  jQuery();
} catch (ReferenceError) {
  throw Error('tutors.js requires jquery');
}
try {
  baseWsServerPath.valueOf();
} catch (ReferenceError) {
  throw Error('You need to set the baseWsServerPath variable before loading tutors.js');
}
try {
  sessionKey.valueOf();
} catch (ReferenceError) {
  throw Error('You need to set the sessionKey variable before loading tutors.js');
}
try {
  if (!Array.isArray(usersCheckList)) {
    throw Error('The variable usersCheckList must be an array');
  }
} catch (ReferenceError) {
  throw Error('You need to make the usersCheckList array before loading tutors.js');
}

$(document).ready(() => {
  /* global usersCheckList:false */

  const opponentUsername = '';

  let websocket = null;

  function setUserOnlineOffline(username, online) {
    const elem = $(`#user-${username}`);
    if (online) {
      elem.attr('class', 'online');
    } else {
      elem.attr('class', 'offline');
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
