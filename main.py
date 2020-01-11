from mazegen import mazegen

def main():
    print("Instantiating MazeGen object...")
    maze_gen = mazegen.mazegen()
    maze_gen.generate(32, True)
    return

if __name__ == '__main__':
    main()
