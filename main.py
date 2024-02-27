import pandas as pd
import asyncio
from samwise_bot import SamwiseBot
from frodo_bot import FrodoBot

async def main():
    dialog = pd.read_csv("lotr_scripts.csv", usecols=["char", "dialog"])
    await asyncio.gather(
        sb = SamwiseBot(dialog),
        fb = FrodoBot(dialog) 
    )



asyncio.run(main())