Talk.ready.then(function () {
    var me = new Talk.User({
      id: localStorage.getItem('groupiee_uname'),
      name: localStorage.getItem('groupiee_uname'),
      photoUrl: 'https://demo.talkjs.com/img/alice.jpg',
      welcomeMessage: 'Hey there! How are you? :-)',
    });
    window.talkSession = new Talk.Session({
      appId: 'tngFxsxz',
      me: me,
    });
    var other = new Talk.User({
      id: document.getElementById('uname').innerText,
      name: document.getElementById('uname').innerText,
      photoUrl: '/file/{{pfp_src}}',
      welcomeMessage: 'Hey, how can I help?',
    });
  

var conversation = window.talkSession.getOrCreateConversation(
  Talk.oneOnOneId(me, other)
);
conversation.setParticipant(me);
conversation.setParticipant(other);
var popup = window.talkSession.createPopup();
popup.select(conversation);
popup.mount({ show: false });

var button = document.getElementById('chatbtn');
button.addEventListener('click', function (event) {
  event.preventDefault();
  popup.show();
});
})