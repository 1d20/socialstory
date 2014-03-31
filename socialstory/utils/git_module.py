__author__ = 'Detonavomek'
#-*- coding: utf-8 -*-
import os, subprocess
from source.settings import MEDIA_ROOT, PROJECT_PATH, STATIC_ROOT
from apps.stories.models import *

TEMPLATE_FILE_NAME = 'story.txt'
REPO_FOLDER = "stories"
REPO_PATH = os.path.join(MEDIA_ROOT, REPO_FOLDER)
GLOBAL_STORY_FOLDER = os.path.join(REPO_PATH, '{0}')
GLOBAL_STORY_FILE = os.path.join(GLOBAL_STORY_FOLDER, TEMPLATE_FILE_NAME)

def commit(branch, message):
    STORY_FOLDER = GLOBAL_STORY_FOLDER.format(str(branch.id))
    os.chdir(STORY_FOLDER)
    try:
        result = subprocess.check_output("git add . && git commit -m \"" + message + "\"", shell=True)
        result = result[:-1]
        result = result.split(']')[0][-8:]
        os.chdir(PROJECT_PATH)
    except:
        os.chdir(PROJECT_PATH)
        return

    comm = Commit()
    comm.branch = branch
    comm.code = result
    comm.title = message
    comm.save()

def create_branch(branch):
    STORY_FOLDER = GLOBAL_STORY_FOLDER.format(str(branch.id))
    if not os.path.exists(STORY_FOLDER):
        os.makedirs(STORY_FOLDER)
    os.chdir(STORY_FOLDER)
    os.system("git init")
    os.system("touch "+TEMPLATE_FILE_NAME)
    commit(branch, 'Створення оповідання')
    os.chdir(PROJECT_PATH)

def get_last_publish_commit(branch):
    id = branch.id
    STORY_FOLDER = GLOBAL_STORY_FOLDER.format(str(id))
    os.chdir(STORY_FOLDER)
    result = subprocess.check_output("git show HEAD:"+TEMPLATE_FILE_NAME, shell=True)
    result = result[:-1]
    os.chdir(PROJECT_PATH)
    return result

def get_commit_info(story, commit):
    id = story.id
    STORY_FOLDER = GLOBAL_STORY_FOLDER.format(str(id))
    os.chdir(STORY_FOLDER)
    HISTORY_LIST_COMMAND = 'git show '
    result = subprocess.check_output(HISTORY_LIST_COMMAND+commit, shell=True)
    result = result[:-1]
    os.chdir(PROJECT_PATH)

    result = result.split('\n')
    commit_code = result[0].split('commit')[1]
    date = result[2].split('Date:')[1]

    #blocks = []

    #result = {
    #    'code': commit_code,
    #    'date': date,
        #'blocks': blocks,
    #}

    #'lines': lines,
    #    'changes': changes,
    #block = {}
    #changes = []
    #bls = result[2].split('Date:')[1]
    #for l in bls:
    #    if '@' == l[0]:
    #        blocks.append(block)
    #        block = {}
    #        changes = []
    #        block['lines'] = l[2:-2]
    #        block['changes'] = changes
    #    changes.append({
    #        'type': l[0],
    #        'content': l[1:],
    #    })

    #lines = result[10][2:-2]
    cs = result[10:]
    changes = []
    for c in cs:
        changes.append({
            'type': c[0],
            'content': c[1:],
        })
    result = {
        'code': commit_code,
        'date': date,
        'changes': changes,
    }
    return result

#def get_commit_list(story):
#    id = story.id
#    STORY_FOLDER = GLOBAL_STORY_FOLDER.format(str(id))
#    os.chdir(STORY_FOLDER)
#    HISTORY_LIST_COMMAND = open(os.path.join(STATIC_ROOT, 'bash/commit_list.bash')).read()
#    result = subprocess.check_output(HISTORY_LIST_COMMAND, shell=True)
#    result = result[:-1]
#    os.chdir(PROJECT_PATH)
#    return result