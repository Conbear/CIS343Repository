
import sys

# Check if arguments were passed

def error():
    print("Error")

def main():
    # Your primary code logic goes here

    if len(sys.argv) >= 3:
        print("Error: Too many arguments")
        sys.exit(1)
    elif len(sys.argv)==2:
        with open(sys.argv[1], "r", encoding="utf-8") as file:
            content = file.read()
            print(content)
            print("Error: Scanner not implimented.")

    elif len(sys.argv)==1:
        while True:
            try:
                returning = input(">>>")
                print(returning)
                print("Error: Scanner not implimented.")
            except KeyboardInterrupt:
                break


if __name__ == "__main__":
    main()