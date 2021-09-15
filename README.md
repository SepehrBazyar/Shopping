# Shopping
Bilingual Online Shopping System Project with Python &amp; Django Framework &amp; REST API

## Photos:
<img src="https://user-images.githubusercontent.com/79161571/133458363-da5e062d-8506-4b21-9989-5ef51cf231ef.jpg" alt="home-page-fa" align="center"/>
<img src="https://user-images.githubusercontent.com/79161571/133458487-e65c7994-3af6-4794-819f-ddbc01d08e7a.jpg" alt="product-list-en" align="center"/>
<img src="https://user-images.githubusercontent.com/79161571/133458507-d49c65fc-7880-4ac9-b207-8b9879b46a06.jpg" alt="cart-page-fa" align="center"/>

### Responsive Mode:
<div>
  <img src="https://user-images.githubusercontent.com/79161571/133458539-e9f96c6e-bd04-48d4-8821-9e05b3fb5cc7.jpg" alt="responsive-category-list"/>
  <img src="https://user-images.githubusercontent.com/79161571/133458578-a9c28e37-ae99-49ed-95e7-750d973a2f63.jpg" alt="responsive-404-not-found" align="right"/>
</div>

## Tools:
1. Back-End: Python, Django, REST API
2. Data Base: PostgreSQL, MongoDB
3. Front-End: HTML5, CSS3, JavaScript, Bootstrap4, jQuery, AJAX

## How to Run?
1. Clone the Project
* `git clone https://github.com/SepehrBazyar/Shopping.git`
2. Create a Virtual Environment("venv" is a Selective Name).
* `virtualenv venv`
3. Activate the Interpreter of the Virtual Environment
* Windows: `venv\Script\active`
* Linux: `source venv/bin/active`
4. Install the Requirements
* `pip install -r requirements.txt`
5. Adjust the Data Base Amount in `settings.py` File in `shopping` Directory
6. Write the Following Command to Create Media Directory
* `mkdir media`
7. Write the Following Command to Compile the Translations
* `python manage.py compilemessages -l fa`
8. Write the Following Command to Create Your Tables
* `python manage.py migrate`
9. Write the Following Command to Create a Superuser
* `python manage.py createsuperuser`
10. Run the MongoDB
11. Write the Following Command to Run the Server
* `python manage.py runserver`

## Features:
* Its Language Changes with One Click
* "Cart" &amp; "Contact Me" Pages are Single Page Application
* Set Cookie to Add Product to Cart without Logging in
* Animated Features in the "Cart Icon", "Category List Page" &amp; "Carousel"
