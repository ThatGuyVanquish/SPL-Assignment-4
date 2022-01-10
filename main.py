from parser import parse
from persistence import _Repository
import sys
import atexit

repo = _Repository(sys.argv[4])
atexit.register(repo._close)

def __main__():
    parse(sys.argv[1], sys.argv[2], sys.argv[3])
    
if __name__ == __main__:
    __main__()