from alembic.config import Config
from alembic import command


alembic_cfg = Config("alembic.ini")


def main():
    command.upgrade(alembic_cfg, "head")


if __name__ == "__main__":
    main()
