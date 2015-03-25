import sqlite3

NUM_RECORDS = 23

if __name__ == '__main__':
    conn = sqlite3.connect('projects.db')
    cursor = conn.cursor()
    for i in xrange(NUM_RECORDS):
        cursor.execute("INSERT INTO projects (title, technologies, image, link, importance) VALUES (?, ?, ?, ?, ?)", 
                            ("{} - zachmcgohan.com".format(i), "CSS3, HTML5, Python (+Flask), JavaScript (+JQuery)", "/static/images/screenshot.jpg", "/", i))
    conn.commit()
    conn.close()
