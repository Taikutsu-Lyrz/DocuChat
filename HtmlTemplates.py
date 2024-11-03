
css = '''
<style>
.chat-message {
    padding: 1.5rem;
    border-radius: 0.5rem;
    margin-bottom: 1rem;
    display: flex;
    align-items: center; /* Ensure vertical alignment */
}
.chat-message.user {
    background-color: #2b313e;
}
.chat-message.bot {
    background-color: #475063;
    
}
.chat-message .avatar {
    flex: 0 0 auto;
    width: 20%;
    max-width: 100px; /* Ensures the avatar doesn't grow too large */
}
.chat-message .avatar img {
    width: 100%;
    height: auto;
    border-radius: 10%;
    object-fit: cover;
}
.chat-message .message {
    flex: 1;
    padding: 0 1.5rem;
    color: #fff;
    
   overflow-wrap: break-word;
    border-right: 2px solid;
    width: 0;
    animation: typing 3s steps(30, end) forwards, blink 0.5s step-end infinite;

}
</style>

'''



bot_template = '''
<div class="chat-message bot">
    <div class="avatar">
      <img src="https://i.ibb.co/gz8kQFm/Bot-final.png" alt="User" border="0">
    </div>
    <div class="message">{{MSG}}</div>
</div>
'''

user_template = '''
<div class="chat-message user">
    <div class="avatar">
       <img src="https://i.ibb.co/gvhGqnq/User.jpg" alt="User" border="0">
    </div>    
    <div class="message">{{MSG}}</div>
</div>
'''
