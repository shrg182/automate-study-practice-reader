import sqlite3

def demo():
    db = sqlite3.connect(":memory:")
    db.execute("create table note(id integer primary key, text text not null)")
    db.execute("insert into note(text) values (?)", ("Read transactions",))
    return db.execute("select text from note").fetchone()[0]
if __name__ == "__main__": print(demo())
