import typer

from db.db_setup import SessionLocal

from db.seeds.users import seed_users, undo_users
from db.seeds.permits import seed_permits, undo_permits

app = typer.Typer()

@app.command()
def seed():
    db = SessionLocal()
    try:
        seed_users(db)
        seed_permits(db)
        db.commit()
    finally:
        db.close()

@app.command()
def undo():
    db = SessionLocal()
    try:
        undo_users(db)
        undo_permits(db)
        db.commit()
    finally:
        db.close()


if __name__ == "__main__":
    app()
