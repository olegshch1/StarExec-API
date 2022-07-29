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

    def add_space (self, parent_id, 
                   name, desc, 
                   locked, users, 
                   solvers, benchmarks, 
                   sticky, add_bench, 
                   add_job, add_solver, 
                   add_space, add_user, 
                   remove_bench, remove_job, 
                   remove_solver, remove_space, 
                   remove_user, is_leader):
        """
        Add space with bool params
        """
        
        for var in {add_bench, 
                   add_job, add_solver, 
                   add_space, add_user, 
                   remove_bench, remove_job, 
                   remove_solver, remove_space, 
                   remove_user}:
            if var == True or var == 'true': var = 'on' 
            if var == False or var == 'false': var = 'off' 

        payload = {'parent': parent_id,
                   'name': name,
                   'desc': desc,
                   'addSolver':add_solver,
                   'addBench':add_bench, 
                   'addUser':add_user,
                   'addSpace':add_space,
                   'addJob':add_job, 
                   'removeSolver':remove_solver,
                   'removeBench':remove_bench,
                   'removeUser':remove_user,
                   'removeSpace':remove_space,
                   'removeJob':remove_job,                                        
                   #'isLeader':is_leader,
                   'locked':locked,
                   'users': users,
                   'solvers': solvers,
                   'benchmarks': benchmarks,
                   'sticky': sticky}
        response = self.session.post(self.preffix_url + 'add/space', data= payload)
        return self.session.cookies.get_dict()['New_ID']

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
        with open(f'download_folder\space_{id}.zip', 'wb') as f:
            for chunk in response.iter_content(10000000):                
                f.write(chunk)
                f.flush()
                os.fsync(f.fileno())
        #delete print
        print('downloading is done')

    def download_space_xml(self, id, include_attrs, benchmarks_updates, upid):
        if benchmarks_updates == False: upid = -1
        paramlist = {'type': 'spaceXML', 'id': id, 'includeattrs': include_attrs, 'updates': benchmarks_updates, 'upid': upid}      
        response = self.session.get(self.preffix_url + 'download', params = paramlist, stream = True)
        response.raise_for_status()
        with open(f'download_folder\spaceXML_{id}.zip', 'wb') as f:
            for chunk in response.iter_content(chunk_size=1024000):
                if chunk:
                    f.write(chunk)
                    f.flush()
                    os.fsync(f.fileno())
        #delete print
        print('downloading is done')
# in progress
    def upload_space_xml(self, parent_space_id, file):
        response = self.session.post(self.preffix_url + 'upload/space', files={'file': file}, data={'space':parent_space_id})
        # delete print
        print(response.text)

    def create_job(self, sid, name, desc, 
                   preprocess, postprocess, queue, 
                   wallclock_timeout, cpu_timeout, max_mem, 
                   subscribe, traversal, pause, 
                   seed, benchmarking_framework, results_interval, 
                   save_other_output, suppress_timestamp, kill_delay, 
                   soft_time_limit, run_choice):

        payload={'sid':sid,	
                 'name':name,
                 'desc':desc,
                 'preProcess':pre_process,
                 'postProcess':post_process,
                 'queue':queue,
                 'wallclockTimeout':wallclock_timeout,
                 'cpuTimeout':cpu_timeout,
                 'maxMem':max_mem,
                 'subscribe':subscribe,
                 'traversal':traversal,
                 'pause':pause,
                 'seed':seed,
                 'benchmarkingFramework':benchmarking_framework,
                 'resultsInterval':results_interval,
                 'saveOtherOutput':save_other_output,
                 'suppressTimestamp':suppress_timestamp,
                 'killDelay':kill_delay,
                 'softTimeLimit':soft_time_limit,
                 'runChoice':run_choice}

        response = self.session.post(self.preffix_url + 'add/job', data=payload)
        return self.session.cookies.get_dict()['New_ID']