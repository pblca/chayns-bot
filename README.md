# Chayns
A discord bot

## Setup
- Create a new `.env` file at root from `sample.env`
- Add your own environment variables to this new file
- run `docker-compose up` for required services
- create a `chayns` db in the psql instance
- run `pip install -r requirements.txt`
- run `alembic upgrade head`
- run `python main.py`

## Migrations
To create a new migration (from root)  
`alembic revision --autogenerage -m "Describe your change here`

To update your db to the current migrations  
`alembic upgrade head`