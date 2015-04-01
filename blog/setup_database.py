import sqlite3
import random
import time

from mysite.blog import config

TESTING = True

DB_FILE = config.DB_FILE

POSTS_TABLE_SQL = '''CREATE TABLE IF NOT EXISTS posts 
                    (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                    url_id TEXT NOT NULL UNIQUE, 
                    title TEXT, 
                    content TEXT, 
                    time_posted INTEGER, 
                    category INTEGER, 
                    visibility INTEGER)'''

COMMENTS_TABLE_SQL = '''CREATE TABLE IF NOT EXISTS comments 
                        (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                        post_id INTEGER, 
                        author TEXT, 
                        content TEXT, 
                        time_posted INTEGER, 
                        visibility INTEGER)'''

CATEGORIES_TABLE_SQL = '''CREATE TABLE IF NOT EXISTS categories 
                        (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                        name TEXT NOT NULL UNIQUE, 
                        color TEXT)'''

INITIAL_CATEGORIES = [ ('Personal', '00dfff'), ('Projects', '00ea04'), ('Programming', 'ff279f') ]

def create_test_posts(cursor):
    NUM_TEST_POSTS = 30
    sentences = [ 'This is a test sentence.', 'I\'m just trying to test out the blog system I\'m creating.', 
                    'I want to see how the layout looks and how everything fits together.',
                    'There has to be quite a few different sentences for it to look halfway decent.',
                    'But that\'s okay! I\'m just making sure it all works.', 'Just gotta keep on trucking with more sentences...' ]
    titles = [ 'Test Post', 'Project: zachmcgohan.com', 'How many posts does it take to test a site?' ]
    url_ids = [ 'test-post', 'project-zachmcgohan-com', 'how-many-posts-does-it-take-to-test-a-site' ]
    for i in xrange(NUM_TEST_POSTS):
        post_content = ''
        for j in xrange(5):
            post_content += '<p>'
            for k in xrange(random.randint(4,10)):
                post_content += random.choice(sentences) + ' '
            post_content += '</p>'
        rand_suffix = random.randint(1,10000)
        title_rand = random.randint(0,len(titles)-1)
        post_title = titles[title_rand]
        url_id = url_ids[title_rand] + '_{}'.format(rand_suffix)
        post_time = int(time.time())
        cursor.execute('''INSERT INTO posts (url_id, title, content, time_posted, category, visibility)
                        VALUES (?, ?, ?, ?, ?, ?)''', (url_id, post_title, post_content, post_time, random.randint(1,3), 1))

if __name__ == '__main__':
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # create tables
    cursor.execute(POSTS_TABLE_SQL)
    cursor.execute(COMMENTS_TABLE_SQL)
    cursor.execute(CATEGORIES_TABLE_SQL)

    # insert initial categories
    for category in INITIAL_CATEGORIES:
        cursor.execute("INSERT INTO categories (name, color) VALUES (?, ?)", category)

    if TESTING:
        create_test_posts(cursor)

    # commit changes, close connection
    conn.commit()
    conn.close()
