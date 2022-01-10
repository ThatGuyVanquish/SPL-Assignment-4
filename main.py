from parser import parse
from persistence import _Repository
import sys
import atexit

repo = _Repository()
atexit.register(repo._close)

def __main__():
    parse(sys.args[0], sys.args[1], sys.args[2])
    
if __name__ == __main__:
    __main__()