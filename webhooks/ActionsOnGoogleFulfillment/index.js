const {conversation} = require('@assistant/conversation');
const functions = require('firebase-functions');

const app = conversation();

app.handle('start_scene_initial_prompt', (conv) => {
  console.log('Start scene: initial prompt');
  conv.overwrite = false;
  conv.scene.next = { name: 'actions.scene.END_CONVERSATION' };
  conv.add('Hi, today you have not yet vented and you have been doing good on tea. You have brewed 7 times so far.');
});

exports.ActionsOnGoogleFulfillment = functions.https.onRequest(app);
