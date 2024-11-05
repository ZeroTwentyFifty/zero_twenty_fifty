    

<h3  align="center">ZeroTwentyFifty</h3>


![ClimateTech](https://img.shields.io/badge/Topic-ClimateTech-brightgreen) ![Sustainability](https://img.shields.io/badge/Topic-Sustainability-yellow) ![Uptime](https://img.shields.io/badge/Uptime-up%25-brightgreen) ![CarbonFootprinting](https://img.shields.io/badge/Topic-CarbonFootprinting-ff69b4) ![Pricing](https://img.shields.io/badge/Pricing-Free-brightgreen) 
![Help Wanted](https://img.shields.io/badge/Help%20Wanted-Contribute-blue)  ![GitHub stars](https://img.shields.io/github/stars/ZeroTwentyFifty/zero_twenty_fifty?style=social)  [![Pact Conformant](https://img.shields.io/badge/Pact-Conformant-brightgreen)](https://github.com/ZeroTwentyFifty/zero_twenty_fifty/blob/master/assets/PACT%20conformant%20Badge.png)

  

# About


ZeroTwentyFifty’s repository represents a [PACT Conformant ](https://www.zerotwentyfifty.com/blog/zerotwentyfifty-is-listed-as-a-pact-conformant-solution-by-wbcsd-pact) implementation of the [WBCSD Partnership for Carbon Transparency (PACT) Pathfinder Protocol](https://www.carbon-transparency.org/). 
As a software company dedicated to combating climate change, we build solutions for sharing Scope 3 Product Carbon footprint data. 

This project is part of our commitment to providing open-source implementations of critical pathway software, enabling organizations of all sizes to collaborate effectively in their sustainability efforts.


# Getting Started

> ⚠️ **Caution:** While every effort has been made to keep the codebase in a "green" state, being an early-stage software project means some components may be unstable. Please note that if you check out the current head, things may be broken. Tagged versions will be maintained in working order.

## 1. Install Dependencies

From the root of the repository, run:

```bash
poetry install
```
### 2. Install Uvicorn

For Ubuntu, install Uvicorn with:
```bash
sudo apt install uvicorn
```
### 3. Activate Poetry Shell

Activate the Poetry environment to access the installed Python dependencies:
```bash
poetry shell
```
### 4. Launch the Development Server

Start the local development server with:
```bash
uvicorn main:app
```
### 5. Verify the Launch

Open your browser and navigate to:

[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

To obtain an authentication token, go to the **POST /auth/token** route and enter a valid username and password in the `client_id` and `client_secret` fields. This should return an auth token and confirm that everything is working correctly.

## Create Local PostgreSQL Instance

### 1. Connect to PostgreSQL

Connect to your local PostgreSQL instance:
```
psql -d postgres
```
### 2. Create the Database

Create a database called `ztf`:
```
CREATE DATABASE ztf;
```
### 3. Verify Configuration

Ensure that the values in `core/config.py` are set correctly for your local development environment:


POSTGRES_USER: str = os.getenv("PGUSER", "username")<br> POSTGRES_PASSWORD = os.getenv("PGPASSWORD", "password")<br> POSTGRES_SERVER: str = os.getenv("PGHOST", "localhost")<br> POSTGRES_PORT: str = os.getenv("PGPORT", 5432) # default PostgreSQL port is 5432<br> POSTGRES_DB: str = os.getenv("PGDATABASE", "ztf")


### 4. Provision Database Tables

Run the following command within the Poetry shell to provision the database with tables:
```
uvicorn main:app
```
If successful, you should see the database tables inside the `ztf` database by executing:
```
\dt
```

## Setup for Local Testing

### 1. Create `pytest.ini`

Create a file named `pytest.ini` modeled after the `env.template` file. Note that this may be handled by dotenv.

### 2. Run Conformance Tests

By default, conformance tests are excluded from the default pytest run and executed in a separate CI/CD pipeline. To run the conformance tests, use:
```
pytest -m conformance
```

## Contact us
If you need help with the software, have questions or queries, or would like to more directly engage ZeroTwentyFifty in work, please reach out to us at:
[louis@zerotwentyfifty.com](mailto:louis@zerotwentyfifty.com)

## Author 
This project was created and is maintained by [Louis W](https://github.com/JohnVonNeumann). If you have any questions or suggestions, feel free to reach out or open an issue on this repository.

## License 
This project is licensed under the MIT License, meaning you are free to use, modify, and distribute this software under the terms of the MIT License.

## Acknowledgements
Thanks to these wonderful people for contributing:

[Chinwoke Anugwara](https://github.com/Chinwoke-C)



