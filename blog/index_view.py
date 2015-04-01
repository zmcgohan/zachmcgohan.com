"""Handles requests to /blog and /blog/page/*"""

import sqlite3
import time
from flask import render_template
from mysite.blog import config
from math import ceil

POSTS_PER_PAGE = 5
TOTAL_PAGE_LINKS = 5

def get_view(page_num):
    """Returns the rendered template."""
    total_pages = get_total_pages(0) # get total number of pages available
    # make sure page_num is in range
    if page_num < 1: page_num = 1
    elif page_num > total_pages: page_num = total_pages
    # create page title
    page_title = "Blog"
    if page_num > 1: page_title += ' | Page {}'.format(page_num)
    # get page nums for links
    link_pages = get_nav_bar_pages(page_num, total_pages)
    # get posts
    # TODO make categories work
    posts = get_posts(0, page_num)
    styles = ['/static/stylesheets/blog/index_style.css']
    return render_template("blog/index.html", page_title=page_title, styles=styles, posts=posts, cur_page=page_num, total_pages=total_pages, link_pages=link_pages)

def get_posts(category, page_num):
    """Returns a list of posts on the specified page_num in the specified category."""
    posts = []
    db_connection = sqlite3.connect(config.DB_FILE)
    db_cursor = db_connection.cursor()
    if category:
        db_cursor.execute("SELECT * FROM posts WHERE category=? AND visibility=1 ORDER BY time_posted DESC LIMIT ?, ?", (str(category), str(POSTS_PER_PAGE*(page_num-1)), str(POSTS_PER_PAGE)))
    else:
        db_cursor.execute("SELECT * FROM posts WHERE visibility=1 ORDER BY time_posted DESC LIMIT ?, ?", (str(POSTS_PER_PAGE*(page_num-1)), str(POSTS_PER_PAGE)))
    for post in db_cursor.fetchall(): # create a dict for each post -- makes it easier to deal with
        posts.append({
            'url_id': post[1],
            'title': post[2],
            'content': post[3],
            'time_posted': time.strftime('%B %d, %Y', time.localtime(post[4])),
            'category': post[5]
            })
    db_connection.close()
    return posts

def get_total_pages(category):
    """Returns the total number of pages of blog posts for a given category."""
    db_connection = sqlite3.connect(config.DB_FILE)
    db_cursor = db_connection.cursor()
    if category:
        db_cursor.execute("SELECT id FROM posts WHERE category=? AND visibility=1", (str(category),))
    else:
        db_cursor.execute("SELECT id FROM posts WHERE visibility=1")
    records = db_cursor.fetchall()
    db_connection.close()
    return int(ceil(len(records) / float(POSTS_PER_PAGE)))

def get_nav_bar_pages(page_num, total_pages):
    """Returns the HTML for page links, determined by the current page (page_num) and the total number of pages available (total_pages)."""
    pages = [page_num]
    for i in xrange(1,TOTAL_PAGE_LINKS):
        if page_num-i >= 1 and len(pages) < TOTAL_PAGE_LINKS:
            pages.insert(0, page_num-i)
        if page_num+i <= total_pages and len(pages) < TOTAL_PAGE_LINKS:
            pages.append(page_num+i)
    return pages
