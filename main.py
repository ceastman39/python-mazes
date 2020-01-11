from mazegen import MazeGenerator

def main():
    print("Instantiating MazeGen object...")
    maze_gen = MazeGenerator.MazeGenerator()
    maze_gen.generate(32, 32, True)
    return

if __name__ == '__main__':
    main()
