from app import Game
import asyncio

print("1. Importations terminées")


async def start_game():
    print("2. Démarrage de start_game")
    app = Game()
    print("3. Objet Game créé, lancement de run...")
    await app.Run()

if __name__ == "__main__":
    print("0. Script lancé")
    asyncio.run(start_game())
