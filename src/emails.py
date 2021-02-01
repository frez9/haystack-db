import json
import smtplib

def listing_sold(listing, user):

    listing_json = json.dumps(listing.serialize())
    user_json = json.dumps(user.serialize())

    msg = f"""
    Listing info: {listing_json}\n\n
    User_json: {user_json}"""

    SERVER = smtplib.SMTP('smtp.gmail.com', 587)
    SERVER.starttls()

    SENDER = 'haystacknotifications@gmail.com'
    password = 'Damnproud12345!'
    SERVER.login(SENDER, password)


    SERVER.sendmail(SENDER, 'awh76@cornell.edu', msg)
    SERVER.sendmail(SENDER, 'Fyn2@cornell.edu', msg)

