import os
import environ

from pathlib import Path

env = environ.Env(
    DEBUG=(bool, False)
)

# This is to read the .env file at the root of the directory
BASE_DIR = Path(__file__).resolve().parent.parent; # parent parent is ugly why python why!
environ.Env.read_env(os.path.join(BASE_DIR, '.env'));
