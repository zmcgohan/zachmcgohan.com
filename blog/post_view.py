from flask import render_template
from mysite.blog.config import DB_FILE
import sqlite3

def get_nav_html(post_id):
    """Gets the next/last post links' HTML if they exist."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    nav_html = '<span id="left_link">\n'
    query = cursor.execute("SELECT * FROM posts WHERE id=? AND visible=1", (post_id - 1,))
    result = query.fetchone()
    if result is not None:
        nav_html += "<a href=\"/blog/{}\">< {}</a>\n".format(result[1], result[4])
    nav_html += "</span>\n"

    nav_html += '<span id="right_link">\n'
    query = cursor.execute("SELECT * FROM posts WHERE id=? AND visible=1", (post_id + 1,))
    result = query.fetchone()
    if result is not None:
        nav_html += "<a href=\"/blog/{}\">{} ></a>\n".format(result[1], result[4])
    nav_html += "</span>\n"

    conn.close()

    return nav_html

def render(post_identifier):
    """Returns the rendered template for a post."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    query = cursor.execute("SELECT * FROM posts WHERE string_identifier=?", (post_identifier,))
    post_info = query.fetchone()

    conn.close()

    post_title = post_info[4]
    post_image = post_info[5]
    post_content = post_info[6]

    if post_info is not None:
        nav_html = get_nav_html(post_info[0])
        return render_template("blog/blog_post.html", styles=["/static/blog/blog_post_style.css"], page_title="Blog | {}".format(post_title), post_identifier=post_identifier,
                post_title=post_title, post_image=post_image, post_content = post_content, nav_html=nav_html)
    else:
        return "Error: Post '{}' not found".format(post_identifier)
