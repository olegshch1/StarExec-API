import requests
from bs4 import BeautifulSoup, SoupStrainer

class WebManager(object):
    """class provides StarExec API"""
    preffix_url = 'https://www.starexec.org/starexec/secure/'
    preffix_url_for_services = 'https://www.starexec.org/starexec/'

    def GetUserId(self):
        self.userId = self.session.get(self.preffix_url_for_services + 'services/users/getid').text


    def Login(self, username, password):
        """
        Login and getting user's ID on StarExec platform
        """
        self.session = requests.Session()
        response = self.session.get(self.preffix_url + 'index.jsp')
        response = self.session.post(self.preffix_url + 'j_security_check', data= {'j_username': username, 'j_password': password})
        response = self.session.get(self.preffix_url + 'index.jsp')
        self.GetUserId()
        

    def Configure_permissions (self, addBench, addJob, addSolver, addSpace, addUser, removeBench, removeJob, removeSolver, removeSpace, removeUser, isLeader):
        """
        Provides permissions for post requests
        All arguments are on/off string type
        """
        self.permissions_dict = {
                'addBench':addBench, 
                'addJob':addJob, 
                'addSolver':addSolver, 
                'addSpace':addSpace, 
                'addUser':addUser, 
                'removeBench':removeBench,
                'removeJob':removeJob, 
                'removeSolver':removeSolver, 
                'removeSpace':removeSpace, 
                'removeUser':removeUser, 
                'isLeader':isLeader}

#in progress
    def Add_space (self, parent_id, name, desc):
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
        print(response.text)
        print(response.url)

    def without_keys(self, dict, keys):
        return {k: v for k, v in dict.items() if k not in keys}


    def Logout(self):
        response = self.session.post(self.preffix_url_for_services + 'services/session/logout')
        #print(response.text)

# in progress
    def GetSolvers(self):
        paramlist = {'id': self.userId}
        response = self.session.get(self.preffix_url + '/details/user.jsp', params=paramlist)
        soup = BeautifulSoup(response.content, 'html.parser', parse_only=SoupStrainer('a'))
        for link in soup:
            if link.has_attr('href'):
                print(link['href'])


    def RemoveSpaces(self, list):
        response = self.session.post(self.preffix_url_for_services + 'services/remove/subspace', data= {'selectedIds[]': list, 'recyclePrims': 'false'})
        print(response.text)

    def IsSpaceVisible(self, spaceId):
        response = self.session.post(self.preffix_url_for_services + f'services/space/isSpacePublic/{spaceId}')
        print(response.text,'\n',response.url)

    def EditSpaceVisibility(self, spaceId, hierarchy, makePublic):
        response = self.session.post(self.preffix_url_for_services + f'services/space/changePublic/{spaceId}/{hierarchy}/{makePublic}')
        print(response.text)