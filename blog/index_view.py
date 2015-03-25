from flask import render_template
import sqlite3
import re
from time import localtime, strftime
from math import ceil

from mysite.blog.config import DB_FILE
from mysite.blog.utils import strip_tags

NAV_HTML_TABS = 5 # tabs to be used for each row in navigation HTML
POSTS_PER_PAGE = 5 # max number of posts on index page

paragraph_finder = re.compile("<p>(.*)</p>")

def get_post_info(posts):
    """Fills a list with info about each post in posts to be sent to the template."""
    post_info = []
    for post in posts:
        temp_info = [] # [0] = title; [1] = image base URL; [2] = content; [3] = time posted; [4] = string identifier
        temp_info.append(post[4] if post[4] else "Title not found") 
        temp_info.append("/static/blog/{}/images/{}".format(post[1], post[5]) if post[5] else "/static/blog/image_not_found.jpg")
        desc = ""
        # TODO (if the site for some reason gets a reasonable amount of traffic): make this method more efficient.. 'cause it's not. At all.
        # adds words one by one until 120 words are added for content
        num_words = 0
        for paragraph in paragraph_finder.findall(post[6]):
            if num_words >= 120:
                break
            paragraph = strip_tags(paragraph)
            desc += "<p>"
            for word in paragraph.split():
                if num_words < 120:
                    desc += word + ' '
                    num_words += 1
                else:
                    desc = '{}... <a href="/blog/{}">Read full post</a>'.format(desc[:-1], post[1])
                    break
            desc += "</p>\n"
        temp_info.append(desc if desc else "<p>Content not found.</p>")
        temp_info.append(strftime("%B %d, %Y", localtime(post[2])))
        temp_info.append(post[1])
        post_info.append(temp_info)
    return post_info

def get_nav_html(page_id, total_pages):
    """Creates the HTML to be placed at the bottom of the page for links to other pages."""
    tab_str = '\t' * NAV_HTML_TABS
    nav_html = tab_str + '<a href="/blog/page/{0}" style="font-weight:500;color:#000000;">{0}</a>'.format(page_id)
    # adds a link back-and-forth, left-to-right, when it can (if it doesn't go over/under the page limits) until 5 page links total are met or it's determined no other page links can be added
    num_links_placed = 0
    for i in xrange(1, 5):
        if 0 < page_id + -1 * i:
            nav_html = tab_str + '<a href="/blog/page/{0}">{0}</a>\n'.format(page_id + -1 * i) + nav_html
            num_links_placed += 1
        if num_links_placed == 4: break
        if page_id + i <= total_pages:
            nav_html += '\n' + tab_str + '<a href="/blog/page/{0}">{0}</a>'.format(page_id + i)
            num_links_placed += 1
    nav_html += '\n' + tab_str + '<span style="float:right">'
    if page_id > 1:
        nav_html += '\n' + '\t' + tab_str + '<a href="/blog/page/1"><< First</a>'
        nav_html += '\n' + '\t' + tab_str + '<a href="/blog/page/{}">< Back</a>'.format(page_id - 1)
    if page_id < total_pages:
        nav_html += '\n' + '\t' + tab_str + '<a href="/blog/page/{}">Next ></a>'.format(page_id + 1)
        nav_html += '\n' + '\t' + tab_str + '<a href="/blog/page/{}">Last >></a>'.format(total_pages)
    nav_html += '\n' + tab_str + '</span>'
    return nav_html

def get_total_pages():
    """Gets total number of pages of posts in database."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    return int(ceil(len(cursor.execute("SELECT 1 FROM posts WHERE visible=1").fetchall()) / float(POSTS_PER_PAGE)))

def render(page_id):
    query_offset = (page_id - 1) * POSTS_PER_PAGE

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    posts = cursor.execute("SELECT * FROM posts WHERE visible=1 ORDER BY id DESC LIMIT ?, ?", (query_offset, POSTS_PER_PAGE)).fetchall()
    total_pages = get_total_pages()
    post_info = get_post_info(posts)
    nav_html = get_nav_html(page_id, total_pages)

    conn.close()

    return render_template("blog/blog_index.html", page_title="Blog", post_info=post_info, nav_html=nav_html, styles=["/static/blog/blog_index_style.css"])
