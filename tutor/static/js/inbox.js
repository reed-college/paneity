/*
 * Gives the inbox page it's functionality
 * This code relies on the baseWsServerPath and sessionKey
 * variables being set before this file is loaded
 */

// stops for the given number of miliseconds
function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

let isNewMessage = false;

/* eslint no-await-in-loop: "off" */
// flashes the title once there is a new message
async function flash() {
  const oldtitle = document.title;
  while (isNewMessage) {
    await sleep(1000);
    document.title = 'New Message';
    await sleep(1000);
    document.title = oldtitle;
  }
}

// stop flashing once window is in focus
$(window).on('blur focus', function stopFlash(e) {
  const prevType = $(this).data('prevType');

  if (prevType !== e.type) {   //  reduce double fire issues
    switch (e.type) {
      case 'blur':
        break;
      case 'focus':
        isNewMessage = false;
        break;
      default:
        break;
    }
  }
  $(this).data('prevType', e.type);
});

$(document).ready(() => {
  // tell user they have no messages
  if ($('#old-message-div').html().replace(/\s/g, '') === '') {
    $('#new-message-div').html($('#no-messages-template').html());
  }

  // This will make it so that when you click on a row,
  // it takes you to that conversation
  $('.clickable-row').click(function clickRow() {
    window.open($(this).data('href'), '_blank');
  });

  let websocket = null;

  function setupChatWebSocket() {
    websocket = new WebSocket(`${baseWsServerPath + sessionKey}/`);

    websocket.onopen = function websocketOpen() {
      const onOnlineCheckPacket = JSON.stringify({
        type: 'check-online',
        session_key: sessionKey,
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
      });
      websocket.send(onClosePacket);
      websocket.close();
    };


    websocket.onmessage = function handleMessage(event) {
      const packet = JSON.parse(event.data);

      if (packet.type === 'new-message') {
        const username = packet.sender_name;
        // remove no message div and any message div with the same username
        $('#no-messages-element').remove();
        $(`#${username}-element`).remove();
        // add new message to new message div
        let newm = $('#new-message-template').html().replace(/\[username\]/g, username);
        newm = newm.replace(/\[message\]/g, packet.message);
        newm += $('#new-message-div').html();
        $('#new-message-div').html(newm);
        // need to add click function for new row

        $(`#${username}-element`).click(function clickNewRow() {
          window.open($(this).data('href'), '_blank');
        });


        isNewMessage = true;
        flash();
      }
    };
  }

  setupChatWebSocket();
});
