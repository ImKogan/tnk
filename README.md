# tnk
Scraping JPS English Bible, processing text, extracting name (etc)
and storing them in a database.

## Data
Downloaded html is stored in JPS directory by default. The name
can be changed in `config.json` in the key `local_jps_html`.

## Configuration
`config.json` define the file names and locations created throughout the
workflow.

Create a file `db_config.json` to define how the database is accessed:

    {
        "db_type": "postgresql",
        "db_user": "user",
        "db_pwd": "123",
        "db_port": "localhost",
        "db_name": "mydatabase"
    }
