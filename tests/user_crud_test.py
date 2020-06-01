import json
from . import app, client, cache, create_token_internal, create_token_noninternal,init_database

class TestUserCrud():
    def test_user_list_internal(self, client, init_database):
        token = create_token_internal()
        res = client.get('/user/list', 
                        headers={'Authorization': 'Bearer ' + token}, 
                        content_type='application/json')

        res_json = json.loads(res.data)
        assert res.status_code == 200

    # def test_user_internal(self, user, init_database):
    #     token = create_token_internal()
    #     res = client.get('/user', 
    #                     headers={'Authorization': 'Bearer ' + token}, 
    #                     content_type='application/json')

    #     res_json = json.loads(res.data)
    #     assert res.status_code == 200

    # def test_user_param_status_internal(self, user, init_database):
    #     token = create_token_internal()
    #     res = user.get('/user?status=true', 
    #                     headers={'Authorization': 'Bearer ' + token}, 
    #                     content_type='application/json')

    #     res_json = json.loads(res.data)
    #     assert res.status_code == 200

    # def test_user_list_orderby_full_name_no_sort(self, user, init_database):
    #     token = create_token_internal()
    #     res = user.get('/user?orderby=full_name&sort=asc', 
    #                     headers={'Authorization': 'Bearer ' + token}, 
    #                     content_type='application/json')

    #     res_json = json.loads(res.data)
    #     assert res.status_code == 200

    # def test_user_list_orderby_full_name(self, user, init_database):
    #     token = create_token_internal()
    #     res = user.get('/user?orderby=full_name', 
    #                     headers={'Authorization': 'Bearer ' + token}, 
    #                     content_type='application/json')

    #     res_json = json.loads(res.data)
    #     assert res.status_code == 200

    # def test_user_invalid_get_id_internal(self, user, init_database):
    #     token = create_token_internal()
    #     res = user.get('/user/ ', 
    #                     headers={'Authorization': 'Bearer ' + token}, 
    #                     content_type='application/json')

    #     res_json = json.loads(res.data)
    #     assert res.status_code == 404

    # def test_user_post_internal(self, user, init_database):
    #     token = create_token_internal()
    #     data = {
    #             "email": "aisyah@gmail.com",
    #             "password": "aisyah",
    #             "avatar": "",
    #             "status": "True"
    #     }
    #     res = user.post('/user', 
    #                     data = json.dumps(data),
    #                     headers={'Authorization': 'Bearer ' + token}, 
    #                     content_type='multipart/form-data')

    #     res_json = json.loads(res.data)
    #     assert res.status_code == 200

    #     self.id_client = res_json['id']

    
    # def test_user_patch_internal(self, user, init_database):
    #     token = create_token_internal()
    #     data = {
    #             "email": "aisyah@gmail.com",
    #             "password": "aisyah",
    #             "avatar": "",
    #             "status": "True"
    #     }
    #     res = user.patch('/user/2', 
    #                     data = json.dumps(data),
    #                     headers={'Authorization': 'Bearer ' + token}, 
    #                     content_type='multipart/form-data')

    #     res_json = json.loads(res.data)
    #     assert res.status_code == 200

    # def test_user_invalid_patch_internal(self, user, init_database):
    #     token = create_token_internal()
    #     data = {
    #             "email": "aisyah@gmail.com",
    #             "password": "aisyah",
    #             "avatar": "",
    #             "status": "True"
    #     }
    #     res = user.put('/user/ ', 
    #                     data = json.dumps(data),
    #                     headers={'Authorization': 'Bearer ' + token}, 
    #                     content_type='multipart/form-data')

    #     res_json = json.loads(res.data)
    #     assert res.status_code == 404

    
    # def test_user_delete_internal(self, user, init_database):
    #     token = create_token_internal()
        
    #     res = user.delete('/user/1', 
    #                     data = json.dumps(data),
    #                     headers={'Authorization': 'Bearer ' + token}, 
    #                     content_type='application/json')

    #     res_json = json.loads(res.data)
    #     assert res.status_code == 200

    # def test_user_invalid_delete_internal(self, user, init_database):
    #     token = create_token_internal()
      
    #     res = user.delete('/user/ ', 
    #                     data = json.dumps(data),
    #                     headers={'Authorization': 'Bearer ' + token}, 
    #                     content_type='application/json')

    #     res_json = json.loads(res.data)
    #     assert res.status_code == 404



    
        
    