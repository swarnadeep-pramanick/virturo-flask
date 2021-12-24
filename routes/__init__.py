from app.app import app, login_manager, db
from flask import render_template, Response, request, url_for, flash, jsonify
from forms import LoginForm, RegistrationForm
from flask import request, redirect, session
from flask_login import login_required, login_user, current_user, logout_user
from datetime import datetime, timedelta, date
import routes.errorhandler

from model.db import User, Event, Menu, Content
from helper import is_live
from sqlalchemy import text
#Routing


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    else:
        return redirect(url_for('login'))
#####################
####AUTH#############
#####################


@app.route('/login')
def login():
    form = LoginForm(request.form)
    return render_template('users/login.html', form=form)


@app.route('/confirm_login', methods=['POST'])
def confirm_login():
    if request.method == "POST":
        form = LoginForm(request.form)
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            if user and user.checkpassword(form.password.data):
                user.is_active = True
                # user.commit()
                login_user(user)
                next = request.args.get('next')
                session['first_name'] = user.first_name
                session['user_id'] = user.id
                return redirect(url_for('dashboard'))
            else:
                flash("No User Found")
                return redirect(url_for('login'))


@app.route('/register')
def register():
    form = RegistrationForm(request.form)
    return render_template('users/register.html', form=form)


@app.route('/confirm_register', methods=['POST'])
def confirm_register():
    if request.method == "POST":
        form = RegistrationForm(request.form)
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            if not user:
                user = User(form.first_name.data, form.last_name.data,
                            form.email.data, form.password.data, 1)
                db.session.add_all([user])
                db.session.commit()
                flash("New User Added Successfully")
                return redirect(url_for("login"))
            else:
                flash("Same Email Address Already Exist")
                return redirect(url_for('register'))


@app.route('/logout')
@login_required
def Logout():
    is_live(current_user.id, 0)
    logout_user()
    return redirect(url_for('login'))

###############################
####Eventee Dashboard#########
##############################


@app.route('/dashboard')
@login_required
def dashboard():
    user = load_user(current_user.id)
    set_live = is_live(current_user.id, 1)
    year = datetime.today().strftime('%Y')
    events = Event.query.filter_by(user_id=current_user.id).count()
    today = date.today()

    liveEvent = Event.query.filter(
        Event.end_date >= today).filter(Event.user_id == current_user.id).count()
    result = text(
        f"SELECT * FROM events where user_id ={current_user.id} and date(created_at) = '{date.today()}' ")

    rec = db.engine.execute(result)

    recent = [row[2] for row in rec]

    todayEvent = Event.query.filter(
        Event.start_date == today, Event.user_id == user.id).count()
    ending_event_today = Event.query.filter(
        Event.end_date == today, Event.user_id == current_user.id).limit(5).all()
    # live_user = Event.query.filter_by(id=user.id).all()
    # userall = User.query.all()
    # print(userall)
    # date = datetime.today().strftime('%Y-%m-%d')
    # return Response(liveEvent)
    return render_template('dashboard.html', events=events, liveEvent=liveEvent, todayEvent=todayEvent, ending_event_today=ending_event_today, year=year, user=user, recent=recent)

#Event Index


@app.route('/events')
@login_required
def Eventlist():
    events = Event.query.filter_by(user_id=current_user.id).order_by(
        Event.created_at.desc()).all()
    current_date = datetime.today().strftime('%Y-%m-%d')
    return render_template('eventee/event/index.html', events=events, current_date=current_date)


@app.route('/events/create', methods=['POST'])
@login_required
def EventCreate():

    if request.method == 'POST':
        event_name = request.form['name']
        event_slug = request.form['event_slug']
        start_date = request.form['start_date']
        end_date = request.form['end_date']
        link = f"{event_slug}.localhost:5000"
        existEve = Event.query.filter_by(slug=event_slug).first()
        menus = ['lobby', 'schedule', 'lounge', 'library',
                 'swagbag', 'leaderboard', 'personalagenda']
        iclasses = ['fa fa-home', 'fe-calendar', 'fe-home',
                    'fe-folder', 'fe-shopping-bag', 'fe-bar-chart', 'fe-home']
        fields = ['login_background', 'lobby_background',
                  'exterior_background_image', 'exterior_background_video', 'favicon', 'logo']
        type_flieds = ['image', 'image', 'image', 'video', 'image', 'image']
        if not existEve:
            event = Event(event_name, event_slug, current_user.id,
                          link, start_date, end_date)

            db.session.add_all([event])
            db.session.commit()
            try:
                i = 1
                for names, iclass in zip(menus, iclasses):
                    menu = Menu(name=names, parent_id=0,
                                event_id=event.id, position=i, link='perm', iClass=iclass, type='nav')
                    db.session.add(menu)
                    db.session.commit()
                for fieldlist, typelist in zip(fields, type_flieds):
                    content = Content(field=fieldlist, type=typelist)
                    db.session.add(content)
                    db.session.commit()

            except:
                Event.query.filter_by(id=event.id).delete()
                flash('Something Went Wrong')
                return redirect(url_for('Eventlist'))
            flash("Event Created Successfully")
            return redirect(url_for('Eventlist'))
        else:
            flash("Same Event Already Exist")
            return redirect(url_for('EventCreate'))


@app.route('/events/edit/<event_id>')
@login_required
def EventEdit(event_id):
    event = Event.query.filter_by(id=event_id).first()
    return render_template('eventee/event/edit.html', event=event)


@app.route('/events/update/<event_id>', methods=['POST'])
@login_required
def EventUpdate(event_id):

    if request.method == 'POST':
        event = Event.query.filter_by(id=event_id).first()
        event.name = request.form['name']
        event.slug = request.form['event_slug']
        event.start_date = request.form['start_date']
        event.end_date = request.form['end_date']
        event.link = f"{request.form['event_slug']}.localhost:5000"
        db.session.commit()
        flash("Event Updated Successfully")
        return redirect(url_for('Eventlist'))


###########################
##Event Dashboard#########
##########################
@app.route('/events/manage/<event_id>')
@login_required
def EventDashboard(event_id):
    event = Event.query.filter_by(id=event_id).first()
    if event:
        session['event_name'] = event.name
    return render_template('eventee/dashboard.html', event_id=event_id)
