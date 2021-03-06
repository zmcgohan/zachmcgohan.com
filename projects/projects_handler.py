from flask import render_template
import sqlite3

### Projects table info ###
#0|id|INTEGER|0||1
#1|title|TEXT|0||0
#2|technologies|TEXT|0||0
#3|image|TEXT|0||0
#4|link|TEXT|0||0
#5|importance|INTEGER|0||0

PROJECTS_DB_FILE = '/srv/www/mysite/venv/mysite/projects/projects.db'
PROJECTS_PER_PAGE = 9 # number of projects on each page

### TODO ###
# Make awesome JavaScript additions to page. (Like screen size-adjusted scrolling display box for projects and possibly blog posts.
# ^^^ Could be added to front page -- hybrid of responseive design types
############

def handle_page_request(page_num):
    """Returns project #(PROJECTS_PER_PAGE*(page_num-1)+1) through project #(PROJECTS_PER_PAGE*(page_num-1)+PROJECTS_PER_PAGE) from PROJECTS_DB_FILE, ordered by importance."""
    # create DB stuff to pass into funcs
    db_connection = sqlite3.connect(PROJECTS_DB_FILE)
    db_cursor = db_connection.cursor()
    # get total number of pages
    total_num_pages = (db_cursor.execute("SELECT Count(*) FROM projects").fetchone())[0] / PROJECTS_PER_PAGE + 1
    # make sure page_num is valid -- if not, correct it
    if page_num < 1: page_num = 1
    elif page_num > total_num_pages: page_num = total_num_pages
    # get projects into list for Jinja2 and navbar string (nav_html)
    project_list = get_projects_on_page(db_cursor, page_num)
    nav_page_nums = get_nav_page_nums(db_cursor, page_num, total_num_pages)
    # close DB connection
    db_connection.close()
    # return rendered page
    styles = ['/static/stylesheets/projects_style.css', '/static/stylesheets/nav_bar_style.css']
    cur_page = page_num
    return render_template("projects.html", projects=project_list, page_title="Projects", styles=styles, cur_page=cur_page, nav_page_nums=nav_page_nums)

def get_projects_on_page(db_cursor, page_num):
    """Returns a list of the projects on page #page_num."""
    db_cursor.execute("SELECT * FROM projects ORDER BY importance DESC LIMIT ?, ?", (PROJECTS_PER_PAGE*(page_num-1), PROJECTS_PER_PAGE))
    project_list = []
    for project_record in db_cursor.fetchall():
        project_list.append({ 'title': project_record[1], 'technologies': project_record[2], 'image': project_record[3], 
                                'link': project_record[4] })
    return project_list

def get_nav_page_nums(db_cursor, current_page, total_num_pages):
    """Returns a list of page numbers to be linked to in the nav bar."""
    total_pages = (db_cursor.execute("SELECT Count(*) FROM projects").fetchone())[0] / PROJECTS_PER_PAGE + 1
    pages = []
    for i in xrange(1, total_pages+1):
        pages.append(i)
    return pages

def create_database():
    """Creates the database file PROJECTS_DB_FILE and sets up the `projects` table."""
    db_connection = sqlite3.connect(PROJECTS_DB_FILE)
    db_cursor = db_connection.cursor()
    db_cursor.execute("CREATE TABLE IF NOT EXISTS projects (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, technologies TEXT, image TEXT, link TEXT, importance INTEGER)")
    db_connection.close()
