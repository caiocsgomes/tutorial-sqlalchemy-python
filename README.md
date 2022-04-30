# Practical Flask SQLAlchemy Tutorial

This is a practical guide to using SQLAlchemy with Python. 
We will create a simple database and use it to store and retrieve data.
To create the database we will use docker and postgres.

## Step 1: Create a database

We need docker installed on the computer. Then we can run the following command to create a database.

```dockerfile
docker container build -t postgres-db .
docker container run -d -p 5432:5432 postgres-db
```

This will create a database called `postgres`. This is the schema:

```sql
CREATE TABLE addresses (
    id SERIAL PRIMARY KEY,
    address VARCHAR NOT NULL
);

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    username VARCHAR NOT NULL,
    email VARCHAR NOT NULL,
    address_id INTEGER NOT NULL,
    FOREIGN KEY (address_id) REFERENCES addresses(id)
 );
```

Resources: https://hub.docker.com/_/postgres
## Step 2: Create a Flask app

First we need to install all the dependencies.

```bash
pip install -r requirements.txt
```

Then we can create a Flask app.

```python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:postgres@localhost:5432/postgres"
db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column("name", db.String(80), nullable=False)
    username = db.Column("username", db.String(80), unique=True, nullable=False)
    email = db.Column("email", db.String(120), nullable=False)
    address = db.relationship("Address", backref="user", uselist=False)
    address_id = db.Column("address_id", db.Integer, db.ForeignKey("addresses.id"))

    def __repr__(self):
        return '<User %r>' % self.username


class Address(db.Model):
    __tablename__ = 'addresses'
    id = db.Column("id", db.Integer, primary_key=True)
    address = db.Column("address", db.String(80), unique=True, nullable=False)

    def __repr__(self):
        return '<Address %r>' % self.street_name


if __name__ == '__main__':
    user = User(name='john doe', username='johndoe', email='johndoe@email.com')
    user.address = Address(address='awesome address number 2')
    db.session.add(user)
    db.session.commit()

    # get user by property
    user = User.query.filter_by(username='johndoe').first()
    print(user)

    # get user by id
    user = User.query.get(1)
    print(user)

    # update user
    user = User.query.filter_by(username='johndoe').first()
    user.name = 'john doe updated'
    db.session.commit()
    user = User.query.get(1)
    print(user.name)

    # get all users
    users = User.query.all()
    print(users)

    # delete user
    db.session.delete(user)
    db.session.commit()
```

Resources: https://flask-sqlalchemy.palletsprojects.com/en/2.x/quickstart/

## Step 3: Understanding the app

- explain db.Column
- explain db.relationship
- explain db.Model
- explain \_\_tablename\_\_
- explain connectio string

