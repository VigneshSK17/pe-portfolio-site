import os
from flask import Flask, render_template, request, url_for
from dotenv import load_dotenv

from peewee import *
from datetime import datetime
from playhouse.shortcuts import model_to_dict

load_dotenv()
app = Flask(__name__)

if os.getenv("TESTING") == "true":
    print("Running in test mode")
    mydb = SqliteDatabase('file::memory:?mode=memory&cache=shared', uri=True)
else:
    mydb = MySQLDatabase(os.getenv("MYSQL_DATABASE"),
              user=os.getenv("MYSQL_USER"),
              password=os.getenv("MYSQL_PASSWORD"),
              host=os.getenv("MYSQL_HOST"),
              port=3306)

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
            "role": "Production Engineer Intern",
            "company": "Meta & Major League Hacking",
            "description": "Gained valuable hands-on experience in Software Engineering (SWE) and Site Reliability Engineering (SRE) principles. Developed real-world projects under the guidance of Meta engineers and learned from industry experts through a comprehensive 12-week curriculum. Collaborated with a team of interns to build a robust portfolio, incorporating industry best practices and services.",
            "dates": "June 2024 - Present",
            "img_url": url_for('static', filename='img/work/mlh-fellowship.png')
        },
        {
            "role": "Machine Learning Research Intern",
            "company": "Fung Group",
            "description": "Implemented a variant of the SZ3 framework for data compression, achieving a 50x reduction with minimal error. Currently developing a Graph Neural Network for sub-second volumetric data compression with dimensionality reduction. Collaborated on designing cutting-edge ML models for quantum chemistry research.",
            "dates": "September 2023 - Present",
            "img_url": url_for('static', filename='img/work/fung-group.png')
        },
        {
            "role": "Robotics Engineer Intern",
            "company": "VIP - Automotive LIDAR",
            "description": "Led a team of 4 interns in migrating from ROS to ROS2, facilitating rewrites of custom dependencies. Successfully presented a technical proposal for the migration to senior engineers. Leveraged multi-threading capabilities of ROS2 to achieve a 4x improvement in path planning computations utilizing LIDAR data.",
            "dates": "August 2023 - Present",
            "img_url": url_for('static', filename='img/work/vip.png')
        },
        {
            "role": "Software Engineer Intern",
            "company": "System Technology Works",
            "description": "Designed and implemented over 10 functionalities for the robot, including grasping and a bipedal walking algorithm. Enhanced Zeus2Q's capabilities by integrating the NVIDIA Riva SDK for real-time conversational AI using industry-leading large language models (LLMs). Developed technical documentation for Zeus2Q's Python-based interfacing API through documentation videos.",
            "dates": "January 2023 - May 2023",
            "img_url": url_for('static', filename='img/work/stw.png')
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
            "title": "Unwrappd",
            "tech": ", ".join(["Java, Firebase, Firestore, Android, Java, Spotify API"]),
            "description": "Unwrappd allows users to generate and save their Spotify listening statistics throughout the year. The project utilized the Spotify API for data retrieval and Firebase for user authentication and cloud storage. Agile development methodologies, specifically Scrum, were employed to manage meetings, delegate tasks, and ensure efficient workflow within weekly sprints.",
            "url": "https://zghazanfar922.wixsite.com/unwrappd",
            "img_url": url_for('static', filename='img/projects/unwrappd.png'),
            "github_url": "https://github.com/VigneshSK17/unwrappd"
        },
        {
            "title": "CLI Shortener",
            "tech": ", ".join(["Rust, MySQL, SQLx, Axum"]),
            "description": "A highly efficient link shortening service capable of generating greater than 500 million unique shortened URLs. Ensures reliable storage of links by utilizing a local SQL database and interfacing with it using the SQLx library. Provides a user-friendly CLI to allow for multiple calls to the link shortening server simultaneously.",
            "url": "https://github.com/VigneshSK17/cli_shortener",
            "github_url": "https://github.com/VigneshSK17/cli_shortener"
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
    name = request.form.get('name')
    email = request.form.get('email')
    content = request.form.get('content')
    
    if not name:
        return {'error': 'Invalid name'}, 400
    if not content:
        return {'error': 'Invalid content'}, 400
    if '@' not in email or '.' not in email:
        return {'error': 'Invalid email'}, 400
    try:
        timeline_post = TimelinePost.create(name=name, email=email, content=content)
        return model_to_dict(timeline_post), 201
    except Exception as e:
        return {'error': str(e)}, 500


@app.route('/api/timeline_post/latest', methods=['DELETE'])
def delete_latest_time_line_post():
    latest_post = TimelinePost.select().order_by(TimelinePost.created_at.desc()).get()
    TimelinePost.delete_instance(latest_post)

    return model_to_dict(latest_post)


if __name__ == '__main__':
    app.run(debug=True)
