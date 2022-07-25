import os
import requests
from web_manager import WebManager

wm = WebManager()

def instructions():
    print('Available commands:\n',
          'AddSpace\n',
          'Logout\n',
          'GetSolvers\n',
          'RemoveSpaces\n',
          'IsSpaceVisible\n',
          'EditSpaceVisibility\n',
          'DownloadSpace\n',
          'DownloadSpaceXML\n',
          'UploadSpaceXML\n',
          'exit\n')

def loop():
    f = open("Login_info.txt", 'r')
    username, password = f.readline().split()
    wm.spaces_ids = f.readline().split()
    wm.folder_for_downloads = f.readline()
    f.close()
    wm.login(username, password)

    instructions()

    s = input("execute one of the following commands: ")

    while s != "exit":
        if s == 'AddSpace':
            wm.configure_permissions('on', 'on', 'on', 'on', 'on', 'on', 'on', 'on', 'on', 'on', 'on')
            parent_id, name, desc = input('enter parent id, new name and description: ').split()
            print(wm.add_space(parent_id, name, desc))

        if s == 'Logout':
            wm.logout()

        if s == 'RemoveSpaces':
            list = input('enter spaces ids: ').split()
            wm.remove_spaces(list)

        if s == 'IsSpaceVisible':
            space_id = input('enter space id: ')
            wm.is_space_visible(space_id)

        if s == 'DownloadSpace':
            space_id, solvs, benchs, hier = input('enter space id and bools for including solvers, benchs and hierarchy: ').split()
            wm.download_space(space_id, solvs, benchs, hier)

        if s == 'DownloadSpaceXML':
            id, include_attrs, benchmarks_updates, upid = input('enter space id and bools for including attrs, updates and upid(optional from updates): ').split()
            wm.download_space_xml(id, include_attrs, benchmarks_updates, upid)

        if s == 'UploadSpaceXML':
            parent_id, space_id = input('enter parent_id and space_id: ').split()
            with open(f'upload_folder\spaceXML_{space_id}.zip', 'rb') as f:             
                wm.upload_space_xml(parent_id, f)

        if s == 'EditSpaceVisibility':
            space_id, hierarchy, makePublic = input('enter space id, hierarchy status and public status: ').split()
            wm.edit_space_visibility(space_id, hierarchy, makePublic)

        if s == 'GetSolvers':
            wm.get_solvers()

        s = input("execute one of the following commands: ")
    wm.logout()
                       
loop()
