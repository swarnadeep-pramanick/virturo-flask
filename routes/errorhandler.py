from app.app import login_manager
from flask import flash, redirect, url_for


# ##Error Handling
#
#


@login_manager.unauthorized_handler
def unauthorized():
    # do stuff
    flash("Unauthorized")
    return redirect(url_for('login'))
