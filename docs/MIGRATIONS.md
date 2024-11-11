# Integrating Database Migrations with Railway's CLI Tool

Here's how you can integrate database migrations with Railway's CLI tool. I'll provide the key steps and concepts, as the exact commands might slightly vary based on your project setup.

## Assumptions

- You have your Alembic project structure set up (`alembic.ini`, migrations directory, etc.).
- You have a `migrate.py` script as outlined previously.

## Steps

1. **Install the Railway CLI:** Follow Railway's documentation on installing their CLI tool.

2. **Authenticate the CLI:**
   - Run `railway login` and follow the prompts to authenticate with your Railway account.

3. **Link Project:**
   - From your project's directory, run `railway link` to link the current project to the CLI.

4. **Custom Migration Commands:**
   - **Local Migrations:**
     `DATABASE_URL=postgresql://postgres:postgres@localhost:5432/postgres python migrate.py`
      This targets the locally deployed Docker hosted pg instance running.
   - **Dev Migrations:**  
     `railway run --environment development python migrate.py`  
     This targets your development environment and executes the migration script.
   - **Production Migrations:**  
     `railway run --environment production python migrate.py`  
     This targets your production environment.

## Additional Notes

- **Environment Variables:** Railway manages environment variables. Ensure your `migrate.py` script can access the correct database connection strings based on the `--environment` flag.
- **Deployment Integration:** Explore if Railway allows setting up these `railway run ...` commands as part of your automated deployment process after code updates.
- **Railway Specifics:** The Railway CLI might have more specialized features for database migrations. Consult their in-depth documentation.

## Example Usage

1. Make changes to your SQLAlchemy models.
2. Generate a new migration:  
   `alembic revision --autogenerate -m "description"`
3. Apply to development:  
   `railway run --environment development python migrate.py`
4. Test changes thoroughly in the development environment.
5. Apply to production:  
   `railway run --environment production python migrate.py`

**Important:** Always test migrations in a staging environment that mirrors production before applying them to your production database.


## Resetting the database entirely in the early stages

Pre beta/having the database models more solidified/normalised, it's probably not a terrible idea to simply wipe the database and start off fresh instead of having migrations that are all over the place. In this case:

1. **Purge the database**: This will involve dropping whatever data is in there.
2. **Downgrade the database to base**: `railway run alembic downgrade base`
3. **Make sure the database is where you need it**: Just go and eyesight check it via railway. Or, use the local database to test.
4. **Delete all of the files in versions**: Go into `alembic/versions` and delete the migration files.
5. **Remove the Enums from the database manually**: For some reason, they don't get removed by the downgrade base, so you've got to remove them by hand, use the script below.
6. **Regenerate the migration**: `railway run alembic revision --autogenerate -m "initialise base database structure"`
7. **Apply the migration**: `railway run --environment dev python migrate.py`

**Script for removing enums**:
```sql
DROP TYPE productfootprintstatus;
DROP TYPE declaredunit;
DROP TYPE characterizationfactors;
DROP TYPE regionorsubregion;
DROP TYPE biogenicaccountingmethodology;
DROP TYPE productorsectorspecificruleoperator;
DROP TYPE crosssectoralstandard;
```

**For local development environment:**
```
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/postgres alembic downgrade base
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/postgres alembic revision --autogenerate -m "initialise base database structure"
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/postgres python migrate.py
```

