/*
 * This is the js that makes the django_private_chat/dialogs.html page work
 * The variables baseWsServerPath and sessionKey and the function
 * getOpponentUsername need to be set before this file is loaded in order
 * for this to work
 * also needs the moment.js library
 */

$(document).ready(() => {
  let websocket = null;

  function scrollToLastMessage() {
    const $msgs = $('#messages');
    $msgs.scrollTop($msgs.prop('scrollHeight'));
  }

  function addNewMessage(packet) {
    let msgElem = '';
    if (packet.sender_name === $('#owner_username').val()) {
      msgElem = $('#message-template-owner').html();
    } else {
      msgElem = $('#message-template-opponent').html();
    }
    msgElem = msgElem.replace(/\[message\]/g, packet.message);
        // convert to local time
    const created = moment().utc(packet.created, 'MMM D, YYYY, hh:mm a');
    let crestr = created.format('MMMM D, YYYY, h:mm a');
        // replaces am/pm with a.m./p.m.
    crestr = crestr.replace(/([a,p])m$/g, '$1.m.');
    msgElem = msgElem.replace(/\[timestamp\]/g, crestr);
    $('#messages').append(msgElem);
    scrollToLastMessage();
  }

  function setUserOnlineOffline(username, online) {
    const elem = $(`#user-${username}`);
    if (online) {
      elem.attr('class', 'btn btn-success');
    } else {
      elem.attr('class', 'btn btn-danger');
    }
  }

  function goneOnline() {
    $('#offline-status').hide();
    $('#online-status').show();
  }

  function goneOffline() {
    $('#online-status').hide();
    $('#offline-status').show();
  }

  function setupChatWebSocket() {
    const opponentUsername = getOpponnentUsername();
    websocket = new WebSocket(`${baseWsServerPath + sessionKey}/${opponentUsername}`);

    websocket.onopen = function websocketOpen() {
      const onOnlineCheckPacket = JSON.stringify({
        type: 'check-online',
        session_key: sessionKey,
        username: opponentUsername,
                // Sending username because the user needs to know if his opponent is online
      });
      const onConnectPacket = JSON.stringify({
        type: 'online',
        session_key: sessionKey,

      });

      websocket.send(onConnectPacket);
      websocket.send(onOnlineCheckPacket);
    };


    window.onbeforeunload = function websocketClose() {
      const onClosePacket = JSON.stringify({
        type: 'offline',
        session_key: sessionKey,
        username: opponentUsername,
                // Sending username because to let opponnent know that the user went offline
      });
      websocket.send(onClosePacket);
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
          if (packet.usernames.indexOf(opponentUsername) !== -1) {
            goneOnline();
          } else {
            goneOffline();
          }
          for (let i = 0; i < packet.usernames.length; i += 1) {
            setUserOnlineOffline(packet.usernames[i], true);
          }
          break;
        case 'gone-offline':
          if (packet.username === opponentUsername) {
            goneOffline();
          }
          setUserOnlineOffline(packet.username, false);
          break;
        case 'new-messagee':
          if (packet.sender_name === opponentUsername || packet.sender_name === $('#owner_username').val()) {
            addNewMessage(packet);
          }
          break;
        case 'opponent-typing': {
          const typingElem = $('#typing-text');
          if (!typingElem.is(':visible')) {
            typingElem.fadeIn(500);
          } else {
            typingElem.stop(true);
            typingElem.fadeIn(0);
          }
          typingElem.fadeOut(3000);
          break;
        }
        default:
          console.error('error: ', event);
      }
    };
  }

  function sendMessage(message) {
    const opponentUsername = getOpponnentUsername();
    const newMessagePacket = JSON.stringify({
      type: 'new-message',
      session_key: sessionKey,
      username: opponentUsername,
      message,
    });
    websocket.send(newMessagePacket);
  }

  $('#chat-message').keypress(function userTyping(e) {
    if (e.which === 13 && this.value) {
      sendMessage(this.value);
      this.value = '';
      return false;
    }
    const opponentUsername = getOpponnentUsername();
    const packet = JSON.stringify({
      type: 'is-typing',
      session_key: sessionKey,
      username: opponentUsername,
      typing: true,
    });
    websocket.send(packet);
    return true;
  });

  $('#btn-send-message').click(() => {
    const $chatInput = $('#chat-message');
    const msg = $chatInput.val();
    if (!msg) return;
    sendMessage($chatInput.val());
    $chatInput.val('');
  });

    // sends a message when you click the videochat button
  $('#btn-video-call').click(() => {
    sendMessage($('#vc-link-message-template').html());
  });

  setupChatWebSocket();
  scrollToLastMessage();
});
