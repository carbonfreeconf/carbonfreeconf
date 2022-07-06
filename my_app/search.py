from elasticsearch_dsl.connections import connections
from elasticsearch_dsl import Document, Text, Date, Search, Boolean, Integer, Keyword, Completion,analyzer, tokenizer#, fields
from elasticsearch.helpers import bulk
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Q
from urllib.parse import urlparse
import os
from . import models
from django.conf import settings
from django.utils.html import strip_tags

#connections.create_connection()
#print('before0',os.environ.get('SEARCHBOX_URL'))

if not 'ON_HEROKU' in os.environ:
    url = urlparse(os.environ.get('SEARCHBOX_URL'))#celui la en local
    connections.create_connection()#celui la en local
else:
    url = getattr(settings, "SEARCHBOX_URL", None)#celui lasur heroku
    connections.create_connection(hosts=[os.environ.get('SEARCHBOX_URL')], timeout=20)#celui la sur heroku

#print('before',url,url.hostname)
#print('after')

class PostIndex(Document):
    slug = Keyword()
    author = Text()
    created_on = Date()
    title = Text()
    title_suggest = Completion()
    content = Text()
    class Index:
        name = 'post-index'

class ConfIndex(Document):
    title = Text()
    title_suggest = Completion()
    abstract = Text()
    start_date = Date()
    end_date = Date()
    user = Text()
    subject = Text()
    #size = Keyword()#doesn't work for some reasons, ES thinks it is an integer
    privacy = Text()
    recording = Boolean()

    class Index:
        name = 'conf-index'


def bulk_indexing():
    PostIndex.init()

    es = Elasticsearch()
    bulk(client=es, actions=(b.indexing() for b in models.Post.objects.all().iterator()))

    ConfIndex.init()
    es = Elasticsearch()
    #url = urlparse(os.environ.get('SEARCHBOX_URL'))

    #es = Elasticsearch(
     #   [url.hostname],
      #  http_auth=(url.username, url.password),
       # scheme=url.scheme,
       # port=url.port,
    #)
    bulk(client=es, actions=(b.indexing() for b in models.CreateConf.objects.all().iterator()))

def Search_suggestion(content):
    client = Elasticsearch()

    #Search in Posts

    #s = Search().filter('term', content=content)
    #s = Search(using=client).query("match", content=content)
    #s = s.highlight('title')
    s = Search(index='post-index')
    q_post = Q("multi_match", query=content, fields=['title'],fuzziness=1)
    #q_post2 = Q("multi_match", query=content, fields=['content'],fuzziness=1)
    #q_conf = Q("multi_match", query=content, fields=['title', 'content','author'])
    q = q_post #| q_post2
    s = s.query(q)

    s1 = Search(index='post-index')
    #q_post = Q("multi_match", query=content, fields=['title'], fuzziness=1)
    q_post2 = Q("multi_match", query=content, fields=['content'], fuzziness=1)
    # q_conf = Q("multi_match", query=content, fields=['title', 'content','author'])
    q = q_post2# | q_post2
    s1 = s1.query(q)

    #s = Search(index='qb_ir_instance_of')[0:10].query('multi_match', query=text,
     #                                                 fields=['wiki_content', 'qb_content', 'source_content'])
    #s = s.highlight('content').highlight('title')

    # Search in Confs

    s2 = Search(index='conf-index')
    #q_conf = Q("query_string", query=content, fields=['title'],fuzziness=3)
    q_conf = Q("multi_match", query=content, fields=['title'],fuzziness=1)
    #q_conf2 = Q("multi_match", query=content, fields=['abstract'],fuzziness=1)
    #q_conf = Q("wildcard", query='content*')

    q = q_conf#|q_conf2
    s2 = s2.query(q)

    s3 = Search(index='conf-index')
    # q_conf = Q("query_string", query=content, fields=['title'],fuzziness=3)
    #q_conf = Q("multi_match", query=content, fields=['title'], fuzziness=1)
    q_conf2 = Q("multi_match", query=content, fields=['abstract'], fuzziness=1)
    # q_conf = Q("wildcard", query='content*')

    q = q_conf2# | q_conf2
    s3 = s3.query(q)

    #print('dict0',s.to_dict())
    #print('dict1',s1.to_dict())
    #print('dict2',s2.to_dict())
    #print('dict3',s3.to_dict())
    response0 = s.execute()
    response1 = s1.execute()
    response2 = s2.execute()
    response3 = s3.execute()
    #response3 = s3.execute().to_dict()
    #print('resp3',response3)
    #for value in s3.execute().suggest.my_suggestion:
    #    print(value.text)
    #print('testsug',s3.execute().sugeest)
    #print('r1sug',response1)
    #print('r2sug',response3)


    suggest=[]
    lenmax=20
    for hit in response0.hits:
        #print('hitpost', hit.title)
        if not hit.title.upper() in (sug.upper() for sug in suggest):
            etc=''
            if len(hit.title)>lenmax:
                etc='...'
            suggest.append(hit.title.lower()[0:min(len(hit.title),lenmax)]+etc)

    for hit in response1.hits:
        #print('hitpost', hit.content)
        if not hit.content.upper() in (sug.upper() for sug in suggest):
            etc = ''
            if len(strip_tags(hit.content)) > lenmax:
                etc = '...'
            suggest.append(strip_tags(hit.content.lower())[0:min(len(strip_tags(hit.content)),lenmax)]+etc)

    for hit in response2.hits:
        #print('hitconf', hit.title)
        if not hit.title.upper() in (sug.upper() for sug in suggest):
            etc = ''
            if len(hit.title) > lenmax:
                etc = '...'
            suggest.append(hit.title.lower()[0:min(len(hit.title),lenmax)]+etc)

    for hit in response3.hits:
        #print('hitconf', hit.abstract)
        if not hit.abstract.upper() in (sug.upper() for sug in suggest):
            etc = ''
            if len(hit.abstract) > lenmax:
                etc = '...'
            suggest.append(hit.abstract.lower()[0:min(len(hit.abstract),lenmax)]+etc)

    #print('r3',response3)

    #print('sugge',suggest)
    response=[response0,response1,response2,response3]

    return suggest#response


