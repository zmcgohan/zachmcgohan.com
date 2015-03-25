from mysite import app

STATIC_FOLDER = "static"

if __name__ == '__main__':
    app.static_folder = STATIC_FOLDER
    app.run(host="0.0.0.0", port=int("80"), debug=True)
