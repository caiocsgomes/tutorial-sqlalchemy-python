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
