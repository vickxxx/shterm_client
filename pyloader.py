from Scripts.Loader import utils, loader
import os, sys


def main():
    print("hello")
    print(sys.argv)
    url_terminal = sys.argv[1]
    print(url_terminal)
    shterm_data = utils.get_json_from_shterm_url(url_terminal)
    print(shterm_data)
    resources_dir = os.getcwd()

    loader.get_loader(shterm_data, resources_dir).load()


if __name__ == "__main__":
    main()