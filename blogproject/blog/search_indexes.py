from haystack import indexes
from .models import Post

class PostIndex(indexes.SearchIndex,indexes.Indexable):
    # 习惯性写法，设置text字段，设置document=True,use_template=True
    text = indexes.CharField(document=True,use_template=True)
    def get_model(self):
        return Post

    def index_queryset(self, using=None):
        #对模型下面的所有文章进行索引，生成索引文件
        return self.get_model().objects.all()