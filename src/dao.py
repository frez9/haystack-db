from db import db, User, Listing, Report, Favorite

def get_userid_by_externalid(external_id):
    user = User.query.filter_by(external_id=external_id).first()
    return user.id

def get_avatarurl_by_userid(user_id):
    user = User.query.filter_by(id=user_id).first()
    return user.avatar_url

def get_listings_by_userid(user_id):
    return [x.serialize() for x in Listing.query.filter_by(user_id=user_id).order_by(Listing.id.desc()).all()]

def create_user(external_id, avatar_url):

    if User.query.filter_by(external_id=external_id).first() != None:
        return

    new_user = User(
        external_id=external_id,
        avatar_url=avatar_url
    )

    db.session.add(new_user)
    db.session.commit()
    return new_user.serialize()

def update_snapchat_username(user_id, username):
    user = User.query.filter_by(id=user_id).first()
    user.snapchat_username = username
    db.session.commit()
    return user.serialize()

def create_listing(user_id, product_image_url, avatar_url):
    new_listing = Listing(
        user_id=user_id,
        product_image_url=product_image_url,
        avatar_url=avatar_url
    )

    db.session.add(new_listing)
    db.session.commit()
    return new_listing.serialize()

def is_favorited(user_id, listing_id):
    favorite = Favorite.query.filter_by(user_id=user_id,listing_id=listing_id).first()
    if favorite is None:
        return False

    return True

def get_paginated_listings(user_id, page_number):
    listing_query = Listing.query.order_by(Listing.id.desc()).paginate(page_number, 45, False)
    listings = listing_query.items
    return_list = []

    if len(listings) != 0:
        for listing in listings:
            seller_id = listing.user_id
            user = User.query.filter_by(id=seller_id).first()

            serial = {
                'id': listing.id,
                'product_image_url': listing.product_image_url,
                'avatar_url': listing.avatar_url,
                'seller_snapchat_username': user.snapchat_username,
                'is_favorited': is_favorited(user_id, listing.id)
            }

            return_list.append(serial)

    return return_list

def delete_listing(listing_id):
    Listing.query.filter_by(id=listing_id).delete()
    db.session.commit()

def should_remove_listing(listing_id):
    listing = Listing.query.filter_by(id=listing_id).first()
    report_count = len(listing.reports)

    if report_count >= 2:
        return True

    return False

def create_report(report, listing_id):
    new_report = Report(
        report=report,
        listing_id=listing_id
    )

    if should_remove_listing(listing_id) == True:
        delete_listing(listing_id)
        return None

    db.session.add(new_report)
    db.session.commit()
    return new_report.serialize()


def create_favorite(user_id, listing_id):
    new_favorite = Favorite(
        user_id=user_id,
        listing_id=listing_id
    )

    db.session.add(new_favorite)
    db.session.commit()
    return new_favorite.serialize()

def get_favorites_by_userid(user_id):
    favorites = Favorite.query.filter_by(user_id=user_id).order_by(Favorite.id.desc()).all()

    return_list = []

    for favorite in favorites:
        listing_id = favorite.listing_id
        listing = Listing.query.filter_by(id=listing_id).first()
        user_id = listing.user_id
        user = User.query.filter_by(id=user_id).first()

        serial = {
            'id': listing.id,
            'product_image_url': listing.product_image_url,
            'avatar_url': listing.avatar_url,
            'seller_snapchat_username': user.snapchat_username,
            'is_favorited': is_favorited(user_id, listing.id)
        }

        return_list.append(serial)


    return return_list

def remove_favorite(user_id, listing_id):
    Favorite.query.filter_by(user_id=user_id, listing_id=listing_id).delete()
    db.session.commit()

def master_delete():
    User.query.delete()
    db.session.commit()
    Listing.query.delete()
    db.session.commit()
    Favorite.query.delete()
    db.session.commit()
    Report.query.delete()
    db.session.commit()
