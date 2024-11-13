from flask import render_template
from app import db

def register_error_handlers(app):
    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('errors/error.html', 
                             error_code=404,
                             error_description="The page you are looking for might have been removed, had its name changed, or is temporarily unavailable."), 404

    @app.errorhandler(403)
    def forbidden_error(error):
        return render_template('errors/error.html', 
                             error_code=403,
                             error_description="You don't have the required permissions to access this resource."), 403

    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()  # Roll back db session in case error occurred during db operation
        return render_template('errors/error.html', 
                             error_code=500,
                             error_description="The server encountered an internal error. Please try again later."), 500

    @app.errorhandler(401)
    def unauthorized_error(error):
        return render_template('errors/error.html', 
                             error_code=401,
                             error_description="Please log in to access this page."), 401
