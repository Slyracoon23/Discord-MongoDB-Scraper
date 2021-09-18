# import requests

# channel_id = "848464764890775565"

# headers = {'Authorization': 'NDI3NTQyODg1ODQ0NjQ3OTQ3.YS2nmQ.8C5lnmOXRC82_gPMGoZjGHkyTN0'}

# url = "https://discord.com/api/v8/channels/{}/messages/search".format(channel_id)

# response = requests.get( url, headers=headers)

# assert response.status_code == 200
# # print(response.text)

# data = response.json()
########################################################################333
######################## DISCORD END ######################################
########################################################################333

############################################################################
#################### MONGODB START #########################################
########################################################################333

import pymongo

myclient =   pymongo.MongoClient("mongodb+srv://dbUser:AXfdXe5Sy2cX32q@discord-crypto.clfxu.mongodb.net", serverSelectionTimeoutMS=5000)
print(myclient.server_info())
mydb = myclient["Crypto-Currency-Discord"]
mycol = mydb["General-Chat"]


mydict = { "name": "John", "address": "Highway 37" }


for post in data['messages']:
    result = mycol.update_one(post[0],{"$set":post[0]},upsert=True)