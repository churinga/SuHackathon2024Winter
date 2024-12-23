import Engine.Engine as Engine
import Player.PlayerStrategy as PlayerStrategy

# main tournament program
def main():
    engine = Engine.Engine()
    engine.set_strategy_obj(PlayerStrategy.PlayerStrategy())
    engine.display_banner()
    engine.run()

main()