from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        "price",
        type=float,
        required=True,
        help="This field cannot be left blank"
    )
    parser.add_argument(
        "store_id",
        type=int,
        required=True,
        help="Every item needs a store id"
    )

    @jwt_required()  # calls the identity function before the request
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {"message": "Item '{}' not found".format(name)}

    def post(self, name):
        if(ItemModel.find_by_name(name)):
            return {"message": "An item with name '{}' already exists".format(name)}, 400

        data = self.parser.parse_args()

        item = ItemModel(name,**data)

        try:
            item.save_to_db()
        except:
            # internal server error
            return {"message": "An error occured while inserting '{}'".format(item.name)}, 500

        return item.json(), 201  # "created" http code, note: 202 stands for accepted, a delayed creation

    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()

        return {"message": "Item deleted"}
        
    def put(self, name):
        # this way, anything other than price is diregarded and not included in the data variable
        data = self.parser.parse_args()

        item = ItemModel.find_by_name(name)
        
        if item is None:
            item = ItemModel(name, **data)
        else:
            item.price = data["price"]

        item.save_to_db()

        return item.json(), 200



class ItemList(Resource):
    def get(self):
        #using list comprehension
        return {"item": 
            [
                item.json() for item in ItemModel.query.all()
            ]
        }
        #or using lambda functions
        # return {"item": 
        #     list(map(lambda x: x.json(), ItemModel.query.all()))
        # }

