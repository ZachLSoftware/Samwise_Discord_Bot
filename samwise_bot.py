import os
import discord
import pandas as pd
import random as rand


from dotenv import load_dotenv

class SamwiseBot():
  stopwords = []
  def __init__(self):
    load_dotenv()
    stopwords = set(['I', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 'your', 'yours', 'yourself', 
                                  'yourselves', 'he', 'him', 'his', 'himself', 'she', 'her', 'hers', 'herself', 'it', 'its', 'itself', 
                                  'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', 
                                  'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 
                                  'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 
                                  'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 
                                  'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 
                                  'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 
                                  'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 
                                  'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', 'should', 'now'])
    sam_dialog = pd.read_csv("lotr_scripts.csv", usecols=["char", "dialog"])
    sam_dialog = sam_dialog[sam_dialog["char"] == "SAM"]
    sam_dialog = sam_dialog.reset_index(drop=True)
    
    
    TOKEN = os.getenv("DISCORD_TOKEN")
    intents = discord.Intents.default()
    intents.message_content=True
    
    client = discord.Client(intents=intents)
    
    @client.event
    async def on_ready():
        print(f'{client.user} has connected to Discord!')
    
    @client.event
    async def on_message(msg):
        content=msg.content
        print(msg.author==client.user)
        if client.user != msg.author:
            
            if "samwise" in content.lower() or "sam" in content.lower() or client.user.mentioned_in(msg):
                context_check = check_keywords(content)
                if context_check == False:
                    index = rand.randint(0,215)
                    response = sam_dialog.loc[index]["dialog"]
                else:
                    response = context_check
                await msg.channel.send(response)
    
    def check_keywords(content):
        keywords = content.split()
        filtered = [word for word in keywords if word.lower() not in stopwords]
        filtered=sorted(filtered, key=len, reverse=True)
        for word in filtered:
            result = sam_dialog[sam_dialog["dialog"].str.contains(word)]
    
            if not result.empty:
                return result.iloc[0]["dialog"]
            else:
                continue
        
        return False
    
    client.run(TOKEN)

sb = SamwiseBot()