from common import Game, Direction, SantaID, GRID_WIDTH, GRID_HEIGHT
from edit_me import handshake, take_turn

class SingleplayerGame(Game):
    def __init__(self):
        super().__init__()
        self.__santa = SantaID("SINGLEPLAYER", handshake())
        self.__direction = None

    def start_server(self):
        pass

    def lock_server(self):
        pass

    def stop_server(self):
        pass

    def get_server_ip(self) -> str:
        return "SINGLEPLAYER"

    def get_santa_ids(self) -> list[SantaID]:
        return [self.__santa]

    def request_santas(self) -> None:
        pass

    def received_santas(self) -> bool:
        return True

    def get_santas(self) -> list[tuple[str, Direction]]:
        game_state = {
            "grid_size": (GRID_WIDTH, GRID_HEIGHT),
            "santas": [self.get_santa_position("SINGLEPLAYER")],
            "gifts": self.get_gifts()
        }
        return [("SINGLEPLAYER", take_turn(game_state))]

def main():
    game = SingleplayerGame()
    game.run()

if __name__ == "__main__":
    main()