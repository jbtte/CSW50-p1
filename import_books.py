import csv
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

def main():
    f = open("books.csv")
    reader = csv.reader(f)
    for x_isbn, x_title, x_author, x_year in reader:
        db.execute("INSERT INTO books (isbn, title, author, year) VALUES (:y_isbn, :y_title, :y_author, :y_year)",
                    {"y_isbn": x_isbn, "y_title": x_title, "y_author": x_author, "y_year":x_year})
    db.commit()

if __name__ == "__main__":
    main()
