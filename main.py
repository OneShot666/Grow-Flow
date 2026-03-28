from app import Game
import asyncio


async def start_game():
    app = Game()
    await app.Run()

if __name__ == "__main__":
    asyncio.run(start_game())

quit()
