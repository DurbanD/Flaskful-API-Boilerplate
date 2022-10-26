from init import app, db
import Routes.main
from Tools.defaultAdmin import create

# Run Server
if __name__ == '__main__':
    with app.app_context():
        # db.drop_all()
        db.create_all()
        # create()
        app.run(host="0.0.0.0", port=5000, debug=False)