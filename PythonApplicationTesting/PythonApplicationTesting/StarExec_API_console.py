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
          'exit\n')

def loop():
    f = open("Login_info.txt", 'r')
    username, password = f.readline().split()
    f.close()
    wm.Login(username, password)

    instructions()

    s = input("execute one of the following commands: ")

    while s != "exit":
        if s == 'AddSpace':
            wm.Configure_permissions('on', 'on', 'on', 'on', 'on', 'on', 'on', 'on', 'on', 'on', 'on')
            parent_id, name, desc = input('enter parent id, new name and description: ').split()
            print(wm.Add_space(parent_id, name, desc))

        if s == 'Logout':
            wm.Logout()

        if s == 'RemoveSpaces':
            list = input('enter spaces ids: ').split()
            wm.RemoveSpaces(list)

        if s == 'IsSpaceVisible':
            space_id = input('enter space id: ')
            wm.IsSpaceVisible(space_id)

        if s == 'EditSpaceVisibility':
            space_id, hierarchy, makePublic = input('enter space id, hierarchy status and public status: ').split()
            wm.EditSpaceVisibility(space_id, hierarchy, makePublic)

        if s == 'GetSolvers':
            wm.GetSolvers()

        s = input("execute one of the following commands: ")
    wm.Logout()
                       
loop()
