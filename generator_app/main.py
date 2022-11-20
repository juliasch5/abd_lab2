import csv
from faker import Faker
from datetime import datetime
from dateutil.relativedelta import relativedelta
import random
import math
import array

fake = Faker()
t0 = datetime(1900, 1, 1)
t1 = datetime(2022, 12, 31)
SERIES_COUNT = 100
MOVIES_COUNT = 500
EPISODES_COUNT = 1200 
ROLES_COUNT = 2000
SEASONS_COUNT = 300


def list2str(s):
    str1 = ""
    for i in s:
        str1 += i
    return str1


def pick_random_from_csv(filename, column):
    path = './files/' + filename
    # encoding="utf-8"
    with open(path) as f:
        reader = csv.reader(f)
        chosen_row = random.choice(list(reader))
        return list2str(chosen_row[column])


def pick_from_csv(filename, column, row):
    path = './files/' + filename
    # encoding="utf-8"
    i = 0
    with open(path) as f:
        reader = csv.reader(f)
        for line in reader:
            if i == row:
                return list2str(line[column])
            i += 1


# def find_serie(class_id):
#     s = 0
#     c = 0
#     found = 0;
#     while found != 1:
#         s = random.randint(0, STUDENTS_COUNT - 1)
#         c = random.randint(0, COURSES_COUNT - 1)
#         if class_id[c][s] == 0:
#             class_id[c][s] = 1
#             found = 1

#     return c + 1, s + 1


# def generate_course_time():
#     day = ['' for _ in range(COURSES_COUNT)]
#     time = ['' for _ in range(COURSES_COUNT)]

#     for i in range(COURSES_COUNT):
#         day[i] = pick_random_from_csv('dni_tygodnia.csv')
#         hour = random.randint(8, 20)
#         if hour < 10:
#             hour = '0' + ''.join(["{}".format(hour)])
#         else:
#             hour = ''.join(["{}".format(hour)])
#         time[i] = hour + ':00:00'

#     return day, time


def create_genres():
    with open('./files/Genres' + '.csv', 'w', newline='') as csvfile:
        fieldnames = ['name']

        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=',')
        writer.writeheader()

        writer.writerow({'name': 'comedy'})
        writer.writerow({'name': 'drama'})
        writer.writerow({'name': 'horror'})
        writer.writerow({'name': 'thriller'})
        writer.writerow({'name': 'action'})
        writer.writerow({'name': 'adventure'})
        writer.writerow({'name': 'fantasy'})
        writer.writerow({'name': 'romance'})
        writer.writerow({'name': 'sci-fi'})
        writer.writerow({'name': 'crime'})
        writer.writerow({'name': 'animation'})
        writer.writerow({'name': 'family'})
        writer.writerow({'name': 'history'})
        writer.writerow({'name': 'musical'})
        writer.writerow({'name': 'biography'})
        writer.writerow({'name': 'documentary'})



def create_movies():
    with open('./files/Movies' + '.csv', 'w', newline='') as csvfile:
        fieldnames = ['title', 'year', 'language', 'localization']

        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=',')
        writer.writeheader()

        for i in range(MOVIES_COUNT):
            writer.writerow(
                {
                    'title': pick_random_from_csv('titles.csv', 2).capitalize(),
                    'year': random.randint(1900, 2022),
                    'language': fake.language_name(),
                    'localization': fake.country()
                }
            )


def create_series():
    with open('./files/Series' + '.csv', 'w', newline='') as csvfile:
        fieldnames = ['title', 'year', 'language', 'localization', 'start_date', 'end_date']

        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=',')
        writer.writeheader()

        for i in range(SERIES_COUNT):
            date = fake.date_between(start_date=t0, end_date=t1)

            writer.writerow(
                {
                    'title': pick_random_from_csv('titles.csv', 2).capitalize(),
                    'year': date.year,
                    'language': fake.language_name(),
                    'localization': fake.country(),
                    'start_date': date,
                    'end_date': fake.date_between(start_date=date, end_date=t1)
                }
            )


def create_seasons():
    with open('./files/Seasons' + '.csv', 'w', newline='') as csvfile:
        fieldnames = ['season_number', 'series_id']

        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=',')
        writer.writeheader()

        for c in range(SEASONS_COUNT):
            writer.writerow(
                {
                    'season_number': random.randint(1, 10),
                    'series_id': random.randint(1, SERIES_COUNT)
                }
            )


def create_episodes():
    with open('./files/Episodes' + '.csv', 'w', newline='') as csvfile:
        fieldnames = ['title', 'year', 'language', 'localization', 'episode_number', 'season_id']

        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=',')
        writer.writeheader()

        for i in range(EPISODES_COUNT):
            season = random.randint(1, SEASONS_COUNT)
            serie = pick_from_csv('Seasons.csv', 1, season)
            start_year = pick_from_csv('Series.csv', 4, int(serie)).split('-')[0]
            end_year = pick_from_csv('Series.csv', 5, int(serie)).split('-')[0]

            writer.writerow(
                {
                    'title': pick_random_from_csv('titles.csv', 2).capitalize(),
                    'year': random.randint(int(float(start_year)), int(float(end_year))),
                    'language': pick_from_csv('Series.csv', 2, int(serie)),
                    'localization': pick_from_csv('Series.csv', 3, int(serie)),
                    'episode_number': random.randint(1, 25),
                    'season_id': season
                }
            )


def create_roles():
    with open('./files/Roles' + '.csv', 'w', newline='') as csvfile:
        fieldnames = ['name', 'surname', 'role_name', 'movie_id']

        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=',')
        writer.writeheader()

        for c in range(ROLES_COUNT):
            writer.writerow(
                {
                    'name': fake.first_name(),
                    'surname': fake.last_name(),
                    'role_name': pick_random_from_csv('role_names.csv', 0),
                    'movie_id': random.randint(1, MOVIES_COUNT)
                }
            )



def create_csv_files():
    create_genres()
    create_movies()
    create_series()
    create_seasons()
    create_episodes()
    create_roles()


if __name__ == '__main__':
    create_csv_files()
    print('generation DATA completed.')
