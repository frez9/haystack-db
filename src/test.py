import unittest
import json
import requests
from app import app
from threading import Thread
from time import sleep
import random


LOCAL_URL = "http://localhost:5000"

SAMPLE_USER1 = {"external_id": "extern_1", "display_name": "Austin", "avatar_url": "www.avatar_url1.com"}
USER1_ID = 1
SAMPLE_USER2 = {"external_id": "extern_2", "display_name": "Frez", "avatar_url": "www.avatar_url2.com"}
USER2_ID = 2

IDS_TO_DELETE = [3, 17, 57, 35, 88]
ITEMS_TO_FAVORITE_U1 = [51, 55, 65, 72, 73]
ITEMS_TO_FAVORITE_U2 = [78, 79, 85, 89, 91]

def unwrap_response(response, body={}):
    try:
        return response.json()
    except:
        req = response.request
        raise Exception(f"""
            Error encountered on the following request:

            request path: {req.url}
            request method: {req.method}
            request body: {str(body)}

            There is an uncaught-exception being thrown in your
            method handler for this route!
            """)

def get_all_listings():
    route = f'{LOCAL_URL}/api/master/austin/all_listings/'
    res = requests.get(route)
    body = unwrap_response(res)
    return body['data']

def get_all_listings_user(user):
    external_id = user['external_id']
    route = f'{LOCAL_URL}/api/users/{external_id}/listings/page/0/'
    res = requests.get(route)
    body = unwrap_response(res)
    return body['data']


