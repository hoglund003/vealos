# Elias og Kaseper
from datetime import date, datetime
from flask import Blueprint
from flask import flash
from flask import g
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from werkzeug.exceptions import abort
from flask import current_app
from application.db import get_db

bp = Blueprint("user", __name__)

@bp.route("/user/<int:userId>")
@bp.route("/user/")
def index(userId=-1):  
    userId = str(userId)
    db = get_db()

    try:
        # Fetching user, if it exists.
        user = db.execute('SELECT * FROM users WHERE id = ?', (userId)).fetchone()
    except:
        return redirect(url_for('index.index'))
    tours = db.execute('SELECT * FROM tours WHERE user_id = ?', (userId)).fetchall()

    totalTours = 0
    toursThisYear = 0
    for tour in tours:
        totalTours += 1

        tourYear = datetime.strftime(tour['tour_date'], '%Y')
        currentYear = str(datetime.now().year)
        if tourYear == currentYear:
            toursThisYear += 1
    
    return render_template("user/user.html", **locals())

@bp.route("/edit-user/<int:userId>")
def edit(userId=-1):
    userId = str(userId)
    db = get_db()

    # Add validation here -->
    
    try:
        user = db.execute('SELECT * FROM users WHERE id = ?', (userId)).fetchone()
    except:
        return redirect('/')

    return render_template("user/edit-user.html", **locals())

@bp.route("/update-user/<int:userId>", methods=["POST"])
def update(userId):
    userId = str(userId)
    db = get_db()
    
    # And here -->

    updatedUsername = request.form['updated_username']
    updatedEmail = request.form['updated_email']
    updatedVisible =request.form.get('updated_visible')
    if not updatedVisible: # updateVisible can be none
        updatedVisible = 0

    db.execute('''
        UPDATE users 
        SET username = ?, 
        email = ?,
        visible = ? 
        WHERE id = ?
        ''',
        (updatedUsername, updatedEmail, updatedVisible, userId)
    )
    db.commit()

    return redirect(url_for('user.index', userId=userId))
