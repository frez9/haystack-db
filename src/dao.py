from db import db, User, Listing, Report, Favorite, Block
from datetime import datetime

def get_userid_by_externalid(external_id):
    user = User.query.filter_by(external_id=external_id).first()
    return user.id

def get_avatarurl_by_userid(user_id):
    user = User.query.filter_by(id=user_id).first()
    return user.avatar_url

def get_listings_by_userid(user_id):
    return [x.serialize() for x in Listing.query.filter_by(user_id=user_id).order_by(Listing.id.desc()).all()]

def create_user(external_id, display_name, avatar_url):

    if User.query.filter_by(external_id=external_id).first() != None:
        return 

    new_user = User(
        external_id=external_id,
        display_name=display_name,
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

def create_listing(user_id, product_image_url, avatar_url, price, title, description, condition):
    new_listing = Listing(
        user_id=user_id,
        product_image_url=product_image_url,
        avatar_url=avatar_url,
        price=price,
        title=title,
        description=description,
        condition=condition
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

            blocked = Block.query.filter_by(blocker_id=user_id, blockee_id=seller_id).first()

            if blocked is None:
                serial = listing.serialize()
                serial['seller_snapchat_username'] = user.snapchat_username
                serial['is_favorited'] = is_favorited(user_id, listing.id)
                # serial = {
                # 'id': listing.id,
                # 'product_image_url': listing.product_image_url,
                # 'avatar_url': listing.avatar_url,
                # 'price': listing.price,
                # 'views': listing.views,
                # 'seller_snapchat_username': user.snapchat_username,
                # 'is_favorited': is_favorited(user_id, listing.id)
                # }
                return_list.append(serial)

    return return_list

def delete_listing(listing_id):
    listing = Listing.query.filter_by(id=listing_id).first()
    db.session.delete(listing)
    db.session.commit()
    return listing.serialize()

def increment_listing_views(listing_id):
    listing = Listing.query.filter_by(id=listing_id).first()
    listing.views += 1
    db.session.commit()
    return listing.serialize()

def listing_status_sold(listing_id):
    listing = Listing.query.filter_by(id=listing_id).first()
    listing.sold = True 
    db.session.commit()
    return listing.serialize()

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

    if should_remove_listing(listing_id):
        delete_listing(listing_id)
        return new_report.serialize()

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
        seller_id = listing.user_id
        seller = User.query.filter_by(id=seller_id).first()

        blocked = Block.query.filter_by(blocker_id=user_id, blockee_id=seller_id).first()

        serial = {
            'id': listing.id,
            'product_image_url': listing.product_image_url,
            'avatar_url': listing.avatar_url,
            'price': listing.price,
            'views': listing.views,
            'seller_snapchat_username': seller.snapchat_username,
            'is_favorited': is_favorited(user_id, listing.id)
        }

        if blocked is None:
            return_list.append(serial)


    return return_list

def remove_favorite(user_id, listing_id):
    favorite = Favorite.query.filter_by(user_id=user_id, listing_id=listing_id).first()
    db.session.delete(favorite)
    db.session.commit()
    return favorite.serialize()

def create_block(user_id, listing_id):
    listing = Listing.query.filter_by(id=listing_id).first()
    seller_id = listing.user_id
    block = Block(
        blocker_id=user_id,
        blockee_id=seller_id
    )

    db.session.add(block)
    db.session.commit()
    return block.serialize()

def get_new_listings():
    listings = Listing.query.all()
    current_week = datetime.now().isocalendar()[1]

    previous_week_count = 0
    current_week_count = 0

    for listing in listings:
        if listing.time_created.isocalendar()[1] == current_week:
            current_week_count += 1
        if listing.time_created.isocalendar()[1] == current_week-1:
            previous_week_count += 1

    return str(previous_week_count)+' new listings last week and '+str(current_week_count)+' new listings so far this week'

def get_display_names():
    users = User.query.all()

    return_list = []

    for user in users:

        serial = {
        'id': user.id,
        'display_name': user.display_name
        }

        return_list.append(serial)

    return return_list

def get_all_listings():
    listings = Listing.query.all()
    return [i.serialize() for i in listings]
