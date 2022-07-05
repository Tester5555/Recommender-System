from flask import Flask, redirect, url_for, render_template, request, session, flash
from datetime import timedelta
import json, requests


app = Flask(__name__)
app.secret_key = 'hello'
app.permanent_session_lifetime = timedelta(days=5)

@app.route('/')
def home():
	return render_template('home.html')

@app.route('/recommendCourses', methods=["POST", "GET"])
def recommCourses():
	if request.method == 'POST':
		session.permanent = True
		skills = request.form['skills']
		
		return redirect(url_for('courses', skills=skills))
	else: 
		return render_template('recommCourses.html')

@app.route('/courses/<skills>')
def courses(skills):
	msg = 'Coursera provides the following courses related to "' + skills + '" :'
	s_list = list(map(str.strip, skills.split(',')))

	for skill in s_list:
		url_coursera = 'https://api.coursera.org/api/courses.v1?q=search&query=' + skill
		courses_list = listcourses(url_coursera, skill)
		
	return  render_template('courses.html', msg=msg, courses_list=courses_list)

def listcourses(url, skill):
	res = requests.get(url)
	courses = json.loads(res.text)
	courses_list = []
	
	for course in courses['elements']:
		course_name = course['name']
		course_url = 'https://www.coursera.org/learn/' + course['slug']
		course_dic = {'name': course_name, 'url': course_url}
		courses_list.append(course_dic)
		
	return courses_list

if __name__ == '__main__':
	app.run(debug=True)