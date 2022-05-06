from flask_admin.contrib.sqla import ModelView
from app import db, admin


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(150))
    admin = db.Column(db.BOOLEAN, default=False)
    api_key = db.Column(db.String(45), nullable=False)


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
    strDrinkThumb = db.Column(db.String(100))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def assign_ingredients(self, ingredients):
        for count, ingredient in enumerate(ingredients):
            count += 1
            if count == 1:
                self.strIngredient1 = ingredient
                continue
            if count == 2:
                self.strIngredient2 = ingredient
                continue
            if count == 3:
                self.strIngredient3 = ingredient
                continue
            if count == 4:
                self.strIngredient4 = ingredient
                continue
            if count == 5:
                self.strIngredient5 = ingredient
                continue
            if count == 6:
                self.strIngredient6 = ingredient
                continue
            if count == 7:
                self.strIngredient7 = ingredient
                continue
            if count == 8:
                self.strIngredient8 = ingredient
                continue
            if count == 9:
                self.strIngredient9 = ingredient
                continue
            if count == 10:
                self.strIngredient10 = ingredient
                continue
            if count == 11:
                self.strIngredient11 = ingredient
                continue
            if count == 12:
                self.strIngredient12 = ingredient
                continue


class DataUsage(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    endpoint = db.Column(db.String(150))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    timestamp = db.Column(db.DateTime)
    data_amount = db.Column(db.Integer, nullable=False)


class MyModelView(ModelView):
    can_view_details = True
    can_set_page_size = True
    can_export = True


admin.add_view(MyModelView(User, db.session))
admin.add_view(MyModelView(Drinks, db.session))
admin.add_view(MyModelView(DataUsage, db.session))

