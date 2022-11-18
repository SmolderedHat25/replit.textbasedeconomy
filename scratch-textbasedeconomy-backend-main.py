import os
from replit import db
import scratchattach as scratch3
import time
import random
import math
from threading import Thread
import json
import jsonpickle

#Thread(target=savenload)
#jsonpickle.decode(file)

try:
  def main():
    #file = open('data.json')
    #file = json.load(file)
    #d = {"data": {}, "gameData": {"lottery": {"lotteryList": [], "lastLottery": time.time(), "lotteryAmount": 0}}}
    #to = jsonpickle.encode(d)
    #db['fullData'] = to
    #print(db['fullData'])
    encoded = db['fullData']
    fullData = jsonpickle.decode(encoded)
    data = fullData["data"]
    
    data['Air_heads']['items']['ecoins']['amount'] = float('inf')
    data['Air_heads']['job']['jobNum'] = '-1'
  
    shop = {
      "banknote": {"buyPrice": 10000, "sellPrice": 9000, "useable": "True", "expireTime": 0, "function": "bankSpace",
                   "maxNum": float('inf'), "description": "Increases bank space."},
      "landmine": {"buyPrice": 30000, "sellPrice": 25000, "useable": "True", "expireTime": 86400,
                   "function": "walletProtection", "maxNum": 3, "description": "Protect your wallet. Blows up a enemy."},
      "paperclip": {"buyPrice": 15000, "sellPrice": 5000, "useable": "True", "expireTime": 18000, "function": "robItem",
                    "maxNum": 5, "description": "Pick the lock on a padlock."},
      "padlock": {"buyPrice": 25000, "sellPrice": 15000, "useable": "True", "expireTime": 86400,
                  "function": "walletProtection", "maxNum": 3, "description": "Protect your wallet by adding a padlock."},
      "dummy": {"buyPrice": 20000, "sellPrice": 14000, "useable": "True", "expireTime": 18000, "function": "robItem",
                "maxNum": 5, "description": "Decreases the chance of you getting blown up by a landmine."},
      "lotteryticket": {"buyPrice": 10000, "sellPrice": 1000, "useable": "False", "function": "lottery",
                        "maxNum": float('inf'), "description": "Participate in the hourly lottery!"},
      "soccerball": {"buyPrice": 'not buyable', "sellPrice": '1000000', "useable": "False", "function": "event", "maxNum": 1, "description": "Thanks for playing in the game's 'kick-off' (alpha)"},
      "guard": {"buyPrice": 50000, "sellPrice": 30000, "useable": "True", "expireTime": 86400,
                   "function": "walletProtection", "maxNum": 3, "description": "Protect your wallet by posting a guard outside."},
      "katana": {"buyPrice": 35000, "sellPrice": 10000, "useable": "True", "expireTime": 18000, "function": "robItem",
                    "maxNum": 4, "description": "Defeat a guard posted outside."},
      "fidgetspinner": {"buyPrice": 25000, "sellPrice": 10000, "useable": "True", "expireTime": 18000, "function": "luck",
                    "maxNum": 5, "description": "Increases your luck with gambles and begging while it spins."},
      "suit": {"buyPrice": 10000, "sellPrice": 5000, "useable": "True", "expireTime": 18000, "function": "workMul",
                    "maxNum": 5, "description": "Makes you look professional when you work. Increases amount earned from working by x2"}
          }
  
    session = scratch3.Session(mysessionid, username='Air_heads')
    conn = session.connect_cloud("718028360")
    client = scratch3.CloudRequests(conn, ignore_exceptions=True)
  
    print("starting server")
  
    print(db['fullData'])
  
  
    @client.request
    def ping():
      return "Pong."
  
    def savenload():
      while True:
        to = jsonpickle.encode(fullData)
        db['fullData'] = to
        time.sleep(5)
  
    @client.request
    def getPlayerJson(argument1):
      chars = """AabBCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789 -_`~!@#$%^&*()+=[];:'"\|,.<>/?}{"""
  
      def encode(text):
        encoded = ""
        length = int(len(text))
        for i in range(0, length):
          try:
            x = int(chars.index(text[i]) + 1)
            if x < 10:
              x = str(0) + str(x)
            encoded = encoded + str(x)
          except Exception:
            print(f"invalid char {text[i]}")
        return encoded
  
      return encode(str(data[argument1]))
  
  
    @client.request
    def checkAccount(argument1):
      global data
      users = list(data.keys())
      if argument1 in users:
        return_data = "| Loaded data!"
      else:
        fullData["data"][argument1] = {"items": {"ecoins": {"amount": 5000, "useable": "False"}}, "lastBeg": 0, "username":{argument1}, "level": 1, "bank": {"bankSpace": 5000, "bankCoins": 0, "bankIntrestTime": int(time.time())}, "daily": {"lastDaily": 0, "streak": 0}, "inbox": [], "job": {"jobNum": "0", "lastWork": 0, "streak": 0}, "rob": {"lastRob": int(time.time()), "lastRobbed": int(time.time())}, "itemsInUse": {}, "trade": {"canTrade": 'True', "lastTrade": 0}}
        
        return_data = "| Created account!"
  
      return return_data
  
  
    @client.request
    def addEcoins(argument1, argument2):
      data[argument1]["items"]["ecoins"]["amount"] = data[argument1]["items"]["ecoins"]["amount"] + float(argument2)
      return "added coins"
  
  
    @client.request
    def subEcoins(argument1, argument2):
      data[argument1]["items"]["ecoins"]["amount"] = data[argument1]["items"]["ecoins"]["amount"] - float(argument2)
      return "subtracted coins"
  
  
    @client.request
    def use(argument1, argument2):
      req = argument2.split(".")
      name = req[0]
      num = req[1]
      num = int(num)
      return_data = ""
      invenNames = list(data[argument1]["items"].keys())
      if name in invenNames:
        inventory = data[argument1]["items"]
        if inventory[name]["useable"] == "True":
          if not inventory[name]["amount"] - num < 0:
            if name == 'banknote':
              data[argument1]["bank"]["bankSpace"] = data[argument1]["bank"]["bankSpace"] + (num * random.randint(5000, 15000))
              data[argument1]["items"]["banknote"]["amount"] = data[argument1]["items"]["banknote"]["amount"] - num
            elif name == 'fidgetspinner':
              data[argument1]["itemsInUse"][name] = {"function": inventory[name]["function"], "expireTime": random.randint(5000, 18000), "useTime": int(time.time())}
              data[argument1]["items"][name]["amount"] = data[argument1]["items"][name]["amount"] - num
            else:
              data[argument1]["itemsInUse"][name] = {"function": inventory[name]["function"], "expireTime": inventory[name]["expireTime"], "useTime": int(time.time())}
              data[argument1]["items"][name]["amount"] = data[argument1]["items"][name]["amount"] - num
            return_data = "You are now using the item!"
          else:
            return_data = "You dont have that item."
        else:
          return_data = "This item is not useable."
      else:
        return_data = "That item does not exist."
      return return_data
  
  
    @client.request
    def sendTrade(argument1, argument2):
      return_data = ""
      req = argument2.split(" ")
      userToTrade = req[len(req) - 1].replace('@', '')
  
      players = list(data.keys())
      if userToTrade in players:
        pass
      else:
        return_data = "Player does not exist."
        return return_data
  
      if data[argument1]['trade']["canTrade"] == 'True':
        pass
      else:
        return_data = "You cant trade yet! (Wait 5 minutes, or wait until the other person accepts/declines.)"
        return return_data
  
      req.pop(len(req) - 1)
      myTrade = []
      uTrade = []
      i = 0
      while req[i] != 'for':
        myTrade.append(req[i])
        i += 1
      i += 1
      while i != len(req):
        uTrade.append(req[i])
        i += 1
  
      i = 0
      print(myTrade)
      print(uTrade)
  
      fakeInven = data[argument1]["items"]
      if ((len(myTrade) + len(uTrade)) % 2) == 0:
        while i != len(myTrade):
          itemNames = list(shop.keys())
          itemNames.append('ecoins')
          if myTrade[i] in itemNames:
            invenNames = list(data[argument1]["items"].keys())
            if myTrade[i] in invenNames:
              myTrade[i + 1] = float(myTrade[i + 1])
              if not (fakeInven[myTrade[i]]["amount"]) - (myTrade[i + 1]) < 0:
                fakeInven[myTrade[i]]["amount"] = fakeInven[myTrade[i]]["amount"] - myTrade[i + 1]
                if i != len(myTrade):
                  i += 2
              else:
                return_data = f"You do not have that many of this item: {myTrade[i]}"
                return return_data
            else:
              return_data = f"You do not have this item: {myTrade[i]}"
              return return_data
          else:
            return_data = f"This item does not exist: {myTrade[i]}"
            return return_data
  
        fakeInven = data[userToTrade]["items"]
        i = 0
        while i != len(uTrade):
          itemNames = list(shop.keys())
          itemNames.append('ecoins')
          if uTrade[i] in itemNames:
            invenNames = list(data[userToTrade]["items"].keys())
            if uTrade[i] in invenNames:
              uTrade[i + 1] = float(uTrade[i + 1])
              if not (fakeInven[uTrade[i]]["amount"]) - (uTrade[i + 1]) < 0:
                fakeInven[uTrade[i]]["amount"] = fakeInven[uTrade[i]]["amount"] - uTrade[i + 1]
                if i != len(uTrade):
                  i += 2
              else:
                return_data = f"Player does not have that many of this item: {uTrade[i]}"
                return return_data
            else:
              return_data = f"Player does not have this item: {uTrade[i]}"
              return return_data
          else:
            return_data = f"This item does not exist: {uTrade[i]}"
            return return_data
  
      else:
        return_data = "Invalid trade syntax."
        return return_data
  
      try:
        output = ""
        i = 0
        while i != len(uTrade) - 2:
          output = f"{output}({uTrade[i]}|{uTrade[i + 1]})"
          i += 2
        if i != len(uTrade):
          output = f"{output}({uTrade[len(uTrade) - 2]}|{uTrade[len(uTrade) - 1]})"
  
        output = f"{output} FOR "
  
        i = 0
        while i != len(myTrade) - 2:
          output = f"{output}({myTrade[i]}|{myTrade[i + 1]})"
          i += 2
        if i != len(myTrade):
          output = f"{output}({myTrade[len(myTrade) - 2]}|{myTrade[len(myTrade) - 1]})"
  
        inbox = data[userToTrade]['inbox']
        inbox.append(f"Trade from @{argument1}: {output}")
        inbox.append(int(time.time()))
        inbox.append(300)
        data[userToTrade]['inbox'] = inbox
  
        data[argument1]['trade']['canTrade'] = "False"
        data[argument1]['trade']['lastTrade'] = int(time.time())
  
        return "Sent trade!"
  
      except Exception:
        return_data = "Invalid trade syntax."
  
      return return_data
  
    @client.request
    def acceptTrade(argument1, argument2):
      string = argument2
      argument2 = argument2.replace("(", "")
      argument2 = argument2.replace(")", "")
      argument2 = argument2.replace("|", " ")
      req = argument2.split(" ")
      userToTrade = req[2].replace(":", "")
      userToTrade = userToTrade.replace("@", "")
      req.pop(0)
      req.pop(0)
      req.pop(0)
      myTrade = []
      uTrade = []
      i = 0
      while req[i] != 'FOR':
        myTrade.append(req[i])
        i += 1
      i += 1
      while i != len(req):
        uTrade.append(req[i])
        i += 1
  
      print(myTrade)
      print(uTrade)
  
      i = 0
      fakeInven = data[argument1]["items"]
      if ((len(myTrade) + len(uTrade)) % 2) == 0:
        while i != len(myTrade):
          itemNames = list(shop.keys())
          itemNames.append('ecoins')
          if myTrade[i] in itemNames:
            invenNames = list(data[argument1]["items"].keys())
            if myTrade[i] in invenNames:
              myTrade[i + 1] = float(myTrade[i + 1])
              print((fakeInven[myTrade[i]]["amount"]) - (myTrade[i + 1]))
              if not (fakeInven[myTrade[i]]["amount"]) - (myTrade[i + 1]) < 0:
                fakeInven[myTrade[i]]["amount"] = fakeInven[myTrade[i]]["amount"] - myTrade[i + 1]
                if i != len(myTrade):
                  i += 2
              else:
                return_data = f"You do not have that many of this item: {myTrade[i]}"
                return return_data
            else:
              return_data = f"You do not have this item: {myTrade[i]}"
              return return_data
          else:
            return_data = f"This item does not exist: {myTrade[i]}"
            return return_data
  
        fakeInven = data[userToTrade]["items"]
        i = 0
        while i != len(uTrade):
          itemNames = list(shop.keys())
          itemNames.append('ecoins')
          if uTrade[i] in itemNames:
            invenNames = list(data[userToTrade]["items"].keys())
            if uTrade[i] in invenNames:
              uTrade[i + 1] = float(uTrade[i + 1])
              if not (fakeInven[uTrade[i]]["amount"]) - (uTrade[i + 1]) < 0:
                fakeInven[uTrade[i]]["amount"] = fakeInven[uTrade[i]]["amount"] - uTrade[i + 1]
                if i != len(uTrade):
                  i += 2
              else:
                return_data = f"Player does not have that many of this item: {uTrade[i]}"
                return return_data
            else:
              return_data = f"Player does not have this item: {uTrade[i]}"
              return return_data
          else:
            return_data = f"This item does not exist: {uTrade[i]}"
            return return_data
  
      else:
        return_data = "Invalid trade syntax."
        return return_data
  
      i = 0
      while i != len(myTrade):
        data[argument1]["items"][myTrade[i]]["amount"] = data[argument1]["items"][myTrade[i]]["amount"] - float(myTrade[i+1])
        if myTrade[i] in list(data[userToTrade]["items"].keys()):
          if myTrade[i] != 'ecoins':
            if not data[userToTrade]["items"][myTrade[i]]["amount"] + float(myTrade[i+1]) > shop[myTrade[i]]["maxNum"]:
              data[userToTrade]["items"][myTrade[i]]["amount"] = data[userToTrade]["items"][myTrade[i]]["amount"] + float(myTrade[i + 1])
            else:
              return_data = f"Player does not have space for the item: {myTrade[i]}"
              return return_data
          else:
            data[userToTrade]["items"][myTrade[i]]["amount"] = data[userToTrade]["items"][myTrade[i]]["amount"] + float(myTrade[i+1])
        else:
          data[userToTrade]["items"][myTrade[i]] = {}
          data[userToTrade]["items"][myTrade[i]]["amount"] = 0
          data[userToTrade]["items"][myTrade[i]]["useable"] = shop[myTrade[i]]["useable"]
          if shop[myTrade[i]]["useable"] == "True":
            data[userToTrade]["items"][myTrade[i]]["expireTime"] = shop[myTrade[i]]["expireTime"]
          data[userToTrade]["items"][myTrade[i]]["function"] = shop[myTrade[i]]["function"]
          data[userToTrade]["items"][myTrade[i]]["amount"] = data[userToTrade]["items"][myTrade[i]]["amount"] + float(myTrade[i + 1])
  
        i += 2
  
      i = 0
      while i != len(uTrade):
        data[userToTrade]["items"][uTrade[i]]["amount"] = data[userToTrade]["items"][uTrade[i]]["amount"] - float(uTrade[i+1])
        if uTrade[i] in list(data[argument1]["items"].keys()):
          if uTrade[i] != 'ecoins':
            if not data[argument1]["items"][uTrade[i]]["amount"] + float(uTrade[i + 1]) > shop[uTrade[i]]["maxNum"]:
              data[argument1]["items"][uTrade[i]]["amount"] = data[argument1]["items"][uTrade[i]]["amount"] + float(uTrade[i + 1])
            else:
              return_data = f"You do not have space for the item: {uTrade[i]}"
              return return_data
          else:
            data[argument1]["items"][uTrade[i]]["amount"] = data[argument1]["items"][uTrade[i]]["amount"] + float(uTrade[i + 1])
        else:
          data[argument1]["items"][uTrade[i]] = {}
          data[argument1]["items"][uTrade[i]]["amount"] = 0
          data[argument1]["items"][uTrade[i]]["useable"] = shop[uTrade[i]]["useable"]
          if shop[uTrade[i]]["useable"] == "True":
            data[argument1]["items"][uTrade[i]]["expireTime"] = shop[uTrade[i]]["expireTime"]
          data[argument1]["items"][uTrade[i]]["function"] = shop[uTrade[i]]["function"]
          data[argument1]["items"][uTrade[i]]["amount"] = data[argument1]["items"][uTrade[i]]["amount"] + float(uTrade[i + 1])
  
        i += 2
  
      inbox = data[userToTrade]['inbox']
      inbox.append(f"Trade: Successfully traded with @{argument1}!")
      inbox.append(int(time.time()))
      inbox.append(86400)
      data[userToTrade]['inbox'] = inbox
      data[userToTrade]["trade"]["canTrade"] = "True"
      data[userToTrade]["trade"]["lastTrade"] = 0
  
      inbox = data[argument1]['inbox']
      index = inbox.index(string)
      inbox.pop(index)
      inbox.pop(index)
      inbox.pop(index)
      data[argument1]['inbox'] = inbox
  
      return_data = f"Successfully traded with @{userToTrade}!"
      return return_data
  
    @client.request
    def declineTrade(argument1, argument2):
      string = argument2
      inbox = data[argument1]['inbox']
      i = inbox.index(argument2)
      inbox.pop(i)
      inbox.pop(i)
      inbox.pop(i)
      data[argument1]["inbox"] = inbox
      argument2 = argument2.replace("(", "")
      argument2 = argument2.replace(")", "")
      argument2 = argument2.replace("|", " ")
      req = argument2.split(" ")
      userToTrade = req[2].replace(":", "")
      userToTrade = userToTrade.replace("@", "")
      data[userToTrade]["trade"]["canTrade"] = "True"
      data[userToTrade]["trade"]["lastTrade"] = 0
      inbox = data[userToTrade]['inbox']
      inbox.append(f"Trade: @{argument1} declined the trade.")
      data[userToTrade]['inbox'] = inbox
  
      inbox = data[argument1]['inbox']
      index = inbox.index(string)
      inbox.pop(index)
      inbox.pop(index)
      inbox.pop(index)
      data[argument1]['inbox'] = inbox
  
      return_data = "Declined trade."
      return return_data
  
    @client.request
    def addItem(argument1, argument2):
      data[argument1]["items"][argument2] = {}
      data[argument1]["items"][argument2]["amount"] = 1
      data[argument1]["items"][argument2]["useable"] = shop[argument2]["useable"]
      if shop[argument2]["useable"] == "True":
        data[argument1]["items"][argument2]["expireTime"] = shop[argument2]["expireTime"]
      data[argument1]["items"][argument2]["function"] = shop[argument2]["function"]
  
  
    @client.request
    def addInbox(argument1, argument2):
      add = argument2.split("$")
      inbox = data[argument1]['inbox']
      inbox.append(add[0])
      inbox.append(int(time.time()))
      inbox.append(int(add[1]))
      data[argument1]['inbox'] = inbox
      return 'inbox updated'
  
  
    @client.request
    def addLevel(argument1, argument2):
      data[argument1]["level"] = data[argument1]["level"] + float(argument2)
      return "added level"
  
  
    @client.request
    def getLevel(argument1):
      return data[argument1]["level"]
  
  
    @client.request
    def removeUse(argument1, argument2):
      data[argument1]["itmesInUse"].pop(argument2, None)
      return "removed item"
  
  
    @client.request
    def loadPlayerList():
      users = list(data.keys())
      return_data = []
      for i in users:
        return_data.append(f"| {i}")
      return return_data
  
  
    @client.request
    def rob(argument1, argument2):
      users = list(data.keys())
      return_data = []
      if argument2 in users:
        pass
      else:
        return_data.append("Err")
        return_data.append("That player does not exist!")
        return return_data
  
      if round(time.time()) - data[argument1]["rob"]["lastRob"] > 3600:
        if round(time.time()) - data[argument2]["rob"]["lastRobbed"] > 3600:
          users = list(data.keys())
          return_data = []
          if argument2 in users:
            itemsInUse = list(data[argument2]["itemsInUse"].keys())
            return_data.append(data[argument2]["items"]["ecoins"]["amount"])
            for i in itemsInUse:
              if data[argument2]["itemsInUse"][i]["function"] == "walletProtection":
                return_data.append(i)
            data[argument1]["rob"]["lastRob"] = time.time()
            data[argument2]['rob']['lastRobbed'] = time.time()
          else:
            return_data.append("Err")
            return_data.append("Player does not exist.")
        else:
          return_data.append("Err")
          return_data.append("That player was recently robbed.")
      else:
        return_data.append("Err")
        return_data.append(
          f"Woah! Slow down, you cant rob that fast! Wait {3600 - (round(time.time()) - data[argument1]['rob']['lastRob'])} seconds!")
      print(return_data)
      return return_data
  
  
    @client.request
    def getRobItems(argument1):
      itemsInUse = list(data[argument1]["itemsInUse"].keys())
      return_data = []
      return_data.append(data[argument1]["items"]["ecoins"]["amount"])
      for i in itemsInUse:
        if data[argument1]["itemsInUse"][i]["function"] == "robItem":
          return_data.append(i)
      return return_data
  
  
    @client.request
    def changeJob(argument1, argument2):
      return_data = ""
      if argument2 == "0":
        data[argument1]["job"]["jobNum"] = "0"
        data[argument1]["job"]["streak"] = 0
      if argument2 == "regemployee":
        if not data[argument1]["level"] < 1:
          data[argument1]["job"]["jobNum"] = "1"
          data[argument1]["job"]["streak"] = 0
          return_data = "Successfully joined job."
        else:
          return_data = "Your level is too low for that job."
      if argument2 == "director":
        if not data[argument1]["level"] < 3:
          data[argument1]["job"]["jobNum"] = "2"
          data[argument1]["job"]["streak"] = 0
          return_data = "Successfully joined job."
        else:
          return_data = "Your level is too low for that job."
      if argument2 == "ceo":
        if not data[argument1]["level"] < 6:
          data[argument1]["job"]["jobNum"] = "3"
          data[argument1]["job"]["streak"] = 0
          return_data = "Successfully joined job."
        else:
          return_data = "Your level is too low for that job."
      return return_data
  
  
    @client.request
    def beg(argument1):
      inUse = list(data[argument1]['itemsInUse'].keys())
      if 'fidgetspinner' in inUse:
        gr = 1
        mul = 2
      else:
        gr = 3
        mul = 1
        
      if round(time.time()) - data[argument1]["lastBeg"] > 30:
        data[argument1]["lastBeg"] = time.time()
        if random.randint(1, 4) > gr:
          ecoins = (random.randint(1000, 5000)) * mul
          return_data = f"Here, take a free {ecoins} coins!"
          data[argument1]["items"]["ecoins"]["amount"] = data[argument1]["items"]["ecoins"]["amount"] + ecoins
        else:
          return_data = "You got no money. Better luck next time."
        return return_data
      else:
        return f"Woah! You cant beg that fast, people will be suspicious! Wait {30 - (round(time.time()) - data[argument1]['lastBeg'])} seconds!"
  
  
    @client.request
    def shoplist():
      itemNames = list(shop.keys())
      return_data = []
      for i in itemNames:
        return_data.append(f"{i}:")
        return_data.append(f"| Buy price: {shop[i]['buyPrice']}")
        return_data.append(f"| Sell price: {shop[i]['sellPrice']}")
        return_data.append(f"| Usable: {shop[i]['useable']}")
        if shop[i]["useable"] == "True":
          return_data.append(f"| Item use time: {shop[i]['expireTime']}")
        return_data.append(f"| Description: {shop[i]['description']}")
      return return_data
  
  
    @client.request
    def buy(argument1, argument2):
      req = argument2.split(".")
      name = req[0]
      num = int(req[1])
      inventory = data[argument1]["items"]
      itemNames = list(shop.keys())
      inventoryNames = list(inventory.keys())
      if name in itemNames:
        if shop[name]["buyPrice"] != 'not buyable':
          if not data[argument1]["items"]["ecoins"]["amount"] < shop[name]["buyPrice"] * num:
            if not name in inventoryNames:
              inventory[name] = {}
              inventory[name]["amount"] = 0
              inventory[name]["useable"] = shop[name]["useable"]
              if shop[name]["useable"] == "True":
                inventory[name]["expireTime"] = shop[name]["expireTime"]
              inventory[name]["function"] = shop[name]["function"]
            if not inventory[name]["amount"] + num > shop[name]["maxNum"]:
              inventory[name]["amount"] = inventory[name]["amount"] + num
              data[argument1]["items"]["ecoins"]["amount"] = data[argument1]["items"]["ecoins"]["amount"] - (shop[name]["buyPrice"] * num)
              data[argument1]["items"] = inventory
              return_data = "Successfully bought item(s)!"
            else:
              return_data = "You already have the max number of this item."
          else:
            return_data = "You don't have enough coins to buy that item!"
        else:
          return_data = "This item is not buyable."
      else:
        return_data = "That item doesn't exist! Type 'pls shop list' to see a list of available items."
      return return_data
  
  
    @client.request
    def profile(argument1):
      def getJobName(num):
        if num == '-1':
          return 'Dev'
        if num == '0':
          return 'no job'
        if num == '1':
          return 'regular employee'
        if num == '2':
          return 'director'
        if num == '3':
          return 'ceo'
  
      argument1 = str(argument1)
      try:
        return_data = []
        trophies = []
        inven = data[argument1]["items"]
        invenNames = list(inven.keys())
        return_data.append("| Player profile: ")
        return_data.append(f"| Username: {data[argument1]['username']} | Level: {data[argument1]['level']}")
        return_data.append(f"| Job: {getJobName(data[argument1]['job']['jobNum'])}")
        return_data.append(f"| Ecoins earned: {data[argument1]['items']['ecoins']['amount']}")
        return_data.append("| -------------------------")
        return_data.append("| Player inventory: ")
        for i in invenNames:
          if i != 'ecoins':
            if inven[i]['amount'] != 0:
              return_data.append(f"| {i} | x{inven[i]['amount']}")
              if inven[i]['function'] == 'event':
                trophies.append(f"| {i} | Description: {shop[i]['description']}")
        return_data.append("| -------------------------")
        return_data.append("| Player bank: ")
        return_data.append(f"| Bank space: {data[argument1]['bank']['bankSpace']} spaces")
        return_data.append(
          f"| Bank space remaining: {data[argument1]['bank']['bankSpace'] - data[argument1]['bank']['bankCoins']} spaces")
        return_data.append(f"| Coins in bank: {data[argument1]['bank']['bankCoins']} coins")
        return_data.append("| -------------------------")
        return_data.append("| Trophies: ")
        for i in trophies:
          return_data.append(i)
  
      except Exception:
        return_data = "Could not fetch data."
      return return_data
  
  
    @client.request
    def sell(argument1, argument2):
      req = argument2.split(".")
      name = req[0]
      num = int(req[1])
      itemNames = list(shop.keys())
      if name in itemNames:
        if shop[name]["sellPrice"] != "not sellable":
          inventory = data[argument1]["items"]
          inventoryNames = list(inventory.keys())
          if name in inventoryNames:
            if not inventory[name]["amount"] - num < 0:
              data[argument1]["items"]["ecoins"]["amount"] = data[argument1]["items"]["ecoins"]["amount"] + float(shop[name]["sellPrice"] * num)
              inventory[name]["amount"] = inventory[name]["amount"] - num
              data[argument1]["items"] = inventory
              return_data = "Successfully sold item."
            else:
              return_data = "You don't own that many of that item."
          else:
            return_data = "You don't own that item."
        else:
          return_data = "Item is not sellable."
      else:
        return_data = "Item does not exist!"
      return return_data
  
  
    @client.request
    def daily(argument1):
      if round(time.time()) - data[argument1]["daily"]["lastDaily"] > 86400:
        if round(time.time()) - data[argument1]["daily"]["lastDaily"] > 172800:
          data[argument1]["daily"]["streak"] = 0
        coins = 5000 + (500 * data[argument1]["daily"]["streak"])
        data[argument1]["items"]["ecoins"]["amount"] = data[argument1]["items"]["ecoins"]["amount"] + coins
        data[argument1]["daily"]["streak"] = data[argument1]["daily"]["streak"] + 1
        data[argument1]["daily"]["lastDaily"] = time.time()
        return_data = f"Daily coins: {coins} coins were placed in your wallet!"
      else:
        return_data = f"You have to wait {86400 - (round(time.time()) - data[argument1]['daily']['lastDaily'])} seconds for your next daily reward!"
      return return_data
  
  
    @client.request
    def deposit(argument1, argument2):
      argument2 = float(argument2)
      if not data[argument1]["bank"]["bankCoins"] + argument2 > data[argument1]["bank"]["bankSpace"]:
        if not data[argument1]["items"]["ecoins"]["amount"] - argument2 < 0:
          data[argument1]["bank"]["bankCoins"] = data[argument1]["bank"]["bankCoins"] + argument2
          data[argument1]["items"]["ecoins"]["amount"] = data[argument1]["items"]["ecoins"]["amount"] - argument2
          return_data = f"Successfully deposited {argument2} coins into your bank!"
        else:
          return_data = "You don't have that much money in your wallet! Failed to deposit."
      else:
        return_data = "You don't have that much space in your bank! Failed to deposit."
      return return_data
  
  
    @client.request
    def withdraw(argument1, argument2):
      argument2 = int(argument2)
      if not data[argument1]["bank"]["bankCoins"] - argument2 < 0:
        data[argument1]["bank"]["bankCoins"] = data[argument1]["bank"]["bankCoins"] - argument2
        data[argument1]["items"]["ecoins"]["amount"] = data[argument1]["items"]["ecoins"]["amount"] + argument2
        return_data = f"Successfully withdrew {argument2} coins from your bank!"
      else:
        return_data = "You don't have that many coins in your bank! Failed to withdraw."
      return return_data
  
  
    @client.request
    def gamble(argument1, argument2):
      inUse = list(data[argument1]['itemsInUse'].keys())
      if 'fidgetspinner' in inUse:
        myTop = 25
      else:
        myTop = 12
        
      argument2 = float(argument2)
      print(data[argument1]["items"]["ecoins"]["amount"])
      if not data[argument1]["items"]["ecoins"]["amount"] - argument2 < 0:
        return_data = []
        botGamble = random.randint(1500, argument2)
        botRoll = random.randint(1, 15)
        myRoll = random.randint(1, myTop)
        return_data.append(f"| Your roll: {myRoll}")
        return_data.append(f"| Bot roll: {botRoll}")
        return_data.append("| -------------------------")
        if botRoll > myRoll:
          return_data.append(f"| You lost {argument2} coins!")
          data[argument1]["items"]["ecoins"]["amount"] = data[argument1]["items"]["ecoins"]["amount"] - argument2
        elif botRoll < myRoll:
          return_data.append(f"| You won {botGamble} coins!")
          data[argument1]["items"]["ecoins"]["amount"] = data[argument1]["items"]["ecoins"]["amount"] + botGamble
        else:
          return_data.append(f"| It was a tie!")
      else:
        return_data = "invalidGambleValue"
      return return_data
  
  
    @client.request
    def lottery(argument1, argument2):
      argument2 = float(argument2)
      inven = data[argument1]["items"]
      invenNames = list(inven.keys())
      if "lotteryticket" in invenNames:
        if not inven["lotteryticket"]["amount"] - argument2 < 0:
          inven["lotteryticket"]["amount"] = inven["lotteryticket"]["amount"] - argument2
          lotteryList = fullData["gameData"]["lottery"]["lotteryList"]
          i = 0
          while i != argument2:
            lotteryList.append(argument1)
            i += 1
          fullData["gameData"]["lottery"]["lotteryList"] = lotteryList
          fullData["gameData"]["lottery"]["lotteryAmount"] = fullData["gameData"]["lottery"]["lotteryAmount"] + (10000 * argument2)
          return_data = f"Successfully entered lottery {argument2} times!"
        else:
          return_data = "You don't have that many lottery tickets."
      else:
        return_data = "You don't have that many lottery tickets."
      return return_data

    @client.request
    def inuse(argument1):
      useItems = list(data[argument1]["itemsInUse"].keys())
      return_data = []
      return_data.append("Items in use:")
      if len(useItems) != 0:
        for i in useItems:
          return_data.append(f"| {i} | Time left: {data[argument1]['itemsInUse'][i]['expireTime']-(round(time.time()) - data[argument1]['itemsInUse'][i]['useTime'])} seconds")
      else:
        return_data.append("| No items in use.")

      return return_data
  
    @client.request
    def work(argument1):
      try:
        data[argument1]
      except Exception:
        return "Error."
      return_data = []
      if data[argument1]["job"]["jobNum"] != "0":
        if round(time.time()) - data[argument1]["job"]["lastWork"] > 3600:
          if round(time.time()) - data[argument1]["job"]["lastWork"] > 7200:
            data[argument1]["job"]["streak"] = 0
          return_data.append(data[argument1]["job"]["jobNum"])
          return_data.append(data[argument1]["job"]["streak"])
          inUse = list(data[argument1]['itemsInUse'].keys())
          if 'suit' in inUse:
            return_data.append(2)
          else:
            return_data.append(1)
          data[argument1]["job"]["lastWork"] = time.time()
          print(data[argument1]["job"]["lastWork"])
          print(time.time())
        else:
          return_data.append("Err")
          return_data.append(
            f"You need to wait {3600 - (round(time.time()) - data[argument1]['job']['lastWork'])} seconds before you can work again!")
      else:
        return_data.append("Err")
        return_data.append("You dont have a job! Type 'pls work list' to see available jobs.")
      return return_data
  
  
    @client.request
    def loadInbox(argument1):
      inbox = data[argument1]["inbox"]
      print(inbox)
      return_data = []
      i = 0
      if len(inbox) != 0:
        while i != len(inbox):
          return_data.append(inbox[i])
          i += 3
      else:
        return_data.append('Nothing in inbox.')
      return return_data
  
  
    def tick():
      while True:
        users = list(data.keys())
        # Check all users -
        for i in users:
          # Bank intrest -
          days = round((round(time.time()) - data[i]["bank"]["bankIntrestTime"]) // 86400)
          if not days < 1:
            if data[i]['bank']['bankCoins'] < 50000:
              ecoins = (data[i]["bank"]["bankCoins"] * 0.1) * days
              data[i]["items"]["ecoins"]["amount"] += ecoins
              data[i]["bank"]["bankIntrestTime"] = time.time()
  
              if ecoins != 0:
                inbox = data[i]["inbox"]
                inbox.append(f"Bank: Collected {ecoins} from bank intrest!")
                inbox.append(time.time())
                inbox.append(86400)
                data[i]["inbox"] = inbox

            else:
              ecoins = (data[i]["bank"]["bankCoins"] * 0.1) * days
              data[i]["bank"]["bankIntrestTime"] = time.time()
              if ecoins != 0:
                inbox = data[i]["inbox"]
                inbox.append(f"Bank: Could not supply interest, more than 50000 coins in bank!")
                inbox.append(time.time())
                inbox.append(86400)
                data[i]["inbox"] = inbox
  
          # Mange inbox -
          ii = 0
          try:
            inbox = data[i]["inbox"]
            if len(inbox) != 0:
              while ii != len(inbox):
                if round(time.time()) - inbox[ii + 1] > inbox[ii + 2]:
                  inbox.pop(ii)
                  inbox.pop(ii)
                  inbox.pop(ii)
                  ii -= 3
                ii += 3
          except Exception as e:
            raise(e)
  
          data[i]["inbox"] = inbox
  
          # Manage used items -
          useItems = list(data[i]["itemsInUse"].keys())
          for j in useItems:
            if round(time.time()) - data[i]["itemsInUse"][j]['useTime'] > data[i]["itemsInUse"][j]['expireTime']:
              data[i]["itemsInUse"].pop(j, None)
  
          # Manage trades -
          if data[i]['trade']['canTrade'] == "False":
            if round(time.time()) - data[i]['trade']['lastTrade'] > 300:
              data[i]['trade']['canTrade'] = "True"
              data[i]['trade']['lastTrade'] = 0
  
        # lottery
        if round(time.time()) - fullData["gameData"]["lottery"]["lastLottery"] > 3600:
          lotteryList = fullData["gameData"]["lottery"]["lotteryList"]
          if len(lotteryList) != 0:
            luckyWinner = lotteryList[random.randint(0, len(lotteryList) - 1)]
            print(f"Lottery: {luckyWinner}")
            data[luckyWinner]["items"]["ecoins"]["amount"] = data[luckyWinner]["items"]["ecoins"]["amount"] + fullData["gameData"]["lottery"][
              "lotteryAmount"]
            inbox = data[luckyWinner]["inbox"]
            inbox.append(
              f"Lottery: YOU WON THE LOTTERY!! {fullData['gameData']['lottery']['lotteryAmount']} ecoins were placed in your wallet!")
            inbox.append(time.time())
            inbox.append(86400)
            data[luckyWinner]["inbox"] = inbox
          fullData["gameData"]["lottery"]["lotteryList"] = []
          fullData["gameData"]["lottery"]["lotteryAmount"] = 0
          fullData["gameData"]["lottery"]["lastLottery"] = time.time()
  
  
    threads = [
      Thread(target=tick, args=()),
      Thread(target=savenload)
    ]
  
    for thread in threads:
      try:
        thread.start()
      except Exception:
        thread.start()

    try:
      client.run()
    except Exception:
      client.run()

except Exception:
  while True:
    encoded = db['fullData']
    fullData = jsonpickle.decode(encoded)
    data = fullData["data"]
    while True:
      main()

try:
  encoded = db['fullData']
  fullData = jsonpickle.decode(encoded)
  data = fullData["data"]
  while True:
    main()
except Exception as e:
  encoded = db['fullData']
  fullData = jsonpickle.decode(encoded)
  data = fullData["data"]
  while True:
    main()
