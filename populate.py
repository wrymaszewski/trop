import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','climbing_project.settings')

import django
django.setup()

from django.contrib.auth import get_user_model
import random
from faker import Faker
from routes.models import Ascent, Route, Sector
from indoor.models import Top, Training, Gym
from accounts.models import User, UserProfile, Group
from posts.models import Post, Comment
from django.db import IntegrityError
fakegen = Faker()
User = get_user_model()

def populate_user(N=200):
    # create N users and userprofiles

    for i in range(N):
        # Create Fake Data for entry
        fake_name = fakegen.name().split()
        fake_first_name = fake_name[0]
        fake_last_name = fake_name[1]
        fake_username = '_'.join([fake_first_name, fake_last_name])
        fake_password = 'nWckx134klvkc837'
        fake_email = fakegen.email()
        fake_description = fakegen.text()

        # Create new User
        user = User.objects.get_or_create(username=fake_username,
                                         password = fake_password)[0]

        # Create new UserProfile
        try:
            userprofile =UserProfile.objects.get_or_create(user = user,
                                                    first_name = fake_first_name,
                                                    last_name = fake_last_name,
                                                    email = fake_email,
                                                    description = fake_description,
                                                    hidden = bool(random.getrandbits(1))
                                                    )
        except IntegrityError:
            pass


def populate_sector (N=100):
    for sec in range(N):
        lat = str(fakegen.latitude())
        lng = str(fakegen.longitude())
        fake_location = ','.join([lat,lng])
        fake_address = ', '.join([fakegen.city(), fakegen.country()])

        sector = Sector.objects.get_or_create(
                                name = fakegen.street_name(),
                                region = fake_address,
                                location = fake_location
                                )[0]

        for rou in range(5):

            try:
                route = Route.objects.get_or_create(
                                sector = sector,
                                name = fakegen.catch_phrase(),
                                route_type = random.choice(Route.ROUTE_TYPE_CHOICES)[0],
                                protection = random.choice(Route.PROTECTION_CHOICES)[0],
                                scale = Route.FR,
                                grade = random.choice(['6b', '5c', '7c', '9a', '6a', '7a', '6c+', '8a', '7c']),
                                )[0]
            except IntegrityError:
                pass

            for asc in range(3):
                try:
                    user = random.choice(User.objects.all())
                    ascent = Ascent.objects.get_or_create(
                        route = route,
                        user = user,
                        date = fakegen.date_this_century(),
                        ascent_style = random.choice(Ascent.ASCENT_STYLE_CHOICES)[0],
                        rating = random.choice(Ascent.RATING_CHOICES)[0],
                        description = fakegen.text()
                    )
                except IntegrityError:
                    pass

def populate_indoor(N=20):
    for gyms in range(N):
        street = fakegen.street_name()
        city = fakegen.city()
        address = ', '.join([street, city])
        lat = str(fakegen.latitude())
        lng = str(fakegen.longitude())
        fake_location = ','.join([lat,lng])

        gym = Gym.objects.get_or_create(
                            name = fakegen.domain_word(),
                            address = address,
                            location = fake_location
                            )[0]

        for trainings in range(5):

            user = random.choice(User.objects.all())
            try:
               training = Training.objects.get_or_create(
                            user = user,
                            location = gym,
                            date = fakegen.date_this_century(),
                            description = fakegen.text()
                            )[0]
            except IntegrityError:
                pass

            for tops in range(4):
                try:
                    top = Top.objects.get_or_create(
                                    training = training,
                                    route_type = random.choice(Top.ROUTE_TYPE_CHOICES)[0],
                                    scale = Route.FR,
                                    grade = random.choice(['6b', '5c', '7c', '9a', '6a', '7a', '6c+']),
                                    ascent_style = random.choice(Ascent.ASCENT_STYLE_CHOICES)[0],
                                    )
                except IntegrityError:
                    pass

def populate_post (N=10):

    for groups in range(N):
        user1 = random.choice(User.objects.all())
        user2 = random.choice(User.objects.all())
        user3 = random.choice(User.objects.all())

        group = Group.objects.get_or_create(
                        name = fakegen.word(),
                        description = fakegen.sentence(),
                        # members = [user1, user2, user3]
                        )[0]
        for posts in range(5):
            user = random.choice([user1, user2, user3])
            try:
                post = Post.objects.get_or_create(
                    group = group,
                    author = user,
                    title = fakegen.sentence(),
                    text = fakegen.text(),
                    )[0]
            except IntegrityError:
                pass

            for comments in range(3):
                com_user = random.choice(User.objects.all())

                try:
                    comment = Comment.objects.get_or_create(
                        post = post,
                        author = com_user,
                        text = fakegen.text()
                        )
                except IntegrityError:
                    pass


if __name__ == '__main__':
    print("Populating the databases...Please Wait")
    print('....Populating User and UserProfile')
    populate_user(5)
    print('....Populating Sectors')
    populate_sector(5)
    print('....Populating Indoor')
    populate_indoor(5)
    print('....Populating Post')
    populate_post(5)
    print('Populating Complete')
