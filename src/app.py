import json
from flask import Flask, request
import dao
from db import db

app = Flask(__name__)
db_filename = "haystack.db"

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///%s" % db_filename
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True

db.init_app(app)
with app.app_context():
    db.create_all()

def success_response(data, code=200):
    return json.dumps({"success": True, "data": data}), code

def failure_response(message, code=404):
    return json.dumps({"success": False, "error": message}), code

@app.route("/")
def test():
    return "Hello World!", 200

@app.route('/api/users/create/', methods=['POST'])
def create_user():
    body = json.loads(request.data)
    user = dao.create_user(
        external_id=body.get('external_id'),
        display_name=body.get('display_name'),
        avatar_url=body.get('avatar_url')
    )
    return success_response(user, 201)

@app.route('/api/users/<string:external_id>/update/notification_id/', methods=['PUT'])
def update_notification_id(external_id):
    body = json.loads(request.data)
    updated_user = dao.update_user_notif_token(
        external_id=external_id,
        notification_token=body.get('notification_token')
    )
    return success_response(updated_user)

# @app.route('/api/users/<string:external_id>/username/update/', methods=['PUT'])
# def update_snapchat_username(external_id):
#     body = json.loads(request.data)
#     user_id = dao.get_userid_by_externalid(
#         external_id=external_id
#     )
#     updated_user_info = dao.update_snapchat_username(
#         user_id=user_id,
#         username=body.get('snapchat_username')
#     )

    return success_response(updated_user_info)

@app.route('/api/users/<string:external_id>/listings/create/', methods=['POST'])
def create_listing(external_id):
    body = json.loads(request.data)
    user_id = dao.get_userid_by_externalid(
        external_id=external_id
    )
    avatar_url = dao.get_avatarurl_by_userid(user_id)
    listing = dao.create_listing(
        user_id=user_id,
        product_image_url=body.get('product_image_url'),
        avatar_url=avatar_url,
        title=body.get('title'),
        description=body.get('description'),
        condition=body.get('condition'),
        price=body.get('price')
    )
    return success_response(listing, 201)

@app.route('/api/users/<string:external_id>/listings/')
def get_my_listings(external_id):
    # body = json.loads(request.data)
    user_id = dao.get_userid_by_externalid(
        external_id=external_id
    )
    my_listings = dao.get_listings_by_userid(user_id)

    return success_response(my_listings)

@app.route('/api/users/<string:external_id>/listings/page/<int:page_number>/')
def get_paginated_listings(external_id, page_number):
    # body = json.loads(request.data)
    user_id = dao.get_userid_by_externalid(
        external_id=external_id
    )
    listings = dao.get_paginated_listings(
        user_id=user_id,
        page_number=page_number
    )

    return success_response(listings)

@app.route('/api/users/GUEST/listings/page/<int:page_number>/')
def get_paginated_listings_guest(page_number):
    listings = dao.get_paginated_listings_guest(page_number)
    return success_response(listings)


@app.route('/api/listings/<string:listing_id>/delete/', methods=['DELETE'])
def delete_listing(listing_id):
    # body = json.loads(request.data)
    deleted_listing = dao.delete_listing(
        listing_id=listing_id
    )

    return success_response(deleted_listing)

@app.route('/api/listings/<string:listing_id>/views/increment/', methods=['PUT'])
def increment_listing_views(listing_id):
    listing = dao.increment_listing_views(listing_id)
    return success_response(listing)

@app.route('/api/listings/<string:listing_id>/status/sold/', methods=['PUT'])
def listing_status_sold(listing_id):
    listing = dao.listing_status_sold(listing_id)
    return success_response(listing)

@app.route('/api/listings/<string:listing_id>/update/', methods=['PUT'])
def update_listing_info(listing_id):
    body = json.loads(request.data)
    updated_listing = dao.update_listing_info(
        listing_id=listing_id,
        price=body.get('price'),
        title=body.get('title'),
        description=body.get('description'),
        condition=body.get('condition')
    )
    return success_response(updated_listing)


@app.route('/api/reports/create/', methods=['POST'])
def create_report():
    body = json.loads(request.data)
    report = dao.create_report(
        report=body.get('report'),
        listing_id=body.get('listing_id')
    )
    # if report is None:
    #     return failure_response("Listing has been removed for too many reports")

    return success_response(report, 201)

@app.route('/api/users/<string:external_id>/favorites/create/', methods=['POST'])
def create_favorite(external_id):
    body = json.loads(request.data)
    user_id = dao.get_userid_by_externalid(
        external_id=external_id
    )
    listing_id = body.get('listing_id')
    favorite = dao.create_favorite(user_id, listing_id)

    return success_response(favorite, 201)

@app.route('/api/users/<string:external_id>/favorites/')
def get_my_favorites(external_id):
    # body = json.loads(request.data)
    user_id = dao.get_userid_by_externalid(
        external_id=external_id
    )
    my_favorites = dao.get_favorites_by_userid(user_id)

    return success_response(my_favorites)

@app.route('/api/users/<string:external_id>/favorites/remove/', methods=['DELETE'])
def remove_favorite(external_id):
    body = json.loads(request.data)
    user_id = dao.get_userid_by_externalid(
        external_id=external_id
    )
    listing_id = body.get('listing_id')
    removed_favorite = dao.remove_favorite(user_id, listing_id)

    return success_response(removed_favorite)

@app.route('/api/users/<string:external_id>/blocks/create/', methods=['POST'])
def block_user(external_id):
    body = json.loads(request.data)
    user_id = dao.get_userid_by_externalid(
        external_id=external_id
    )
    listing_id = body.get('listing_id')
    block = dao.create_block(user_id, listing_id)

    return success_response(block, 201)

@app.route('/api/master/frez/newlistings/', methods=['GET'])
def get_new_listings():
    new_listings = dao.get_new_listings()

    return success_response(new_listings)

@app.route('/api/master/frez/displaynames/', methods=['GET'])
def get_display_names():
    display_names = dao.get_display_names()

    return success_response(display_names)

@app.route('/api/master/austin/all_listings/', methods=['GET'])
def get_all_listings():
    listings = dao.get_all_listings()

    return success_response(listings)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
