from app.app import app, db
from flask_login import login_required, current_user
from flask import render_template, flash, redirect, request, url_for
from model.db import User, Event


@app.route('/users/manage/<event_id>')
@login_required
def EventUser(event_id):
    event = Event.query.filter_by(id=event_id).first()
    users = User.query.filter_by(event_id=event.id)
    return render_template('eventee/users/index.html', event_id=event.id, users=users)


@app.route('/users/create/<event_id>')
@login_required
def EventUserCreate(event_id):
    event = Event.query.filter_by(id=event_id).first()
    return render_template('eventee/users/create.html', event_id=event.id)


@app.route('/user/store/<event_id>',methods=['POST'])
def UserStore(event_id):
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    email = request.form['email']
    password = request.form['password']
    type = request.form['type']
    user = User(first_name, last_name, email, password, type, event_id)
    db.session.add_all([user])
    db.session.commit()
    flash("User Created Successfully")
    return redirect(url_for('EventUser', event_id=event_id))
