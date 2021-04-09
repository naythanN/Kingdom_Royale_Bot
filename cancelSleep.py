import asyncio
#from kingdomRoyale import KingdomRoyale

async def cancelableSleep (time : int, cond : asyncio.Condition, game):
    
    await cond.acquire()
    print(f"espera {time} segundos ou skip")
    try:
        await asyncio.wait_for(cond.wait(), timeout=time - 10)
        print("de fato skippou")
    except asyncio.TimeoutError:
        await game.bigRoomC.send("10 seconds to end")
        await asyncio.sleep(10)
        print(f"passou {time} segundos")
    except asyncio.CancelledError:
        print("hmmmm")
        for i in game.secretMeetings:
            print("hmmmmmmmmm")
            i.task.cancel()
        game.taskTurn.cancel()
    finally:
        cond.release()
        print("weee")
