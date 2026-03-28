from pprint import pprint

from src.db.connection import test_connection

def main() -> None:
    result = test_connection()
    pprint(result)


if __name__ == "__main__":
    main()
