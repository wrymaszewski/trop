# TROP application

> Backend by [Wojtek Rymaszewski](https://github.com/wrymaszewski)
> Frontend by [Mikołaj Klarżuk](https://github.com/daxtersky)

## Summary

Endomondo for Climbers. It allows users to Sign Up and upload their outdoor ascents and indoor training to the database. Users can form groups to post and comment on eachother's achievements. Ascents and trainings are visualized by [Highcharts](https://www.highcharts.com)-powered charts.

## Apps
- [**Acconts**](accounts/) - Information about user profiles and user groups. Users can hide their profiles if they prefer not to be visible to other users.
- [**Routes**](routes/) - Module for tracking outdoor ascents.
- [**Indoor**](indoor/) - Module for tracking indoor trainings.
- [**Posts**](posts/) - Social networking module for creation of posts and comments in user groups.

## Technologies

- Python/Django
- HTML5
- CSS3 + Sass
- JavaScript + jQuery

## APIs
 - [GoogleMaps Javascript API](https://developers.google.com/maps)
 - [Highcharts](https://www.highcharts.com) (via chartit package)
 - [Cloudinary](https://cloudinary.com/)

## To do

- [x] accounts module
- [x] routes module
- [x] indoor module
- [x] posts module
- [ ] mobile version

## CLI commands
  The project will be soon deployed, however now it can be previewed on a local machine. Steps required are listed below:
  1. Download and install [Anaconda](https://www.anaconda.com/download/#linux)
  2. Create a virual environent in your terminal: `conda create --name <environment_name>`
  2. Activate the environment: `activate <environment_name>` (Windows) or `source activate <environment_name>` (MacOS, Linux)
  3. Install PIP and dependencies:
  ```
  conda install -c anaconda pip
  pip install django
  pip install django-extensions
  pip install chartit
  pip install cloudinary
  pip install django-mediumeditor
  pip install django-location-field
  ```
  4. Clone the repo: `git clone https://github.com/wrymaszewski/trop.git`
  5. Go into the main folder containing manage.py and start the server: `python manage.py runserver`. local server setup default address is <http://127.0.0.1:8000/>

Please report bugs to wrymaszewski@gmail.com or in the Issues section.
