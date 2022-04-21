from flask_admin.contrib.sqla import ModelView
from app import db, admin


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(150))
    admin = db.Column(db.BOOLEAN, default=False)


class Drinks(db.Model):
    __tablename__ = "drinks"
    index = db.Column(db.Integer, primary_key=True, autoincrement=True)
    strDrink = db.Column(db.String(100))
    strAlcoholic = db.Column(db.String(100))
    strCategory = db.Column(db.String(100))
    strGlass = db.Column(db.String(100))
    strInstructions = db.Column(db.String(500))
    strIngredient1 = db.Column(db.String(100))
    strIngredient2 = db.Column(db.String(100))
    strIngredient3 = db.Column(db.String(100))
    strIngredient4 = db.Column(db.String(100))
    strIngredient5 = db.Column(db.String(100))
    strIngredient6 = db.Column(db.String(100))
    strIngredient7 = db.Column(db.String(100))
    strIngredient8 = db.Column(db.String(100))
    strIngredient9 = db.Column(db.String(100))
    strIngredient10 = db.Column(db.String(100))
    strIngredient11 = db.Column(db.String(100))
    strIngredient12 = db.Column(db.String(100))
    strMeasure1 = db.Column(db.String(100))
    strMeasure2 = db.Column(db.String(100))
    strMeasure3 = db.Column(db.String(100))
    strMeasure4 = db.Column(db.String(100))
    strMeasure5 = db.Column(db.String(100))
    strMeasure6 = db.Column(db.String(100))
    strMeasure7 = db.Column(db.String(100))
    strMeasure8 = db.Column(db.String(100))
    strMeasure9 = db.Column(db.String(100))
    strMeasure10 = db.Column(db.String(100))
    strMeasure11 = db.Column(db.String(100))
    strMeasure12 = db.Column(db.String(100))
    strDrinkThumb =  db.Column(db.String(100))


class MyModelView(ModelView):
    can_view_details = True
    can_set_page_size = True
    can_export = True


admin.add_view(MyModelView(User, db.session))
admin.add_view(MyModelView(Drinks, db.session))