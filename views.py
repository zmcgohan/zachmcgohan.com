from mysite import app
from flask import render_template, request

from mysite.blog import blog_handler
from mysite.projects import projects_handler

@app.route("/")
def render_index():
    return render_template("about.html", page_title="About")

@app.route("/projects/", defaults={'page_num': 1})
@app.route("/projects/page/<int:page_num>")
def render_projects(page_num):
    """Renders the Projects page. Pulls project names, technologies and pictures from database file specified."""
    return projects_handler.handle_page_request(page_num)

### TODO BLOG STUFF -- GOING TO BE COMPLETELY REDONE MOST LIKELY ###
@app.route("/blog/post_source/<string:post_identifier>")
def render_blog_temp_post(post_identifier):
    return blog_handler.handle_temp_post_request(post_identifier)

@app.route("/blog/<string:post_identifier>")
def render_blog_post(post_identifier):
    return blog_handler.handle_post_request(post_identifier)

@app.route("/blog/", defaults={'page_id': 1})
@app.route("/blog/page/<int:page_id>")
def render_blog_index(page_id):
    return blog_handler.handle_page_request(page_id)

@app.route("/contact")
def render_contact():
    return render_template("contact.html", page_title="Contact")

@app.route("/hityler")
def render_hityler():
    return render_template("hityler.html")
