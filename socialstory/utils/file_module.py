__author__ = 'Detonavomek'
#-*- coding: utf-8 -*-
from utils.git_module import GLOBAL_STORY_FILE


def get_txt_content(branch):
    file_path = GLOBAL_STORY_FILE.format(str(branch.id))

    f = open(file_path)
    res = f.read()
    f.close()
    return res

def rewrite_txt_content(branch, content):
    file_path = GLOBAL_STORY_FILE.format(str(branch.id))

    f = open(file_path, 'w')
    f.write(content)
    f.close()
    return True