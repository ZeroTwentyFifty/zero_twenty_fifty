# ZeroTwentyFifty

This repository and application represents [ZeroTwentyFifty](https://zerotwentyfifty.com)'s implementation
of the [WBCSD](https://www.wbcsd.org/) [Partnership For Carbon Transparency (PACT)](https://www.carbon-transparency.com/) [Pathfinder Protocol](https://wbcsd.github.io/data-exchange-protocol/v2).

It is part of our commitment to the fight against climate change, to bring Open Source implementations of critical
pathway software, so that organisations of all sizes can move together as one.

If you need help with the software, have questions or queries, or would like to more directly engage ZeroTwentyFifty in work, please reach out to us:
`louis@zerotwentyfifty.com`


## Development

### Setting up locally

### Getting setup for the first time on a new setup/host
You're gonna have to make sure that first you've got the deps installed, so from the root of the repo:

    poetry install


After this, install uvicorn, on Ubuntu this is with:

    sudo apt install uvicorn

Now you'll have to activate the shell to  have access to your poetry installed python deps:

    poetry shell

Finally, you can run this to access a local dev environment:

uvicorn main:app

You can verify that the thing has launched correctly by going to:

    http://127.0.0.1:8000/docs

Now that you're there, you can get an auth token by going down to the:

    POST /auth/token route and inserting a valid username and password in the client_id and client_secret fields

Executing that should give you an auth token and validate that things are absolutely working correctly.


#### Create local Postgres instance

Connect to your pg local instance

    psql -d postgres

Create a database called ztf

    CREATE DATABASE ztf;

Make sure that values in `core/config.py` are valid for the local dev env setup:

    ```python
    POSTGRES_USER: str = os.getenv("PGUSER", "username")
    POSTGRES_PASSWORD = os.getenv("PGPASSWORD", "password")
    POSTGRES_SERVER: str = os.getenv("PGHOST", "localhost")
    POSTGRES_PORT: str = os.getenv(
        "PGPORT", 5432
    )  # default postgres port is 5432
    POSTGRES_DB: str = os.getenv("PGDATABASE", "ztf")
    ```

Finally, in order to have the database provision with tables, run (within a `poetry shell`):

    uvicorn main:app

If all went well, you should be able to see the database tables inside the `ztf` database with:

    \dt


#### Setup for local testing

Create a file called `pytest.ini`, and model it off the `env.template` file. There's a chance this may be handled for
you by `dotenv`, but probably not.
