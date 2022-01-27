from base.core import Game


def main():
    sizes = (width, height) = (960, 720)
    game = Game(sizes, 120)
    game.run()


if __name__ == "__main__":
    main()
