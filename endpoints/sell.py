import logging
from flask import request, g, abort
from flask_restful import Resource
from extensions import auth, db
from endpoints import api

logger = logging.getLogger(__name__)

class Sell(Resource):
    @auth.login_required
    def post(self):
        if request.json is None: abort(400, "No json payload provided.")

        item_id = request.json.get("item_id", None)
        if item_id is None: abort(400, "No item_id provided. You must provide an item_id to sell.")

        user_item = next((user_item for user_item in g.current_user.items if user_item.item_id == item_id), None)
        if user_item is None: abort(400, f"You don't own any items with id [{item_id}]") 

        sell_amount = request.json.get("amount", 1)
        if sell_amount > user_item.amount: abort(400, f"You don't have [{sell_amount}] of item [{user_item.item.name}] to sell. You have [{user_item.amount}] in stock.")

        transaction_fee_per_item = 0
        transaction_fee = transaction_fee_per_item * sell_amount
        item_price = user_item.item.get_current_price()
        sell_price = sell_amount * item_price
        if g.current_user.balance + sell_price < transaction_fee: abort(400, f"You cannot afford the transaction fee for this sale. The fee is [{transaction_fee}] and you will have [{g.current_user.balance + sell_price}] after sale.")

        try:
            g.current_user.balance += sell_price - transaction_fee
            user_item.item.amount += sell_amount
            user_item.amount -= sell_amount
            if user_item.amount == 0:
                db.session.remove(user_item)
            db.session.commit()
            return 200

        except Exception as e:
            db.session.rollback()
            logger.error(e)
            abort(500)

api.add_resource(Sell, "/sell")