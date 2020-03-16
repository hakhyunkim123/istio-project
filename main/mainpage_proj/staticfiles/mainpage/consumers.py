from channels.generic.websocket import AsyncWebsocketConsumer
import json
import os, requests
from . import views


MESSAGE_URL='http://'+os.environ.get('MESSAGE_IP')+":"+os.environ.get('MESSAGE_PORT')
LOGIN_URL = 'http://' + os.environ.get('LOGIN_IP') + ':' + os.environ.get('LOGIN_PORT') 
USERID=""
#LOCAL_URL = 'http://' + os.environ.get('LOCAL_IP') + ':' + os.environ.get('LOCAL_PORT')

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = self.room_name

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()


    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        userId = text_data_json['userId']
        print(userId)
        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'userId' : userId
            }
        )
        #URL=LOCAL_URL+"/proj/whoami/"
        global USERID
        USERID=views.USERID
        #print(userId)
        URL=MESSAGE_URL+'/saveChat'
        data={
                "projId": self.room_name,
                "user": USERID,
                "content":message}
        requests.post(URL, data=data)

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']
        global USERID
        USERID=views.USERID
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message, 
            'userId' : USERID,
        }))

