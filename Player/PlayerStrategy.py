from Engine.Strategy import Strategy

class PlayerStrategy(Strategy):
    def __init__(self):
        super().__init__()

    def decision(
            self,
            seq: int,
            jetfighter_info: dict,
            propfighter_info: dict,
            obstacle_info: dict,
            bullet_info: list
    ):
        return Strategy.NOOP
