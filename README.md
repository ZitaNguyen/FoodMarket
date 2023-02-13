
# Food Market Web Application

#### Video Demo:   [URL here](https://www.youtube.com/watch?v=0olo0vUtuM0)

#### Description:

**Idea**

Living in a foreign country, I am always craving for Vietnamese food, but it's not easy to find. I only know some good sellers by the word-of-mouth or by Facebook groups. Furthermore, some of them are really far from my place. Therefore I would like to build a website for sellers to promote their business and for buyers to easily find Vietnamese food, which is nearby.Living in a foreign country, I am always craving for Vietnamese food, but it's not easy to find. I only know some good sellers by the word-of-mouth or by Facebook groups. Furthermore, some of them are really far from my place. Therefore I would like to build a website for sellers to promote their business and for buyers to easily find Vietnamese food, which is nearby.

**Website Functionalities**

* Users can register as a buyer or a seller, which allows them to log in and log out. Then they can modify their profile, for example to change their name or password. They can also delete their profile as they wish.

* As sellers, they can add a product in their menu by filling a form and uploading their food photo. Each photo is saved under a unique name using uuid4. Sellers can also modify their products for example food name, food price, food photo or food description. If they no longer sell any dishes, they can delete it out of their menu.

* Both sellers and buyers can browse through the website for their desired products by typing dish name, or sellers nearby by typing a district number in a search bar. If users click on any food item on the search result list, they are redirected to that product page, including seller contact detail and other offers from the same seller.

**Website Pages**

* Index page (Main page): all of the latest food added into the db, divided into 3 sections (starters, main dishes, desserts). If there is no food for any section, you will see a "No food" image.

* Starters page/ Main dishes page/ Desserts page: show all offers from all sellers for each category

* Product page: Show food photo, name, price and description with the seller contact details at the left side, below displaying other offers from the same seller.

* Profile page: if seller, there is his contact details, and his menu; if buyer, there is only his name and email.

* Search page: show list of search results

* Register page: allows users to register their account

* Login page: allows users to login by their email and password

**Languages and Frameworks**

* Flask - Python
* Jinja2 - HTML
* Bootstrap - CSS
* FontAwesome
* Javascript
* SQLite

**Database diagram**
![Food Market DB](/static/photos/FoodMarket.png)

**How to run the application**
1. Install Python
```
$ brew install python
$ python --version
```
2. Clone this project to your local
```
$ git clone https://github.com/ZitaNguyen/FoodMarket.git
```
3. Create virtual environment and activate
```
$ python3 -m venv venv
$ source venv/bin/activate
```
4. Install all required packages
```
$ pip install -r requirements.txt
```
5. Start Django server and run locally
```
$ flask run
```

