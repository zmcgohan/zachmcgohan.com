import sqlite3
import time
from flask import render_template
from mysite.blog import config

from mysite.blog import post_parsing

def get_view(post_id):
    """Returns the rendered template for the post with string identifier post_id."""
    db_connection = sqlite3.connect(config.DB_FILE)
    db_cursor = db_connection.cursor()
    # create page title
    page_title = "Blog | {}".format(post_id)
    # get post info
    post_info = get_post_info(db_cursor, post_id)
    # get adjacent posts' info
    adjacent_posts = get_adjacent_posts(db_cursor, post_info['id'])
    # close DB connection
    db_connection.close()
    styles = ['/static/stylesheets/blog/post_style.css', '/static/stylesheets/nav_bar_style.css']
    return render_template("blog/post.html", page_title=page_title, styles=styles, post_info=post_info, last_post=adjacent_posts['last'], next_post=adjacent_posts['next'])

def get_post_info(db_cursor, post_id):
    """Returns a dictionary of fields for the post with url_id post_id."""
    db_cursor.execute("SELECT * FROM posts WHERE url_id=?", (post_id,))
    db_result = db_cursor.fetchone()
    post_info = None
    if db_result:
        post_info = {
            'id': db_result[0],
            'url_id': db_result[1],
            'title': db_result[2],
            'content': post_parsing.html_parse(db_result[3]),
            'time_posted': time.strftime('%B %d, %Y', time.localtime(db_result[4])),
            'category': db_result[5]
            }
    else:
        post_info = None
    return post_info

def get_adjacent_posts(db_cursor, post_id):
    """Returns the post title/url_id info for the last/next posts from the post with id post_id."""
    adjacent_posts = { 'last': None, 'next': None }
    # get LAST post info
    db_cursor.execute("SELECT url_id, title FROM posts WHERE id=?", (post_id-1,))
    db_result = db_cursor.fetchone()
    if db_result:
        adjacent_posts['last'] = { 'url_id': db_result[0], 'title': db_result[1] }
    # get NEXT post info
    db_cursor.execute("SELECT url_id, title FROM posts WHERE id=?", (post_id+1,))
    db_result = db_cursor.fetchone()
    if db_result:
        adjacent_posts['next'] = { 'url_id': db_result[0], 'title': db_result[1] }
    return adjacent_posts
