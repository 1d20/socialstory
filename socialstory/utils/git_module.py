__author__ = 'Detonavomek'
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
    commit(branch, 'branch init')
    os.chdir(PROJECT_PATH)

def get_last_publish_commit(story):
    id = story.id
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
    HISTORY_LIST_COMMAND = open(os.path.join(STATIC_ROOT, 'bash/commit_info.bash')).read()
    result = subprocess.check_output(HISTORY_LIST_COMMAND+commit, shell=True)
    result = result[:-1]
    os.chdir(PROJECT_PATH)
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