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

We can think of SQL Alchemy as a way of describing the database with python constructs.
So a schema is defined in python and then we can use SQLAlchemy to access and manipulate the database.

### db.Model()
This is the base class for all models, so we inherit from it in our model classes. It provides a table name 
and a _query_ attribute attached that we can use to query the database.

For example, as User in the example above, we inherit from db.Model and define a table name.
Because we inherit from db.Model, we can use the query attribute to query the database.

```python
user = User.query.all()
users = User.query.get(1)
```

Resources: https://flask-sqlalchemy.palletsprojects.com/en/2.x/api/#flask_sqlalchemy.Model

### \_\_tablename\_\_
This is the name of the table in the database. If not defined, it will be the name of the class.

### db.Column()
With the help of db.Column() we can define the schema of the database and specify how 
the class properties should be mapped to the database columns. This is the signature:

```python
db.Column(name, type, nullable=False, primary_key=False, unique=False, default=None, server_default=None, onupdate=None, autoincrement=False, comment=None)
```
Most important parameters are:
- Name: name of the column in the database
- Type: type of the column in the database
- Nullable: whether the column can be null or not
- Primary Key: whether the column is a primary key or not
- Unique: whether the column is unique or not
- Default: default value of the column

So if we have:

```python
class User(db.Model):
    id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column("name", db.String(80), nullable=False)
```
We are saying we have a table called users with a column called id of type integer and a column called name of type string and
these two columns are mapped to our class properties id and name respectively. Another key
point is that the column name does not have to match the property name. We can have for example:

```python
class User(db.Model):
    id = db.Column("user_id", db.Integer, primary_key=True)
    name = db.Column("user_name", db.String(80), nullable=False)
```

The user_id column will be mapped to the id property and the user_name column will be mapped to the name property.

Resources: https://docs.sqlalchemy.org/en/14/core/metadata.html#sqlalchemy.schema.Column

### db.relationship()
This is the way to define relationships between tables.
In our example, we have a User class and an Address class.
The User class has a relationship with the Address class, so 
each User has an Address. In our User class we have:

```python
address = db.relationship("Address", backref="user", uselist=False)
address_id = db.Column("address_id", db.Integer, db.ForeignKey("addresses.id"))
```

This is saying that the User class has a relationship with the Address class, 
so the _address_id_ in the User table is a foreign key to the id column in the Address table.
The backref parameter is used to define the name of the relationship in the Address class, 
so in the Address class we can access the User using the user attribute (_address.user_).


Resources: https://flask-sqlalchemy.palletsprojects.com/en/2.x/quickstart/#simple-relationships
### Connection string

Our connection string is:
```python
"postgresql://postgres:postgres@localhost:5432/postgres"
```
Describing each part in sequence:
- postgresql: the database type
- postgres: the username
- postgres: the password
- localhost: the hostname
- 5432: the port
- postgres: the database name

### Differences between SQLAlchemy and Flask SQLAlchemy
https://flask-sqlalchemy.palletsprojects.com/en/2.x/quickstart/#road-to-enlightenment