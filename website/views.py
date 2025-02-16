from flask import Blueprint, render_template, request, flash, jsonify,redirect,url_for
from flask_login import login_required, current_user
from .models import Note
from . import db,getcurrentprice,addtoqueue,getcurrentprice
import json
from .price import price as current_price

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        note = request.form.get('note')

        if len(note) < 1:
            flash('Note is too short!', category='error')
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added!', category='success')

    return render_template("home.html", user=current_user)


@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})

@login_required
@views.route('/shop')
def shop():
    user = current_user
    return render_template('shopex.html',user = current_user)

@views.route('/shop-robuxbuy')
@login_required
def shop_extend():
    user = current_user
    current_price = getcurrentprice()
    if user.balance == current_price or user.balance > current_price:
        addtoqueue(user.id)
        return redirect(url_for('views.home')),flash('Order placed',category='success')
    else:
        return redirect(url_for('views.home')),flash('Insuffucient balance',category='error') 
    
@views.route('/pricing')
@login_required
def pricing_handler():
    return render_template('pricing.html',user=current_user)
        
        