from app.app import app, db
from flask_login import login_required, current_user
from flask import render_template, flash, redirect, request, url_for, jsonify
from model.db import Menu, Event, Page, Booth, SessionRoom


@app.route('/eventee/menu/nav/<event_id>')
def EventNav(event_id):
    menus = Menu.query.filter(
        Menu.event_id == event_id, Menu.type == 'nav').order_by(Menu.id.desc()).all()
    return render_template('eventee/menu/nav.html', event_id=event_id, menus=menus)


@app.route('/eventee/menu/nav/create/<event_id>')
def CreateNav(event_id):
    pages = Page.query.filter_by(event_id=event_id).all()
    rooms = SessionRoom.query.filter_by(event_id=event_id).all()
    booths = Booth.query.filter_by(event_id=event_id).all()
    types = ['page',
             'session_room',
             'zoom',
             "booth",
             "vimeo",
             "pdf",
             "lobby",
             "back",
             "faq",
             "photobooth",
             "videosdk",
             "modal",
             "lounge",
             "SwagBag",
             "Leaderboard",
             "Schedule",
             "Library",
             "social_wall"]
    return render_template('eventee/menu/createnav.html', pages=pages, booths=booths, rooms=rooms, types=types, event_id=event_id)
