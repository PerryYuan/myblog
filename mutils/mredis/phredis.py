# coding:utf8
import redis
import json
class TopArticleRedis(object):
    def __init__(self,cache):
        self.cache = cache
        self.name = 'top_article'

    @classmethod
    def to_json(self,article):
        top_article_context = {'uid': str(article.uid), 'title': article.title, 'desc': article.desc,
            'thumbnail': article.thumbnail}
        return json.dumps(top_article_context)

    def add_top_article(self,article):
        # top_len = self.cache.llen(self.name)
        # if top_len >= 3:
        #     self.cache.rpop(self.name)
        self.cache.lpush(self.name,TopArticleRedis.to_json(article))

    def delete_top_article(self,article):
        try:
            self.cache.lrem(self.name,TopArticleRedis.to_json(article),1)
        except Exception:
            pass

    def get_all(self):
        return self.cache.lrange(self.name,0,2)

class CategoryRedis(object):
    def __init__(self,cache):
        self.cache = cache
        self.name = 'category'

    @classmethod
    def to_json(self,category):
        context = {
            'id':category.id,
            'name':category.name
        }
        return json.dumps(context)

    def add_category(self,category):
        self.cache.lpush(self.name,CategoryRedis.to_json(category))

    def delete_category(self,category):
        try:
            self.cache.lrem(self.name,CategoryRedis.to_json(category),1)
        except Exception:
            pass

    def push_all_category(self,categorys):
        for category in categorys:
            self.add_category(category)

    def category_update(self,old_category,new_category):
        self.delete_category(old_category)
        self.add_category(new_category)
    def get_all(self):
        return self.cache.lrange(self.name,0,-1)





class MyBlogRedis(object):
    _pool = redis.ConnectionPool(host='127.0.0.1', port=6379)
    cache = redis.Redis(connection_pool=_pool)
    top_article = TopArticleRedis(cache)
    category = CategoryRedis(cache)
    @classmethod
    def set(cls,name,value):
        cls.cache.set(name,value)
    @classmethod
    def get(cls,name):
        return cls.cache.get(name)

