from controllers.app_controller import create_app
from utils.create_db import create_db  # Optional, only if you're using this

if __name__ == "__main__":
    app = create_app()

    # Uncomment this line if you want to initialize the DB schema
    # create_db(app)

    # Start the Flask server with logs and auto-reload
    app.run(host='127.0.0.1', port=8080, debug=True)
