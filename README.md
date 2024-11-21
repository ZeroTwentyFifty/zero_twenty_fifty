<p align="center">
  <a href="https://www.zerotwentyfifty.com/solutions/zerotwentyfifty">
   <img src="https://github.com/user-attachments/assets/3cc843f2-9dff-4dde-a06b-0218a577f207" alt="branding">
  </a>

  <h3 align="center">ZeroTwentyFifty Corporation</h3>

  <p align="center">
    Enabling the exchange of product-level carbon accounting data.
    <br />
    <a href="https://www.zerotwentyfifty.com"><strong>Learn more »</strong></a>
    <br />
    <br />
    <a href="https://github.com/orgs/ZeroTwentyFifty/discussions">Discussions</a>
    ·
    <a href="https://www.zerotwentyfifty.com/blog">Blog</a>
    ·
    <a href="https://www.zerotwentyfifty.com/solutions">Solutions</a>
    ·
    <a href="https://www.zerotwentyfifty.com/services">Services</a>
    ·
    <a href="https://mailchi.mp/zerotwentyfifty.com/newsletter">Newsletter</a>
  </p>

</p>

<p align="center">
    <a href="https://github.com/ZeroTwentyFifty/zero_twenty_fifty/actions"><img src="https://img.shields.io/badge/coverage-pytest--cov-red.svg"></a>
    <a href="https://img.shields.io/badge/license-MIT-blue.svg"><img src="https://img.shields.io/badge/license-MIT-blue.svg" alt="license"></a>
    <a href="https://github.com/ZeroTwentyFifty/zero_twenty_fifty/stargazers"><img src="https://img.shields.io/github/stars/ZeroTwentyFifty/zero_twenty_fifty" alt="Github Stars"></a>
    <a href="https://img.shields.io/github/workflows/status/ZeroTwentyFifty/zero_twenty_fifty/master"><img src="https://github.com/ZeroTwentyFifty/zero_twenty_fifty/actions/workflows/app.yml/badge.svg"></a>
    <!--<a href="https://readthedocs.org/projects/pathfinder-framework/badge/?version=latest"><img src="https://pathfinder-framework.readthedocs.io/en/latest/?badge=latest"></a>-->
    <img src="https://img.shields.io/badge/Topic-ClimateTech-brightgreen" alt="ClimateTech">
    <img src="https://img.shields.io/badge/Topic-Sustainability-yellow" alt="Sustainability">
    <img src="https://img.shields.io/badge/Topic-CarbonFootprinting-ff69b4" alt="Carbon Footprinting">
    <img src="https://img.shields.io/badge/Pricing-Free-brightgreen" alt="Pricing">
    <img src="https://img.shields.io/badge/Help%20Wanted-Contribute-blue" alt="Help Wanted">
    <a href="https://github.com/ZeroTwentyFifty/zero_twenty_fifty/blob/master/assets/PACT%20conformant%20Badge.png">
        <img src="https://img.shields.io/badge/PACT-Conformant-brightgreen" alt="PACT Conformant">
    </a>
</p>



<div align="center"> <a href="https://github.com/ZeroTwentyFifty/zero_twenty_fifty/blob/master/assets/PACT%20conformant%20Badge.png"> <img src="https://drive.google.com/file/d/1SiTeNyQ_AIzwG2o8-hlL4wHk-55DZoYj/view?usp=sharing" alt="PACT conformant badge" width="80" height="80"> </a> </div>

  
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


## Acknowledgements
Thanks to these wonderful people for contributing:

[Chinwoke Anugwara](https://github.com/Chinwoke-C)



