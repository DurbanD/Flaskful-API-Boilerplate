from init import app, db
import Routes.main

# Run Server
if __name__ == '__main__':
    with app.app_context():
        # db.drop_all()
        db.create_all()
        # createDefaultAdminAccount()
        app.run(debug=True)