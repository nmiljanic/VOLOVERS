from pony.orm import Database, PrimaryKey, Required, Set, Optional
from datetime import datetime

db = Database()

class Volonter(db.Entity):
    volonter_id = PrimaryKey(int, auto=True)
    ime = Required(str)
    prezime = Required(str)
    email_volontera = Required(str)
    kontakt_broj_volontera = Required(str)
    aktivnost_id= Optional('VolonterskaAktivnost')

class VolonterskaAktivnost(db.Entity):
    aktivnost_id = PrimaryKey(int, auto=True)
    naziv_aktivnosti = Required(str)
    opis_aktivnosti = Required(str)
    lokacija_aktivnosti = Required(str)
    datum_vrijeme_aktivnosti = Required(datetime)
    broj_volontera = Optional(str)
    volonter = Set('Volonter')
    status_aktivnosti = Optional(str)

db.bind(provider='sqlite', filename='volovers.sqlite', create_db=True)
db.generate_mapping(create_tables=True)