import routes
from app.app import app, db
from flask_migrate import Migrate  # To use model Migration
from routes import jsonresponse, userManange, faqManage, manuManage
Migrate(app, db)
if __name__ == '__main__':
    app.run()
