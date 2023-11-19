# uvicorn dota2:app --reload 
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sqlite3

app = FastAPI()

def con_db():
    return sqlite3.connect('2.Dota2.db')


def create_table():
    connection = con_db()
    cursor = connection.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Heroes (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    q TEXT NOT NULL,
    w TEXT NOT NULL,
    e TEXT NOT NULL,
    r TEXT NOT NULL
    )
    ''')
    connection.commit()
    connection.close()


def add_data():
    connection = con_db()
    cursor = connection.cursor()
    cursor.execute('INSERT INTO Heroes(name, q, w, e, r) VALUES ("Riki", "SMOKE SCREEN", "BLINK STRIKE", "TRICKS OF THE TRADE", "CLOAK AND DAGGER")')
    cursor.execute('INSERT INTO Heroes(name, q, w, e, r) VALUES ("Shadow Fiend", "SHADOWRAZE", "SHADOWRAZE", "SHADOWRAZE", "REQUIEM OF SOULS")')
    cursor.execute('INSERT INTO Heroes(name, q, w, e, r) VALUES ("Lina", "DRAGON SLAVE", "LIGHT STRIKE ARRAY", "FLAME CLOAK", "LAGUNA BLADE")')
    cursor.execute('INSERT INTO Heroes(name, q, w, e, r) VALUES ("Crystal Maiden", "CRYSTAL NOVA", "FROSTBITE", "CRYSTAL CLONE", "FREEZING FIELD")')
    cursor.execute('INSERT INTO Heroes(name, q, w, e, r) VALUES ("Meepo", "EARTHBIND", "POOF", "MEGAMEEPO", "MEGAMEEPO FLING")')
    connection.commit()
    connection.close()


def insert_hero(name, q, w, e, r):
    connection = con_db()
    cursor = connection.cursor()
    cursor.execute('INSERT INTO Heroes(name, q, w, e, r) VALUES (?, ?, ?, ?, ?)', (name, q, w, e, r))
    connection.commit()
    connection.close()


def select_all_heroes():
    connection = con_db()
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM Heroes')
    heroes = cursor.fetchall()
    connection.close()
    return heroes


def select_hero_by_name(name):
    connection = con_db()
    cursor = connection.cursor()
    cursor.execute('SELECT name, q, w, e, r FROM Heroes WHERE name = ?', (name,))
    hero = cursor.fetchone()
    connection.close()
    return hero


def update_skills_by_name(name, new_q, new_w, new_e, new_r):
    connection = con_db()
    cursor = connection.cursor()
    cursor.execute('UPDATE Heroes SET q = ?, w = ?, e = ?, r = ? WHERE name = ?', (new_q, new_w, new_e, new_r, name))
    connection.commit()
    connection.close()
    return f'{name} обновлен!'


def delete_hero_by_name(name):
    connection = con_db()
    cursor = connection.cursor()
    cursor.execute('DELETE FROM Heroes WHERE name = ?', (name,))
    connection.commit()
    connection.close()
    return f'{name} удален!'


def main():
    create_table()
    add_data()


class Hero(BaseModel):
    name: str
    q: str = None
    w: str = None
    e: str = None
    r: str = None

class Abilities(BaseModel):
    q: str = None
    w: str = None
    e: str = None
    r: str = None


@app.post('/add-hero/', response_model=Hero)
async def add_hero(hero: Hero):
    insert_hero(hero.name, hero.q, hero.w, hero.e, hero.r)
    return hero


@app.put('/update-skills-by-name/{hero_name}', response_model=Abilities)
async def change_hero_skills_by_name(hero_name: str, abilities: Abilities):
    update_skills_by_name(hero_name, abilities.q, abilities.w, abilities.e, abilities.r)
    return abilities


@app.delete('/delete-hero-by-name/{hero_name}')
async def remove_hero_by_name(hero_name: str):
   return delete_hero_by_name(hero_name)


@app.get('/select-all-heroes/')
async def get_all_heroes():
   return select_all_heroes()


@app.get('/select-hero-by-name/{hero_name}')
async def get_hero_by_name(hero_name: str):
   return select_hero_by_name(hero_name)


if __name__ == '__main__':
    main()

# uvicorn dota2:app --reload 
