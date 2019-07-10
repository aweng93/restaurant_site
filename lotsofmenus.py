from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
 
from database_setup import Restaurant, Base, MenuItem, User
 
engine = create_engine('sqlite:///restaurantmenu.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine
 
DBSession = scoped_session(sessionmaker(bind=engine))
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()



#Menu for Haru Ichiban
restaurant1 = Restaurant(name = "Haru Ichiban")

session.add(restaurant1)
session.commit()


menuItem1 = MenuItem(
    name = "Tonkotsu Ramen", 
    description = "Creamy pork broth filled with chashu pork, seaweed, corn, soft boiled egg, and noodles.", 
    price = "$8.99", 
    course = "Main", 
    restaurant = restaurant1)

session.add(menuItem1)
session.commit()

menuItem2 = MenuItem(
    name = "Miso Ramen", 
    description = "Juicy grilled chicken patty with tomato mayo and lettuce", 
    price = "$5.50", 
    course = "Entree", 
    restaurant = restaurant1)

session.add(menuItem2)
session.commit()

menuItem3 = MenuItem(
    name = "Shio Ramen", 
    description = "fresh baked and served with ice cream", 
    price = "$3.99", 
    course = "Entree", 
    restaurant = restaurant1)

session.add(menuItem3)
session.commit()

menuItem4 = MenuItem(
    name = "Beef Menchikatsu", 
    description = "Made with grade A beef", 
    price = "$7.99", 
    course = "Entree", 
    restaurant = restaurant1)

session.add(menuItem4)
session.commit()

menuItem5 = MenuItem(
    name = "Ramune", 
    description = "16oz of Japanese Marble Soda",
    price = "$1.99", 
    course = "Beverage", 
    restaurant = restaurant1)

session.add(menuItem5)
session.commit()

menuItem6 = MenuItem(
    name = "Iced Tea", 
    description = "with Lemon", 
    price = "$.99", 
    course = "Beverage", 
    restaurant = restaurant1)

session.add(menuItem6)
session.commit()

menuItem7 = MenuItem(
    name = "Tsukemen Ramen", 
    description = "Dipping Noodles with a Tonkotsu broth", 
    price = "$3.49", 
    course = "Entree", 
    restaurant = restaurant1)

session.add(menuItem7)
session.commit()

menuItem8 = MenuItem(
    name = "Katsu Curry", 
    description = "Made with freshest of ingredients and home grown spices", 
    price = "$5.99", 
    course = "Entree", 
    restaurant = restaurant1)

session.add(menuItem8)
session.commit()




#Menu for Momofuku Noodle Bar
restaurant2 = Restaurant(name = "Momofuku Noodle Bar")

session.add(restaurant2)
session.commit()


menuItem1 = MenuItem(
    name = "Stuffed Dip (1pc)", 
    description = "Daily selection of delicious wraps", 
    price = "$8", 
    course = "Appetizer", 
    restaurant = restaurant2)

session.add(menuItem1)
session.commit()

menuItem2 = MenuItem(
    name = "Seared Shrimp (2pc)", 
    description = "Jumbo shrimp seared on a grill dressed with spicy red mayo and pickled onion", 
    price = "$13", 
    course = "Appetizer", 
    restaurant = restaurant2)

session.add(menuItem2)
session.commit()

menuItem3 = MenuItem(
    name = "Spicy Beef Ramen", 
    description = "Intensely flavored short rib with delicious noodles and water spinach", 
    price = "19", 
    course = "Entree", 
    restaurant = restaurant2)

session.add(menuItem3)
session.commit()

menuItem4 = MenuItem(
    name = "Garlic Chicken Ramen ", 
    description = "Savory chicken broth with yu choy, egg yolk, and garlic.", 
    price = "17", 
    course = "Entree", 
    restaurant = restaurant2)

session.add(menuItem4)
session.commit()

menuItem5 = MenuItem(
    name = "Smoked Pork Ramen", 
    description = "Thick creamy broth served with pork belly, egg yolk, and bamboo", 
    price = "18", 
    course = "Entree", 
    restaurant = restaurant2)

session.add(menuItem5)
session.commit()

menuItem6 = MenuItem(
    name = "Spicy Oxtail", 
    description = "Large hearty dish served with rice cakes, daikon, and buttered rice", 
    price = "32", 
    course = "Main", 
    restaurant = restaurant2)

session.add(menuItem6)
session.commit()




#Menu for Umami Ramen
restaurant3 = Restaurant(name = "Umami Ramen")

session.add(restaurant3)
session.commit()


menuItem1 = MenuItem(
    name = "Pork Buns", 
    description = "oven roasted house cured pork belly with pickled cucumbers, scallions and special blend hoisin sauce.", 
    price = "", 
    course = "", 
    restaurant = restaurant3)

session.add(menuItem1)
session.commit()

menuItem2 = MenuItem(
    name = "Pork and Chives Dumplings",
    description = "with Taiwanese cabbage, Chinese chives, and ginger", 
    price = "9", 
    course = "Appetizer", 
    restaurant = restaurant3)

session.add(menuItem2)
session.commit()

menuItem3 = MenuItem(
    name = "Tonkotsu Ramen", 
    description = "rich pork broth with fresh ramen noodles topped with flavor infused egg, braised pork, marinated bamboo shoots, nori (seaweed) and green onions",
    price = "12", 
    course = "Entree", 
    restaurant = restaurant3)

session.add(menuItem3)
session.commit()

menuItem4 = MenuItem(
    name = "Matcha Green Tea Creme Brulee", 
    description = "Savory, creamy, and light", 
    price = "5", 
    course = "Dessert", 
    restaurant = restaurant3)

session.add(menuItem4)
session.commit()



#Menu for Thyme for that
restaurant4 = Restaurant(name = "Thyme for That Vegetarian Cuisine ")

session.add(restaurant4)
session.commit()


menuItem1 = MenuItem(
    name = "Tres Leches Cake", 
    description = "Rich, luscious sponge cake soaked in sweet milk and topped with vanilla bean whipped cream and strawberries.", 
    price = "5", 
    course = "Dessert", 
    restaurant = restaurant4)

session.add(menuItem1)
session.commit()

menuItem2 = MenuItem(
    name = "Mushroom risotto", 
    description = "Portabello mushrooms in a creamy risotto", 
    price = "10", 
    course = "Entree", 
    restaurant = restaurant4)

session.add(menuItem2)
session.commit()

menuItem3 = MenuItem(
    name = "Honey Boba Shaved Snow", 
    description = "Milk snow layered with honey boba, jasmine tea jelly, grass jelly, caramel, cream, and freshly made mochi", 
    price = "3", 
    course = "Beverage", 
    restaurant = restaurant4)

session.add(menuItem3)
session.commit()

menuItem4 = MenuItem(
    name = "Cauliflower Manchurian", 
    description = "Golden fried cauliflower florets in a midly spiced soya,garlic sauce cooked with fresh cilantro, celery, chilies,ginger & green onions", 
    price = "12", 
    course = "Main", 
    restaurant = restaurant4)

session.add(menuItem4)
session.commit()

menuItem5 = MenuItem(
    name = "Aloo Gobi Burrito", 
    description = "Vegan goodness. Burrito filled with rice, garbanzo beans, curry sauce, potatoes (aloo), fried cauliflower (gobi) and chutney. Nom Nom", 
    price = "9", 
    course = "Main", 
    restaurant = restaurant4)

session.add(menuItem5)
session.commit()


print ("added menu items!")

