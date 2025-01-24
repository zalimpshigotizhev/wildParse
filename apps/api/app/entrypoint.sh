alembic revision --autogenerate -m "First migrations"
alembic upgrade head
python main.py