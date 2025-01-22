import pandas
import sqlite3
import yaml
import sys


DEBUPE_CONFIG = {}


def load_config():
    with open('config.yml', 'r') as file:
        config = yaml.safe_load(file)

    with open('sort_config.yml','r') as file:
        sort_config = yaml.safe_load(file)

    # Read from a configuration files
    # List of files that should be searched for.
    # - images
    # - videos
    # - everything
    # Priority of properties
    # Auto-Delete = False
    # Backend/Output
    # Graphical Prompt, etc
    return(config.update(sort_config))


def parse_args(args, default_config=config):
    # Modifications to the initial configuration.
    DEDUPE_CONFIG = config


def init_db():

    pass


def operation():
    pass


def dedupe(config):
    db_conn = init_db()
    output = operation()
    print(output)


if __name__ == '__main__':
    parse_args(sys.argv, load_config())
    base_directory = sys.argv[1]
    dedupe(DEDUPE_CONFIG, base_directory)
