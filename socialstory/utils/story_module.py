__author__ = 'Detonavomek'
import random

from apps.stories.models import *


def get_similar_stories(branch):
    story_count = 6
    stories_info = []
    #sts1 = SimilarStory.objects.filter(story1=story).order_by('count').all()[:story_count]# group - rating
    #sts2 = SimilarStory.objects.filter(story2=story).order_by('count').all()[:story_count]# group - rating
    sts3 = Story.objects.filter().exclude(id=branch.story.id).order_by('date_add')[:story_count+1]
    sts = []
    #for s in sts1:
    #    sts.append(s.story2)
    #for s in sts2:
    #    sts.append(s.story1)
    last_stories = story_count - len(sts)
    for i in range(0, last_stories):
        sts.append(sts3[i])
    random.shuffle(sts)
    for i in range(0, story_count):
        stories_info.append({
            'id': sts[i].story_version.all()[0].id,
            'title': sts[i].story_version.all()[0].title,
            'poster': sts[i].story_version.all()[0].poster
        })
    return stories_info


def txt_to_ssr(lines):
    result = ''
    p_id = 0
    for l in lines:
        l = l.split('\n')[0]
        l = '<p data-element-id="'+str(p_id)+'">'+l+'</p>\n'
        #print l
        p_id+=1
        result += l
    return result