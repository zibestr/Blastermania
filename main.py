from base.core import Game


def main():
    sizes = (width, height) = (900, 700)
    game = Game(sizes, 120)
    game.run()


if __name__ == "__main__":
    main()
