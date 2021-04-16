import asyncio
#from kingdomRoyale import KingdomRoyale

async def cancelableSleep (time : int, cond : asyncio.Condition, game):
    
    await cond.acquire()
    try:
        await asyncio.wait_for(cond.wait(), timeout=time - 10)
    except asyncio.TimeoutError:
        await asyncio.sleep(10)
    except asyncio.CancelledError:
        for i in game.secretMeetings:
            i.task.cancel()
        game.taskTurn.cancel()
    finally:
        cond.release()
