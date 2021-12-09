from app.app import app, db
from flask import jsonify, flash, request
from model.db import User, Event, UserLocation
from flask_login import current_user, login_required


@app.route('/events/delete', methods=["POST"])
@login_required
def EventDelete():
    event = Event.query.filter_by(id=request.form['id']).first()
    try:
        db.session.delete(event)
        db.session.commit()
        return jsonify({'code': 200, 'message': "Event Deleted Successfully"})
    except:
        return jsonify({'code': 500, 'message': "Something went wrong"})


@app.route('/events/OnlineChart', methods=['POST'])
def ChartJs():
    event = Event.query.filter_by(id=request.form['id']).first()
    online_user = User.query.filter_by(event_id=event.id, is_active=1).count()
    offline_user = User.query.filter_by(event_id=event.id, is_active=0).count()
    total = User.query.filter_by(event_id=event.id).count()
    userobj = {'online_user': online_user, 'offline_user': offline_user}
    return jsonify({'userobj': userobj, 'total': total})


@app.route('/events/sessionChart', methods=['POST'])
def SessionChartJs():
    event = Event.query.filter_by(id=request.form['id']).first()
    locations = UserLocation.query.filter_by(
        event_id=event.id, type="Sessionroom", current_status=1).all()
    locList = []
    for location in locations:
        counts = UserLocation.query.filter_by(
            type_location=location.type_location, current_status=1).count()
        locobj = {'room_name': location.type_location, 'room_count': counts}
        locList.append(locobj)

    return jsonify({'locations': locList})


@app.route('/events/pageChart', methods=['POST'])
def PageChart():
    event = Event.query.filter_by(id=request.form['id']).first()
    locations = UserLocation.query.filter_by(
        event_id=event.id, type="page", current_status=1).all()
    locList = []
    for location in locations:
        counts = UserLocation.query.filter_by(
            type_location=location.type_location, current_status=1).count()
        locobj = {'room_name': location.type_location,
                  'room_count': counts}
        locList.append(locobj)

    return jsonify({'locations': locList})


@app.route('/events/BoothChart', methods=['POST'])
def BoothChart():
    event = Event.query.filter_by(id=request.form['id']).first()
    locations = UserLocation.query.filter_by(
        event_id=event.id, type="page", current_status=1).all()
    locList = []
    for location in locations:
        counts = UserLocation.query.filter_by(
            type_location=location.type_location, current_status=1).count()
        locobj = {'room_name': location.type_location,
                  'room_count': counts}
        locList.append(locobj)

    return jsonify({'locations': locList})


@app.route('/events/LoungeUser', methods=['POST'])
def LoungeUser():
    event = Event.query.filter_by(id=request.form['id']).first()
    locations = UserLocation.query.filter_by(
        event_id=event.id, type="Lounge", current_status=1).all()
    locList = []
    for location in locations:
        counts = UserLocation.query.filter_by(
            type_location=location.type_location, current_status=1).count()
        locobj = {'room_name': "Lounge",
                  'room_count': counts}
        locList.append(locobj)

    return jsonify({'locations': locList})


@app.route('/events/Lobby', methods=['POST'])
def LobbyUser():
    event = Event.query.filter_by(id=request.form['id']).first()
    locations = UserLocation.query.filter_by(
        event_id=event.id, type="Lobby", current_status=1).all()
    locList = []
    for location in locations:
        counts = UserLocation.query.filter_by(
            type_location=location.type_location, current_status=1).count()
        locobj = {'room_name': "Lounge",
                  'room_count': counts}
        locList.append(locobj)

    return jsonify({'locations': locList})
