# TROP application

> Backend by [Wojtek Rymaszewski](https://github.com/wrymaszewski)
> Frontend by [Mikołaj Klarżuk](https://github.com/daxtersky)

## Summary

Endomondo for Climbers. It allows users to Sign Up and upload their outdoor ascents and indoor training to the database. Users can form groups to post and comment on eachother's achievements. Ascents and trainings are visualized by [Highcharts](https://www.highcharts.com)-powered charts.

## Apps

- [**Accounts**](accounts/) - Information about user profiles and user groups. Users can hide their profiles if they prefer not to be visible to other users.
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
- [ ] pretty frontend
- [ ] mobile version

## CLI commands

The App is now deployed at: <https://trackyourtops.herokuapp.com>
It can be previewed on a local machine. Steps required are listed below:

1. Download and install [Anaconda](https://www.anaconda.com/download/#linux)
1. Create a virual environent in your terminal:
    ```bash
    conda create --name <environment_name>
    ```
    <!-- do not delete that slash below! -->
1. Activate the environment:\
    (Windows)
    ```bash
    activate <environment_name>
    ```
    (MacOS, Linux)
    ```bash
    source activate <environment_name>
    ```
1. Clone the repo:
    ```bash
    git clone <https://github.com/wrymaszewski/trop.git>
    ```
1. Go to the main folder

1. Install PIP and dependencies:
    ```bash
    conda install -c anaconda pip
    pip install -r requirements.txt
    ```
1. Start the server:
    ```bash
    python manage.py runserver
    ```
    local server setup default address is <http://127.0.0.1:8000/>. You can clear the existing database with
    ```bash
    python manage.py flush
    ```
    and populate it with fake data using
    ```bash
    python populate.py
    ```

1. Please report bugs to <wrymaszewski@gmail.com> or in the Issues section.
