from market import db, login_manager
from market import bcrypt
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(length=30), nullable=False, unique=True)
    email_address = db.Column(db.String(length=50), nullable=False, unique=True)
    password_hash = db.Column(db.String(length=60), nullable=False)
    budget = db.Column(db.Integer(), default=1000)
    items = db.relationship("Item", backref="owned_user", lazy=True)

    @property
    def budget_format(self):
        if len(str(self.budget)) == 4:
            return f"{str(self.budget)[:-3]},{str(self.budget)[-3:]} GHC"
        else:
            return f"{self.budget} GHC"

    @property
    def password(self):
        return self.password

    @password.setter
    def password(self, plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode("utf-8")

    def __repr__(self):
        return f"User {self.username}"

    def check_password_correction(self, attempted_password):
        return bcrypt.check_password_hash(self.password_hash, attempted_password)

    def can_purchase(self, item_obj):
        return self.budget >= item_obj.price

    def can_sell(self, items_obj):
        return items_obj in self.items


class Item(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(length=30), nullable=False, unique=True)
    price = db.Column(db.Integer(), nullable=False)
    brand = db.Column(db.String(length=30), nullable=False)
    description = db.Column(db.String(length=1024), nullable=False)
    owner = db.Column(db.Integer(), db.ForeignKey("user.id"))

    def __repr__(self):
        return f"Item {self.name}"

    def buy(self, user):
        self.owner = user.id
        user.budget -= self.price
        db.session.commit()

    def sell(self, user):
        self.owner = None
        user.budget += self.price
        db.session.commit()

# Item1 = Item("Infix hot 8", 2200, "infixi", "This is an infixi brand new Phone ")
# db.drop_all()
# db.create_all()
# db.session.add(Item1)
# db.session.commit()
# Item.query.all()
# Item1.owner = User.query.filter_by(username="Kwame").first().id
# db.session.add(Item1)
# db.session.commit()

# u1 = User(username="Kwame", email_address="kwame@gmail.com", password_hash="123456")
# db.create_all()
# db.session.add(u1)
# db.session.commit()