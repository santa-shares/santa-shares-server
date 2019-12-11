import logging, json, datetime
from flask import g, abort, request
from flask_restful import Resource
from endpoints import api
from extensions import db, auth
from models import UserItem, Item, UserLog

logger = logging.getLogger(__name__)

class Buy(Resource):

    @auth.login_required
    def post(self):
        if request.json is None: return abort(400, "No json payload provided.")
           
        item_id = request.json.get('item_id')
        if item_id is None: return abort(400, "An item must be specified to purchase.")
           
        item = Item.query.filter_by(id=item_id).first()
        if item is None: return abort(400, f"The provided id [{item_id}] does not match an item in the database.")
           
        purchase_amount = max(int(request.json.get('amount', 1)))
        if item.amount < purchase_amount: return abort(400, f"Not enough items for sale. Requested amount is [{purchase_amount}] yet stock is [{item.amount}].")
           
        item_price = item.get_current_price()
        purchase_cost = item_price * purchase_amount
        if purchase_cost > g.current_user.balance: abort(400, f"Not enough cash for purchase. You need [{purchase_cost}] when you have [{g.current_user.balance}]")

        try:
            user_item = next((user_item for user_item in g.current_user.items if user_item.item_id == item_id), None)
            if user_item is None:
                user_item = UserItem(user_id = g.current_user.id, item_id = item_id, amount = purchase_amount)
                db.session.add(user_item)
            else:
                user_item.amount += purchase_amount

            g.current_user.balance -= purchase_cost
            item.amount -= purchase_amount

            user_log = UserLog(user_id=g.current_user.id, item_id=item_id, amount=purchase_amount,buy_sell=True,datetime=datetime.datetime.now(),balance=g.current_user.balance)
            db.session.add(user_log)
            db.session.commit()
            return 200 
        
        except Exception as e:
            db.session.rollback()
            logger.exception(e)
            abort(500)

api.add_resource(Buy, "/buy")