from app.app import app, db
from flask_migrate import Migrate  # To use model Migration
import routes
Migrate(app, db)
if __name__ == '__main__':
    app.run()
