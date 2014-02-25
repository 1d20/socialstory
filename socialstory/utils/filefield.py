__author__ = 'Detonavomek'
#-*- coding: utf-8 -*-

import os, shutil
PROJECT_PATH = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

def get_txt_content(url):
    file_path = PROJECT_PATH+'/'+url

    f = open(file_path)
    res = f.read()
    f.close()
    return res;

def create_txt_file(default_path_obj, id):
    default_path = str(default_path_obj)
    dpl = default_path.split('.')[:(len(default_path.split('.'))-1)]
    local_out_file = ''
    for dp in dpl:
        local_out_file += dp
    local_out_file += str(id)+'.txt'

    in_file = PROJECT_PATH+'/media/'+default_path
    out_file = PROJECT_PATH+'/media/'+local_out_file

    shutil.copyfile(in_file, out_file)
    return local_out_file


def rewrite_txt_content(url, content):
    file_path = PROJECT_PATH+'/'+url

    f = open(file_path, 'w')
    f.write(content)
    f.close()
    return True