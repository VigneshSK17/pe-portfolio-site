import os
from flask import Flask, render_template, request, url_for
from dotenv import load_dotenv

from peewee import *
from datetime import datetime
from playhouse.shortcuts import model_to_dict

load_dotenv()
app = Flask(__name__)

mydb = MySQLDatabase(os.getenv("MYSQL_DATABASE"),
              user=os.getenv("MYSQL_USER"),
              password=os.getenv("MYSQL_PASSWORD"),
              host=os.getenv("MYSQL_HOST"),
              port=3306)

print(mydb)

class TimelinePost(Model):
    name = CharField()
    email = CharField()
    content = TextField()
    created_at = DateTimeField(default=datetime.now)

    class Meta:
        database = mydb


mydb.connect()
mydb.create_tables([TimelinePost])

@app.route('/')
def index():

    # Formatted as [latitude, longitude, description]
    # latitude: S is negative, longitude: W is negative
    locations = [
        [34.0708, -84.2772, "Alpharetta, GA, USA - Hometown"],
        [40.5804, -74.2851, "Avenel, NJ, USA - Previously Lived"],
        [1.3521, 103.8198, "Singapore - Previously Lived"],
        [13.0843, 80.2705, "Chennai, India - Birthplace"],
        [33.7756, -84.3963, "Georgia Tech - Pursuing BS in CS"]
    ]

    return render_template('index.html', title="MLH Fellow", url=os.getenv("URL"), active_page = 'home', mapsApiKey=os.getenv("MAPS_API_KEY"), locations=locations)

@app.route('/about')
def about():
    hobbies = [
        {"name": "Working out", "description": "Love to workout ", "img_url": url_for('static', filename='img/gym.jpg')},
        {"name": "Traveling", "description": "Exploring new places, especially around the city", "img_url": url_for('static', filename='img/traveling.jpg')},
        {"name": "Eating out", "description": "Trying different restaurant cuisines", "img_url": url_for('static', filename='img/restaurant.jpg')},
        {"name": "Programing", "description": "Learning new programing concepts!", "img_url": url_for('static', filename='img/Programing.jpg')},
    ]

    # If you prefer a separate loop for adding URLs, use the following:
    # for hobby in hobbies:
    #     hobby['img_url'] = url_for('static', filename='img/' + hobby['img'])

    return render_template('about.html', title="About Me", active_page = 'about', hobbies = hobbies)

@app.route('/work')
def work():
    work_experiences = [
        {
            "role": "Role Name",
            "company": "Company Name",
            "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.",
            "dates": "June 2024 - Present",
            "link": "http://www.google.com",
            "img_url": url_for('static', filename='img/logo.jpg')
        },
        {
            "role": "Role Name",
            "company": "Company Name",
            "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.",
            "dates": "June 2024 - Present",
            "link": "http://www.google.com",
            "img_url": url_for('static', filename='img/logo.jpg')
        },
        {
            "role": "Role Name",
            "company": "Company Name",
            "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.",
            "dates": "June 2024 - Present",
            "link": "http://www.google.com",
            "img_url": url_for('static', filename='img/logo.jpg')
        }
    ]

    return render_template('work.html', title="Work Experience", active_page = 'work', work_experiences=work_experiences)

@app.route('/projects')
def projects():

    projects = [
        {
            "title": "GT Reserve",
            "tech": ", ".join(["AWS", "Python", "Javascript", "ReactJS", "Selenium"]),
            "description": "Student-friendly alternative site to book study rooms at Georgia Tech. AWS Lambda fuctions run Selenium web automation scripts to update availabilities every 10 minutes and display them on a interactive dashboard powered by ReactJS.",
            "url": "https://gt-reserve.vercel.app/",
            "img_url": url_for("static", filename="img/projects/gt-reserve.png"),
            "github_url": "https://github.com/VigneshSK17/gt-reserve-scraper"
        },
        {
            "title": "Cubimer",
            "tech": ", ".join(["Dart", "Flutter", "Local Storage", "Cloudflare", "Git"]),
            "description": "An elegant and effective cubing timer that allows you to save your solve times locally on various different platforms, from web to desktop. Enabled by Flutter & Dart and utilizes cross-platform state management to store times. Hosted the web version of the app on Cloudflare Pages to ensure fast loading times and reliable access worldwide.",
            "url": "https://cubimer.pages.dev/#/",
            "img_url": url_for('static', filename='img/projects/cubimer.png'),
            "github_url": "https://github.com/VigneshSK17/cubimer"
        },
        {
            "title": "Personal Website",
            "description": "Engineered and deployed a sophisticated personal website that serves as a portfolio showcasing my software engineering abilities and web development expertise. Key features include interactive elements using DOM, CSS animations, and asynchronous JavaScript for real-time functionality. Integrated LinkedIn, GitHub, and Calendly for enhanced professional networking and scheduling.",
            "github_url": "https://jimmymishan.com/"
        },
        {
            "title": "Music Playlist Application",
            "description": "Created a Java application replicating streaming service operations with various features: Managed song sequences using circular linked lists for playlist navigation. Automated song library generation from CSV files for user-driven playlist customization. Implemented playlist manipulation capabilities, including merge, reverse, and shuffle functions, optimized by song popularity metrics to demonstrate intricate data structure utilization.",
            "github_url": "https://github.com/jimmyMsh/Data-Structures/tree/master/MusicPlaylist"
        }
    ]

    return render_template('projects.html', title="projects", active_page = 'projects', projects = projects)

@app.route('/contact')
def contact():
    return render_template('contact.html', title="Contact", active_page = 'contact')

@app.route('/timeline')
def timeline():
    return render_template('timeline.html', title='Timeline', active_page='timeline')


@app.route('/api/timeline_post')
def get_time_line_post():
    return {
        'timeline_posts':[
            model_to_dict(p)
            for p in
            TimelinePost.select().order_by(TimelinePost.created_at.desc())
        ]
    }

@app.route('/api/timeline_post', methods=['POST'])
def post_time_line_post():
    name = request.form['name']
    email = request.form['email']
    content = request.form['content']
    timeline_post = TimelinePost.create(name=name, email=email, content=content)

    return model_to_dict(timeline_post)

@app.route('/api/timeline_post/latest', methods=['DELETE'])
def delete_latest_time_line_post():
    latest_post = TimelinePost.select().order_by(TimelinePost.created_at.desc()).get()
    TimelinePost.delete_instance(latest_post)

    return model_to_dict(latest_post)


if __name__ == '__main__':
    app.run(debug=True)