def Search_ela(content):
    client = Elasticsearch()
    #url = urlparse(os.environ.get('SEARCHBOX_URL'))

    #client = Elasticsearch(
     #   [url.hostname],
      #  http_auth=(url.username, url.password),
      #  scheme=url.scheme,
       # port=url.port,
    #)
    #Search in Posts

    #s = Search().filter('term', content=content)
    #s = Search(using=client).query("match", content=content)
    #s = s.highlight('title')
    s = Search(index='post-index')
    q_post = Q("multi_match", query=content, fields=['title', 'content','author'],fuzziness='AUTO')
    #q_conf = Q("multi_match", query=content, fields=['title', 'content','author'])
    q=q_post #| q_conf
    s = s.query(q)

    #s = Search(index='qb_ir_instance_of')[0:10].query('multi_match', query=text,
     #                                                 fields=['wiki_content', 'qb_content', 'source_content'])
    s = s.highlight_options(pre_tags="<b>", post_tags="</b>")

    s = s.highlight('content', fragment_size=300).highlight('title', fragment_size=100)
    # Search in Confs

    s2 = Search(index='conf-index')
    #q_post = Q("multi_match", query=content, fields=['title', 'content', 'author'])
    q_conf = Q("multi_match", query=content, fields=['title', 'abstract', 'user'])
    q_conf = Q("query_string", query=content, fields=['title', 'abstract', 'user'],fuzziness='AUTO')
    q = q_conf
    s2 = s2.query(q)

    # s = Search(index='qb_ir_instance_of')[0:10].query('multi_match', query=text,
    #                                                 fields=['wiki_content', 'qb_content', 'source_content'])
    s2 = s2.highlight_options(pre_tags="<b>", post_tags="</b>")

    s2 = s2.highlight('abstract', fragment_size=300).highlight('title', fragment_size=100)

    #results = list(s.execute())
    #f len(results) == 0:
     #   highlights = {'wiki': [''],
      #                'qb': [''],
       #               'guess': ''}
       # return highlights

    #guess = results[0]  # take the best answer
    #_highlights = guess.meta.highlight

    #try:
     #   content = list(_highlights.content)
    #except AttributeError:
     #   content = ['']

    #try:
     #   title = list(_highlights.title)
    #except AttributeError:
     #   title = ['']

    #highlights = {'title': title,
     #             'content': content,
      #            'guess': guess}
    #print(highlights)
    #return highlights
    search = Search(index='post-index')



    #print('dict',s.to_dict())
    #print('dict',s2.to_dict())
    response1 = s.execute()
    response2 = s2.execute()

    #print('testsug',s3.execute().sugeest)
    #print('r1',response1)
    #print('r2',response2)

    response=[response1,response2]

    return response
