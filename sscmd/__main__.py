from sscmd import  __appname__
import .cli

def cli_main():
    cli.app(prog_name = __appname__)

if __name__ == "__main__":
    cli_main()