class TestRoutes(unittest.TestCase):
    def test_a_get_initial_display_names(self):
        route = f'{LOCAL_URL}/api/master/frez/displaynames/'
        res = requests.get(route)
        body = unwrap_response(res)
        assert body["success"]

    def test_b_create_user(self):
        route = f'{LOCAL_URL}/api/users/create/'
        res = requests.post(route, data=json.dumps(SAMPLE_USER1))
        body1 = unwrap_response(res)
        new_user1 = body1["data"]

        assert body1["success"]
        assert new_user1["external_id"] == SAMPLE_USER1["external_id"]
        assert new_user1["avatar_url"] == SAMPLE_USER1["avatar_url"]
        # assert new_user1["snapchat_username"] == None

        res = requests.post(route, data=json.dumps(SAMPLE_USER2))
        body2 = unwrap_response(res) 
        new_user2 = body2['data'] 

        assert body1['success']
        assert new_user2['external_id'] == SAMPLE_USER2['external_id']
        assert new_user2['avatar_url'] == SAMPLE_USER2['avatar_url']
        # assert new_user1['snapchat_username'] == None 

    # def test_c_update_snapchat_username(self):
    #     def create_route(external_id):
    #         return f'{LOCAL_URL}/api/users/{external_id}/username/update/'
    #     def create_json(snapchat_username):
    #         j = {'snapchat_username': snapchat_username}
    #         return json.dumps(j)
        
    #     route1 = create_route(SAMPLE_USER1['external_id'])
    #     res1 = requests.put(route1, data=create_json('awhochman'))
    #     body1 = unwrap_response(res1)
    #     updated_user1 = body1['data']

    #     assert body1['success']
    #     assert updated_user1['snapchat_username'] == 'awhochman'

    #     route2 = create_route(SAMPLE_USER2['external_id'])
    #     res2 = requests.put(route2, data=create_json('freznoel'))
    #     body2 = unwrap_response(res2)
    #     updated_user2 = body2['data']

    #     assert body2['success']
    #     assert updated_user2['snapchat_username'] == 'freznoel'

    def test_d_create_listing(self):
        def create_route(external_id):
            return f'{LOCAL_URL}/api/users/{external_id}/listings/create/'
        def create_json(product_image_url, price, title, description, condition):
            j = {'product_image_url': product_image_url, 'price': price, 'title': title, 'description': description, 'condition': condition}
            return json.dumps(j)
        def create_assert_listing(user, url, user_id, price, title, description, condition):
            route = create_route(user['external_id'])
            res = requests.post(route, data=create_json(url, price, title, description, condition))
            body = unwrap_response(res)
            listing = body['data']

            assert body['success']
            assert listing['user_id'] == user_id
            assert listing['product_image_url'] == url 
            assert listing['avatar_url'] == user['avatar_url']

        i_num = 50
        for i in range(i_num):
            price1 = random.randint(0, 100)
            price2 = random.randint(0, 100)
            cond1 = random.randint(0, 2)
            cond2 = random.randint(0, 2)
            create_assert_listing(SAMPLE_USER1, f'www.product{i}_url.com', USER1_ID, price1, f'title{i}', 'sample description', cond1)
            create_assert_listing(SAMPLE_USER2, f'www.product{i_num+i}_url.com', USER2_ID, price2, f'title{i_num+i}', 'sample description', cond2)

    def test_e_get_my_listings(self):
        def create_route(external_id):
            return f'{LOCAL_URL}/api/users/{external_id}/listings/'

        route = create_route(SAMPLE_USER1['external_id'])
        res = requests.get(route)
        body = unwrap_response(res)
        listings = body['data']

        assert body['success']
        for i in listings:
            assert i['user_id'] == USER1_ID

        route = create_route(SAMPLE_USER2['external_id'])
        res = requests.get(route)
        body = unwrap_response(res)
        listings = body['data']

        assert body['success']
        for i in listings:
            assert i['user_id'] == USER2_ID

    def test_f_get_paginated_listings(self):
        def create_route(external_id, page_num):
            return f'{LOCAL_URL}/api/users/{external_id}/listings/page/{page_num}/'
        
        route = create_route(SAMPLE_USER1['external_id'], 0)
        res = requests.get(route)
        body = unwrap_response(res)
        listings = body['data']

        assert body['success']
        assert len(listings) == 45

        route = create_route(SAMPLE_USER2['external_id'], 1)
        res = requests.get(route)
        body = unwrap_response(res)
        listings = body['data']
        
        assert body['success']
        assert len(listings) == 45

    def test_g_delete_listing(self):
        def create_route(listing_id):
            return f'{LOCAL_URL}/api/listings/{listing_id}/delete/'
        
        for i in IDS_TO_DELETE:
            route = create_route(i)
            res = requests.delete(route)
            body = unwrap_response(res)

            assert body['success']

        all_listings = get_all_listings()
        for l in all_listings:
            assert l['id'] not in IDS_TO_DELETE

    def test_h_create_report(self):
        example_report = 'stolen'
        id_to_rep_x2 = 66
        id_to_rep_x1 = 94
        def create_json(item_id, report):
            j = {'report': report, 'listing_id': item_id}
            return json.dumps(j)
        
        route = f'{LOCAL_URL}/api/reports/create/'
        def report_listing(listing_id, report_message):
            res = requests.post(route, data=create_json(listing_id, report_message))
            body = unwrap_response(res)
            report = body['data']

            assert body['success']
            assert report['report'] == report_message
            assert report['listing_id'] == listing_id
            
        report_listing(id_to_rep_x2, example_report)
        report_listing(id_to_rep_x1, example_report)

        assert len(get_all_listings()) == 95

        report_listing(id_to_rep_x2, example_report)
        report_listing(id_to_rep_x2, example_report)

        assert len(get_all_listings()) == 94
    
    def test_i_create_favorites(self):
        def create_route(external_id):
            return f'{LOCAL_URL}/api/users/{external_id}/favorites/create/'
        def create_json(listing_id):
            j = {'listing_id': listing_id}
            return json.dumps(j)
        def favorite_listing(user, listing_id, user_id):
            route = create_route(user['external_id'])
            res = requests.post(route, data=create_json(listing_id))
            body = unwrap_response(res)
            favorite = body['data']

            assert body['success']
            assert favorite['listing_id'] == listing_id
            assert favorite['user_id'] == user_id

        for i in ITEMS_TO_FAVORITE_U1:
            favorite_listing(SAMPLE_USER1, i, USER1_ID)
        for i in ITEMS_TO_FAVORITE_U2:
            favorite_listing(SAMPLE_USER2, i, USER2_ID)

    def test_j_get_favorites(self):
        def create_route(external_id):
            return f'{LOCAL_URL}/api/users/{external_id}/favorites/'
        
        def check_favorites(user, favorited_items):
            route = create_route(user['external_id'])
            res = requests.get(route)
            body = unwrap_response(res)
            favorites = body['data']

            assert body['success']
            for l in favorites:
                assert l['id'] in favorited_items

        check_favorites(SAMPLE_USER1, ITEMS_TO_FAVORITE_U1)
        check_favorites(SAMPLE_USER2, ITEMS_TO_FAVORITE_U2)

    def test_k_remove_favorite(self):
        def create_route(external_id):
            return f'{LOCAL_URL}/api/users/{external_id}/favorites/remove/'
        def create_json(listing_id):
            j = {'listing_id': listing_id}
            return json.dumps(j)

        route = create_route(SAMPLE_USER1['external_id'])
        res = requests.delete(route, data=create_json(ITEMS_TO_FAVORITE_U1[0]))
        body = unwrap_response(res)
        favorite = body['data']
        
        assert body['success']
        assert favorite['listing_id'] == ITEMS_TO_FAVORITE_U1[0]

        user_id = SAMPLE_USER1['external_id']
        route = f'{LOCAL_URL}/api/users/{user_id}/favorites/'
        res = requests.get(route)
        body = unwrap_response(res)
        for l in body['data']:
            assert l['id'] != ITEMS_TO_FAVORITE_U1[0]
        
    def test_l_block_user(self):
        post_id_to_block = 4
        def create_route(external_id):
            return f'{LOCAL_URL}/api/users/{external_id}/blocks/create/'
        def create_json(listing_id):
            j = {'listing_id': listing_id}
            return json.dumps(j)

        route = create_route(SAMPLE_USER1['external_id'])
        res = requests.post(route, data=create_json(post_id_to_block))
        body = unwrap_response(res)
        block = body['data']

        assert body['success']
        assert block['blocker_id'] == USER1_ID
        assert block['blockee_id'] == USER2_ID

        non_blocked_listings = get_all_listings_user(SAMPLE_USER1)
        for l in non_blocked_listings:
            assert l['user_id'] != USER2_ID 
    
    def test_m_increment_listing_views(self):
        listings_to_inc = [1, 2, 4, 5]
        amount_to_inc_views = [random.randint(1, 15) for i in range(5)]
        def create_route(listing_id):
            return f'{LOCAL_URL}/api/listings/{listing_id}/views/increment/'
        def inc_view(listing_id):
            route = create_route(listing_id)
            res = requests.put(route)
            body = unwrap_response(res)
            listing = body['data']

            assert body['success']
            assert listing['id'] == listing_id 
            assert listing['views'] > 0

        for i, v in enumerate(listings_to_inc):
            for j in range(amount_to_inc_views[i]):
                inc_view(v)

    def test_n_listing_status_sold(self):
        listings_to_sell = [10, 15, 20]
        def create_route(listing_id):
            return f'{LOCAL_URL}/api/listings/{listing_id}/status/sold/'
        def sell_listing(listing_id):
            route = create_route(listing_id)
            res = requests.put(route)
            body = unwrap_response(res)
            listing = body['data']

            assert body['success']
            assert listing['sold'] == True 
        
        for i in listings_to_sell:
            sell_listing(i)

    def test_o_update_listing(self):
        listings_to_update = [6, 7, 8]
        def create_route(listing_id):
            return f'{LOCAL_URL}/api/listings/{listing_id}/update/'
        def create_json(price, title, description, condition):
            j = {'price': price, 'title': title, 'description': description, 'condition': condition}
            return json.dumps(j)
        def update_listing(listing_id, price, title, description, condition):
            route = create_route(listing_id)
            res = requests.put(route, data=create_json(price, title, description, condition))
            body = unwrap_response(res)
            listing = body['data']

            assert body['success']
            assert listing['price'] == price 
            assert listing['title'] == title 
            assert listing['description'] == description 
            assert listing['condition'] == condition 

        for i, v in enumerate(listings_to_update):
            update_listing(v, (i+1)*10, f'new_title{i+1}', f'new_description{i+1}', random.randint(0, 2))

def run_tests():
    sleep(1.5)
    unittest.main()


if __name__ == "__main__":
    thread = Thread(target=run_tests)
    thread.start()
    app.run(host="0.0.0.0", port=5000, debug=False)