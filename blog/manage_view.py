from flask import render_template, request, make_response, redirect
import hashlib
import sqlite3
from mysite.blog.config import DB_FILE

PASSWORD_FILE = '/srv/www/mysite/blog_password.txt'
MD5_COOKIE_NAME = 'verified_md5'
MAX_COOKIE_AGE = 60*60*24*30 # one month
POSTS_PER_PAGE = 25

def get_view(page_num):
    """Renders the blog's manage page."""
    # set up DB stuff
    db_connection = sqlite3.connect(DB_FILE)
    db_cursor = db_connection.cursor()
    total_num_pages = get_total_num_posts(db_cursor) / POSTS_PER_PAGE + 1
    # make sure page num isn't invalid
    if page_num < 1: page_num = 1
    elif page_num > total_num_pages: page_num = total_num_pages
    # get vars for page
    posts = get_posts(db_cursor, page_num)
    page_title = "Blog Manager"
    user_verified = user_is_verified()
    wrong_pw_submission = request.args.get('err') == '1' # if user already submitted wrong password to form, then True; else False
    page_nums = get_page_nums(total_num_pages, page_num)
    styles = ['/static/stylesheets/nav_bar_style.css', '/static/stylesheets/blog/manage_style.css']
    scripts = [ '/static/scripts/jquery.js', '/static/blog/scripts/manage_scripts.js' ]
    db_connection.close()
    return render_template("blog/manage.html", page_title=page_title, styles=styles, scripts=scripts, user_verified=user_verified, wrong_pw_submission=wrong_pw_submission, posts=posts, page_nums=page_nums, cur_page=page_num)

def get_posts(db_cursor, page_num):
    """Gets the posts for the page specified by page_num."""
    posts = []
    db_cursor.execute("SELECT * FROM posts ORDER BY time_posted DESC LIMIT ?, ?", (POSTS_PER_PAGE*(page_num-1), POSTS_PER_PAGE))
    for post in db_cursor.fetchall():
        posts.append({
                'url_id': post[1],
                'title': post[2],
                'time_posted': post[4],
                'category': post[5],
                'visibility': post[6]
            })
    return posts

def user_is_verified():
    """Returns True if the user has the verified_md5 cookie set to the correct value, False otherwise."""
    stored_md5 = request.cookies.get(MD5_COOKIE_NAME)
    if not stored_md5: # no cookie, user can't be verified
        return False
    else: # has cookie, now see if it has the right value
        return stored_md5 == get_correct_pw_md5()

def verify_manager():
    # get md5 repr of correct password
    pw_md5 = get_correct_pw_md5()
    # get md5 of password form's content
    md5_input = hashlib.md5()
    md5_input.update(request.form['password'])
    md5_input = md5_input.hexdigest()
    if pw_md5 == md5_input:
        response = make_response(redirect("/blog/manage"))
        response.set_cookie(MD5_COOKIE_NAME, md5_input, max_age=MAX_COOKIE_AGE)
        return response
    else:
        response = make_response(redirect("/blog/manage?err=1"))
        return response

def get_correct_pw_md5():
    """Returns the md5 of the correct password for the blog, taken from PASSWORD_FILE."""
    f = open(PASSWORD_FILE, 'r')
    pw_md5 = f.read().strip()
    f.close()
    return pw_md5

# TODO implement cur_page functionality -- currently only returns ALL pages, not enough posts to matter
def get_page_nums(total_pages, cur_page):
    """Returns the page numbers relevant to current page's navbar."""
    return [x+1 for x in xrange(total_pages)]

def get_total_num_posts(db_cursor):
    db_cursor.execute("SELECT Count(*) FROM posts")
    return (db_cursor.fetchone())[0]
