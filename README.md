# Finder_And_I

This is a simple application that helps you locate your friends on campus.

It is built using Django

HOW TO RUN THE WEBSITE!!!!!
# IN COMMAND PROMPT DO THIS (to activate virtual environment):
myworld\Scripts\activate.bat

# Then this; cd path till where your manange.py file is
something like this;
(myworld) C:\Users\erajr> cd C:\Users\erajr\Personal_blogapp\Personal_Blog

# Install the requirments 
pip install -r requirements.txt


# run  migrations
python manage.py makemigrations 

python manage.py migrate


# create a super user to log in for admin
python manage.py createsuperuser
(then enter username, email and password once asked!)


# Now you can run the server to see the app running 

python manage.py runserver
