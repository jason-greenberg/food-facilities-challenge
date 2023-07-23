import typer

from db.db_setup import SessionLocal

from db.db_setup import get_db
from db.seeds.users import seed_users, undo_users

app = typer.Typer()

@app.command()
def seed():
    db = SessionLocal()
    try:
        seed_users(db)
        db.commit()
    finally:
        db.close()

@app.command()
def undo():
    db = SessionLocal()
    try:
        undo_users(db)
        db.commit()
    finally:
        db.close()


if __name__ == "__main__":
    app()
