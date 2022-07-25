import requests
from bs4 import BeautifulSoup, SoupStrainer
import os

class WebManager(object):
    """class provides StarExec API"""
    preffix_url = 'https://www.starexec.org/starexec/secure/'
    preffix_url_for_services = 'https://www.starexec.org/starexec/'
    spaces_ids = []
    folder_for_downloads = ''

    def get_user_id(self):
        self.user_id = self.session.get(self.preffix_url_for_services + 'services/users/getid').text


    def login(self, username, password):
        """
        Login and getting user's ID on StarExec platform
        """
        self.session = requests.Session()
        response = self.session.get(self.preffix_url + 'index.jsp')
        response = self.session.post(self.preffix_url + 'j_security_check', data= {'j_username': username, 'j_password': password})
        response = self.session.get(self.preffix_url + 'index.jsp')
        self.get_user_id()
        
# need to be modified
    def configure_permissions (self, add_bench, add_job, 
                               add_solver, add_space, 
                               add_user, remove_bench, 
                               remove_job, remove_solver, 
                               remove_space, remove_user, 
                               is_leader):
        """
        Provides permissions for post requests
        All arguments are on/off string type
        """
        self.permissions_dict = {
                'addBench':add_bench, 
                'addJob':add_job, 
                'addSolver':add_solver, 
                'addSpace':add_space, 
                'addUser':add_user, 
                'removeBench':remove_bench,
                'removeJob':remove_job, 
                'removeSolver':remove_solver, 
                'removeSpace':remove_space, 
                'removeUser':remove_user, 
                'isLeader':is_leader}

#in progress
    def add_space (self, parent_id, name, desc):
        payload = {'parent': parent_id,
                   'name': name,
                   'desc': desc,
                   'locked':'false',
                   'users': 'true',
                   'solvers': 'true',
                   'benchmarks': 'true',
                   'sticky': 'false'}
        response = self.session.post(self.preffix_url + 'add/space', data= payload.update(self.without_keys(self.permissions_dict, ['isLeader'])))
        #response = self.session.post(self.preffix_url + 'add/space', data= payload)
        #delete print
        print(response.text)
        #delete print
        print(response.url)

    def without_keys(self, dict, keys):
        return {k: v for k, v in dict.items() if k not in keys}


    def logout(self):
        response = self.session.post(self.preffix_url_for_services + 'services/session/logout')

# in progress
    def get_solvers(self):
        paramlist = {'id': self.user_id}
        response = self.session.get(self.preffix_url + '/details/user.jsp', params=paramlist)
        soup = BeautifulSoup(response.content, 'html.parser', parse_only=SoupStrainer('a'))
        for link in soup:
            if link.has_attr('href'):
                print(link['href'])


    def remove_spaces(self, list):
        response = self.session.post(self.preffix_url_for_services + 'services/remove/subspace', data= {'selectedIds[]': list, 'recyclePrims': 'false'})
        #delete print
        print(response.text)

    def is_space_visible(self, space_id):
        response = self.session.post(self.preffix_url_for_services + f'services/space/isSpacePublic/{space_id}')
        if response.text == '1': return True
        else: return False

    def edit_space_visibility(self, space_id, hierarchy, make_public):
        """
        Change visibility for space and its hierarchy by True/False 
        """
        response = self.session.post(self.preffix_url_for_services + f'services/space/changePublic/{space_id}/{hierarchy}/{make_public}')

    def download_space(self, id, include_solvers, include_benchmarks, hierarchy):
        paramlist = {'type': 'space', 'id': id, 'includesolvers': include_solvers, 'includebenchmarks': include_benchmarks, 'hierarchy': hierarchy}
        response = self.session.get(self.preffix_url + 'download', params = paramlist, stream = True)
        response.raise_for_status()
        with open(self.folder_for_downloads + f'space_{id}.zip', 'wb') as f:
            for chunk in response.iter_content(chunk_size=1024*6):
                #delete print
                print('receiving')
                f.write(chunk)
                f.flush()
                os.fsync(f.fileno())
        #delete print
        print('downloading is done')

    def upload_space_xml(self, parent_space_id, file):
        response = self.session.post(self.preffix_url + 'upload/space', files=file, params={'space':parent_space_id})
        # delete print
        print(response.text)