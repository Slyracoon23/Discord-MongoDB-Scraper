import os
import requests
import time

import pymongo
from pymongo.errors import AutoReconnect, ConnectionFailure, ExecutionTimeout

class DiscordScraper:
    def __init__(self, channel_id, auth_token):
        self.channel_id = channel_id
        self.auth_token = auth_token
        self.url = "https://discord.com/api/v8/channels/{}/messages/search".format(channel_id)
        self.headers = {'Authorization': auth_token ,'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:20.0) Gecko/20100101 Firefox/20.0'}

    def get_messages(self):
        '''
        API Call only recieves ~25 of most recent messages
        '''
        response = requests.get( self.url, headers=self.headers)
        if response.status_code != 200:
            print(f"\nStatus Code: {response.status_code}")
            print(response.text)
            raise 

            
        return response.json()


class Mongo:
    def __init__(self, client_uri, db="Crypto-Currency-Discord", col="General-Chat"):
        self.client_uri = client_uri
        self.myclient = self.createClient()
        self.mydb = self.myclient[db]
        self.mycol = self.mydb[col]

    def createClient(self):
        try:
            myclient =  pymongo.MongoClient(self.client_uri , serverSelectionTimeoutMS=5000)
        except (AutoReconnect, ConnectionFailure) as e:
            print("Client Failed to Connect")
            raise 

        return myclient

    def updateDB(self, data):
        for post in reversed(data['messages']): # Reversed because first element is newest not oldest
            result = self.mycol.update_one(post[0],{"$set":post[0]},upsert=True)

        return
        




if __name__ == '__main__':

    # Variables
    channel_id = "848464764890775565"
    auth_token = os.environ['API_DISCORD_TOKEN']
    time_per_update = 10.0 # sec

    mongo_password = os.environ['MONGODB_PASSWORD']
    mongo_uri = f"mongodb+srv://scraper:{mongo_password}@discord-crypto.clfxu.mongodb.net"
 
    # instances
    scraper = DiscordScraper(channel_id,auth_token)
    
    mong = Mongo(mongo_uri)

    # Method calls
    starttime = time.time()
    while True:
        data = scraper.get_messages()
        mong.updateDB(data)
        time.sleep(time_per_update - ((time.time() - starttime) % time_per_update))



