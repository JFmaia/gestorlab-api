alembic revision --autogenerate -m ''
alembic upgrade head
python create_utils.py
uvicorn main:app --host 0.0.0.0 --port 8000
