import sys

from parser import parse

def main():
    parse(sys.argv[1], sys.argv[2], sys.argv[3])
    
if __name__ == "__main__":
    main()