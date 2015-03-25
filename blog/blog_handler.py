from flask import render_template
from mysite.blog import index_view, post_view

def handle_page_request(page_id):
    total_pages = index_view.get_total_pages()
    if page_id < 1: page_id = 1
    elif page_id > total_pages: page_id = total_pages
    return index_view.render(page_id)

def handle_post_request(post_identifier):
    return post_view.render(post_identifier)

def handle_temp_post_request(post_identifier):
    post_title = None
    content = ""
    try:
        with open("/srv/www/mysite/venv/mysite/blog/posts/{}/content.html".format(post_identifier)) as f:
            post_title = f.next()[:-1]
            for line in f:
                content += line
    except Exception as e:
        return "<p>Could not open post files.</p><p>Error message: {}</p>".format(str(e))

    return render_template("blog/blog_post.html", page_title="Blog | {}".format(post_title), post_content=content)
