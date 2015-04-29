from flask import render_template, request
import sqlite3
from mysite.blog.config import DB_FILE

def get_view(post_id):
    """Returns the page for editing a blog post."""
    # create DB connection
    db_connection = sqlite3.connect(DB_FILE)
    db_cursor = db_connection.cursor()
    post_info = get_post_info(db_cursor, post_id)
    # close DB connection
    db_connection.close()
    page_title = "Blog Manager | Edit Post"
    styles = [ '/static/stylesheets/blog/edit_post_style.css' ]
    scripts = [ '/static/scripts/jquery.js', '/static/blog/scripts/edit_post_scripts.js' ]
    return render_template("blog/edit_post.html", page_title=page_title, styles=styles, scripts=scripts, post_info=post_info)

def get_post_info(cursor, post_id):
    """Returns post info for the blog post with url_id post_id."""
    post_info = None
    cursor.execute("SELECT * FROM posts WHERE url_id=?", (post_id,))
    results = cursor.fetchone()
    if results:
        post_info = {
            'url_id': results[1],
            'title': results[2],
            'content': results[3],
            'time_posted': results[4],
            'category': results[5],
            'visibility': results[6]
            }
    return post_info
