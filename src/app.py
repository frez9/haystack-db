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

@app.route('/api/users/username/update/', methods=['POST'])
def update_snapchat_username():
    body = json.loads(request.data)
    user_id = dao.get_userid_by_externalid(
        external_id=body.get('external_id')
    )
    updated_user_info = dao.update_snapchat_username(
        user_id=user_id,
        username=body.get('snapchat_username')
    )

    return success_response(updated_user_info)

@app.route('/api/listings/create/', methods=['POST'])
def create_listing():
    body = json.loads(request.data)
    user_id = dao.get_userid_by_externalid(
        external_id=body.get('external_id')
    )
    avatar_url = dao.get_avatarurl_by_userid(user_id)
    listing = dao.create_listing(
        user_id=user_id,
        product_image_url=body.get('product_image_url'),
        avatar_url=avatar_url
    )

    return success_response(listing, 201)

@app.route('/api/listings/my/', methods=['POST'])
def get_my_listings():
    body = json.loads(request.data)
    user_id = dao.get_userid_by_externalid(
        external_id=body.get('external_id')
    )
    my_listings = dao.get_listings_by_userid(user_id)

    return success_response(my_listings)

@app.route('/api/listings/paginated/', methods=['POST'])
def get_paginated_listings():
    body = json.loads(request.data)
    user_id = dao.get_userid_by_externalid(
        external_id=body.get('external_id')
    )
    listings = dao.get_paginated_listings(
        user_id=user_id,
        page_number=body.get('page_number')
    )

    return success_response(listings)

@app.route('/api/listings/delete/', methods=['DELETE'])
def delete_listing():
    body = json.loads(request.data)
    deleted_listing = dao.delete_listing(
        listing_id=body.get('listing_id')
    )

    return success_response(deleted_listing)

@app.route('/api/reports/create/', methods=['POST'])
def create_report():
    body = json.loads(request.data)
    report = dao.create_report(
        report=body.get('report'),
        listing_id=body.get('listing_id')
    )
    if report is None:
        return failure_response("Listing has been removed for too many reports")

    return success_response(report, 201)

@app.route('/api/favorites/create/', methods=['POST'])
def create_favorite():
    body = json.loads(request.data)
    user_id = dao.get_userid_by_externalid(
        external_id=body.get('external_id')
    )
    listing_id = body.get('listing_id')
    favorite = dao.create_favorite(user_id, listing_id)

    return success_response(favorite, 201)

@app.route('/api/favorites/my/', methods=['POST'])
def get_my_favorites():
    body = json.loads(request.data)
    user_id = dao.get_userid_by_externalid(
        external_id=body.get('external_id')
    )
    my_favorites = dao.get_favorites_by_userid(user_id)

    return success_response(my_favorites)

@app.route('/api/favorites/remove/', methods=['DELETE'])
def remove_favorite():
    body = json.loads(request.data)
    user_id = dao.get_userid_by_externalid(
        external_id=body.get('external_id')
    )
    listing_id = body.get('listing_id')
    removed_favorite = dao.remove_favorite(user_id, listing_id)

    return success_response(removed_favorite)

@app.route('/api/blocks/create/', methods=['POST'])
def block_user():
    body = json.loads(request.data)
    user_id = dao.get_userid_by_externalid(
        external_id=body.get('external_id')
    )
    listing_id = body.get('listing_id')
    block = dao.create_block(user_id, listing_id)

    return success_response(block, 201)

@app.route('/api/master/frez/delete/', methods=['DELETE'])
def master_delete():
    deletion = dao.master_delete()

    return success_response(deletion)

@app.route('/api/master/frez/displaynames/', methods=['POST'])
def get_display_names():
    display_names = dao.get_display_names()

    return success_response(display_names)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
