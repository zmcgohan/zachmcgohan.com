import sqlite3
import time
from flask import render_template
from mysite.blog import config

def get_view(post_id):
    """Returns the rendered template for the post with string identifier post_id."""
    # create page title
    page_title = "Blog | {}".format(post_id)
    # get post info
    post_info = get_post_info(post_id)
    styles = ['/static/stylesheets/blog/post_style.css']
    return render_template("blog/post.html", page_title=page_title, styles=styles, post_info=post_info)

def get_post_info(post_id):
    """Returns a dictionary of fields for the post with url_id post_id."""
    db_connection = sqlite3.connect(config.DB_FILE)
    db_cursor = db_connection.cursor()
    db_cursor.execute("SELECT * FROM posts WHERE url_id=?", (post_id,))
    db_result = db_cursor.fetchone()
    post_info = None
    if db_result:
        post_info = {
            'url_id': db_result[1],
            'title': db_result[2],
            'content': db_result[3],
            'time_posted': time.strftime('%B %d, %Y', time.localtime(db_result[4])),
            'category': db_result[5]
            }
    else:
        post_info = None
    db_connection.close()
    return post_info
