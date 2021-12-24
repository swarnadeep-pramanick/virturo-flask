from app.app import app, db
from flask_login import login_required, current_user
from flask import render_template, flash, redirect, request, url_for, jsonify
from model.db import User, Event


@app.route('/eventee/users/manage/<event_id>')
@login_required
def EventUser(event_id):
    event = Event.query.filter_by(id=event_id).first()
    users = User.query.filter_by(event_id=event.id)
    return render_template('eventee/users/index.html', event_id=event.id, users=users)


@app.route('/eventee/users/create/<event_id>')
@login_required
def EventUserCreate(event_id):
    event = Event.query.filter_by(id=event_id).first()
    return render_template('eventee/users/create.html', event_id=event.id)


@app.route('/eventee/user/store/<event_id>', methods=['POST'])
@login_required
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


@app.route('/eventee/user/delete', methods=['POST'])
@login_required
def UserDelete():
    user = User.query.filter_by(id=request.form['id']).first()
    db.session.delete(user)
    db.session.commit()
    usercount = User.query.filter_by(event_id=request.form['event_id']).count()
    return jsonify({'code': 200, 'message': "Event Deleted Successfully", 'userCount': usercount})


@app.route('/eventee/user/edit/<event_id>/<user_id>')
@login_required
def UserEdit(event_id, user_id):
    user = User.query.filter_by(id=user_id).first()
    return render_template('eventee/users/edit.html', user=user, event_id=event_id)


@app.route('/eventee/user/update/<event_id>/<user_id>', methods=['POST'])
@login_required
def UserUpdate(event_id, user_id):
    user = User.query.filter_by(id=user_id).first()
    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    if request.form['email']:
        user.email = request.form['email']

    user.type = request.form['type']
    db.session.commit()
    flash("User Updated Successfully")
    return redirect(url_for('EventUser', event_id=event_id))
