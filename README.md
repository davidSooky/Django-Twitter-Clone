# Twitter Clone built with Django and JavaScript
Functional Twitter Clona where you can make posts, upload images, comment on posts and customise your profile.

Like funcionality, searching for other peoples profiles and infinite scrolling is managed by an API built with Django Rest Framework.

So far only posting and commenting is working, making groups or chat functionality is not implemented.

## Project Screenshots
[!alt text](./static/images/demo.gif)
[!alt text](./static/images/signup.png)
[!alt text](./static/images/main_page.png)
[!alt text](./static/images/profile_page.png)

## How to get started

- Git Clone the project with: ```git clone https://github.com/davidSooky/Django-Twitter-Clone.git```

- Move to the base directory: ```cd Django-Twitter-Clone```

- Create a new python enveronment with: ```python -m venv env```

- Activate enveronment with: ```env\Scripts\activate``` on windows, or ```source env/bin/activate``` on Mac and Linux

- Install required dependencies with: ```pip install -r requirements.txt```

- Make migrations with: ```python manage.py makemigrations``` and then ```python manage.py migrate```

- Run app localy with: ```python manage.py runserver```

- Make your own profile :)

## License
[MIT](https://choosealicense.com/licenses/mit/)