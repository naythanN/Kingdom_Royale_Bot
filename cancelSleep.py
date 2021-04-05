import asyncio

async def cancelableSleep (time : int, cond : asyncio.Condition):
    
    await cond.acquire()
    print(f"espera {time} segundos ou skip")
    try:
        await asyncio.wait_for(cond.wait(), timeout=time)
        print("de fato skippou")
    except:
        print(f"passou {time} segundos")
    finally:
        cond.release()
        print("weee")
