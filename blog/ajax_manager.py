from flask import request
import sqlite3
from mysite.blog.config import DB_FILE

def get_response():
    '''The entry point of all blog manager AJAX requests. Passes off the requests to the appropriate other functions.'''
    request_type = request.form['request_type']
    if request_type == 'edit_post':
        return get_edit_response()
    elif request_type == 'hide_show_post':
        return get_hide_show_response()
    else:
        return "ERROR 404 - INVALID REQUEST TYPE"

def get_edit_response():
    '''Returns the response for an "edit_post" request.'''
    db_connection = sqlite3.connect(DB_FILE)
    db_cursor = db_connection.cursor()
    post_url_id = request.form['url_id']
    post_title = request.form['post_title']
    post_content = request.form['post_content']
    db_cursor.execute("UPDATE posts SET title=?, content=? WHERE url_id=?", (post_title, post_content, post_url_id))
    db_connection.commit()
    db_connection.close()
    if db_cursor.rowcount:
        return "UPDATE SUCCESSFUL"
    else:
        return "UPDATE ERROR"

def get_hide_show_response():
    '''Returns the response for a request to hide (set visibility = 0) a post.'''
    return_val = -1
    post_url_id = request.form['url_id']
    db_connection = sqlite3.connect(DB_FILE)
    db_cursor = db_connection.cursor()
    db_cursor.execute("SELECT visibility FROM posts WHERE url_id=?", (post_url_id,))
    results = db_cursor.fetchone()
    if results[0] == 1:
        db_cursor.execute("UPDATE posts SET visibility=0 WHERE url_id=?", (post_url_id,))
        return_val = 'POST HIDDEN'
    elif results[0] == 0:
        db_cursor.execute("UPDATE posts SET visibility=1 WHERE url_id=?", (post_url_id,))
        return_val = 'POST SHOWN'
    db_connection.commit()
    db_connection.close()
    return return_val
