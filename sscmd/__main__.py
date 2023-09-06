from sscmd import  __appname__
from .cli import app

def cli_main():
    app(prog_name = __appname__)

if __name__ == "__main__":
    cli_main()
