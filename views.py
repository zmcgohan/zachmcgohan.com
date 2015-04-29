from mysite import app
from flask import render_template, request

from mysite.projects import projects_handler
from mysite import blog; from blog import *

@app.route("/")
def render_index():
    return render_template("about.html", page_title="About")

@app.route("/projects/", defaults={'page_num': 1})
@app.route("/projects/page/<int:page_num>")
def render_projects(page_num):
    """Renders the Projects page. Pulls project names, technologies and pictures from database file specified."""
    return projects_handler.handle_page_request(page_num)

# blog index
@app.route("/blog/", defaults={'page_num': 1})
@app.route("/blog/page/<int:page_num>")
def render_blog_index(page_num):
    return blog.index_view.get_view(page_num)

# blog manager's AJAX manager (for editing posts, getting drafts, hiding/showing posts, etc.)
@app.route("/blog/manage/ajax_manager", methods=['POST'])
def blog_manager_ajax_call():
    return blog.ajax_manager.get_response()

# log in to blog
@app.route("/blog/manage/verify", methods=['POST'])
def verify_blog_manager():
    return blog.manage_view.verify_manager()

# blog manager main page
@app.route("/blog/manage", defaults={'page_num': 1}, methods=['GET'])
@app.route("/blog/manage/page/<int:page_num>")
def render_blog_manage(page_num):
    return blog.manage_view.get_view(page_num)

# edit post
@app.route("/blog/manage/edit/<string:post_id>", methods=['GET', 'POST'])
def render_blog_edit_post(post_id):
    return blog.edit_post_view.get_view(post_id)

# blog post
@app.route("/blog/<string:post_id>")
def render_blog_post(post_id):
    return blog.post_view.get_view(post_id)

@app.route("/contact")
def render_contact():
    return render_template("contact.html", page_title="Contact")

@app.route("/hityler")
def render_hityler():
    return render_template("hityler.html")
