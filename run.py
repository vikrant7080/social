from app import create_app

flask_app = create_app()

"""
Initialize the app by importing the app object from the app.py to avoid circular
Imports.
"""
if __name__ == '__main__':
    flask_app.run(host='0.0.0.0', debug=True)
