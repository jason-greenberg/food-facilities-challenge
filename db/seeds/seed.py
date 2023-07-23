import typer
from db.db_setup import get_db
from db.seeds.users import seed_users, undo_users

app = typer.Typer()

@app.command()
def seed():
    with get_db() as db:
        with db.begin():
            seed_users(db)
            db.commit()

@app.command()
def undo():
    with get_db() as db:
        with db.begin():
            undo_users(db)
            db.commit()

if __name__ == "__main__":
    app()
