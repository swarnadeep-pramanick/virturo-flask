from app.app import app, db
from flask_login import login_required, current_user
from flask import render_template, flash, redirect, request, url_for, jsonify
from model.db import User, Event, Faq


@app.route('/eventee/faq/<event_id>')
def EventFaq(event_id):
    faqs = Faq.query.filter_by(event_id=event_id).all()
    return render_template('eventee/faq/index.html', event_id=event_id, faqs=faqs)


@app.route('/eventee/faq/create/<event_id>')
def CreateFaq(event_id):
    return render_template('eventee/faq/create.html', event_id=event_id)


@app.route('/eventee/faq/store/<event_id>', methods=['POST'])
def StoreFaq(event_id):
    if request.method == 'POST':
        question = request.form['question']
        answer = request.form['answer']
        faq = Faq(question, answer, event_id)
        try:
            db.session.add_all([faq])
            db.session.commit()
            flash("Faq Added Successfully")
            return redirect(url_for('EventFaq', event_id=event_id))
        except:
            flash("Something Went Wrong")
            return redirect(url_for('EventFaq', event_id=event_id))


@app.route('/eventeefaq/edit/<event_id>/<faq_id>')
def EditFaq(event_id, faq_id):
    faq = Faq.query.filter_by(id=faq_id).first()
    return render_template('eventee/faq/edit.html', event_id=event_id, faq=faq)


@app.route('/eventee/faq/update/<event_id>/<faq_id>', methods=['POST'])
def UpdateFaq(event_id, faq_id):
    faq = faq = Faq.query.filter_by(id=faq_id).first()
    faq.question = request.form['question']
    faq.answer = request.form['answer']
    try:
        db.session.add(faq)
        db.session.commit()
        flash("Faq Updated Successfully")
        return redirect(url_for('EventFaq', event_id=event_id))
    except:
        flash("Something Went Wrong")
        return redirect(url_for('EventFaq', event_id=event_id))


@app.route('/eventee/faq/delete', methods=['POST'])
@login_required
def DeleteFaq():
    faq = Faq.query.filter_by(id=request.form['id']).first()
    db.session.delete(faq)
    db.session.commit()
    faqount = Faq.query.filter_by(event_id=request.form['event_id']).count()
    return jsonify({'code': 200, 'message': "Event Deleted Successfully", 'userCount': faqount})
