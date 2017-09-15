from django.db import models
from django.urls import reverse
#User是一个自带的模型类，里面是用户
from django.contrib.auth.models import User
from markdown import Markdown
#除掉标签
from django.utils.html import strip_tags

#类别
class Category(models.Model):
    name = models.CharField(max_length=64)
    # annotate产生的隐藏属性
    def __str__(self):
        return self.name
#标签
class Tag(models.Model):
    name = models.CharField(max_length=64)
    def __str__(self):
        return self.name
#文章
class Post(models.Model):
    title = models.CharField(max_length=64)
    body = models.TextField()
    created_time = models.DateTimeField()
    modified_time = models.DateTimeField()
    # 摘要
    excerpt = models.CharField(max_length=256,blank=True)

    #关系
    category = models.ForeignKey(Category)
    tage = models.ManyToManyField(Tag,blank=True)

    author = models.ForeignKey(User)
    # 阅读量
    views = models.PositiveIntegerField(default=0)
    def increase_views(self):
        self.views += 1
        #update_fields 为只定义一个需要更新的函数
        self.save(update_fields=['views'])
    #看不到的属性comment_set

    # ordering 属性用来指定文章排序方式，['-created_time'] 指定了依据哪个属性的值进行排序
    class Meta:
        ordering = ['-created_time','-modified_time']

    #获取绝对路径
    def get_absolute_url(self):
        return reverse('blog:detail',kwargs={'pk':self.pk})

    def save(self,*args,**kwargs):
        if not self.excerpt:
            md = Markdown(extensions=[
                'markdown.extensions.extra',
                'markdown.extensions.codehilite',
            ])
            # 先将 Markdown 文本渲染成 HTML 文本
            #  strip_tags 去掉 HTML 文本的全部 HTML 标签
            self.excerpt = strip_tags(md.convert(self.body))[:32]
            # 调用父类的 save 方法将数据保存到数据库中
        super().save(*args,**kwargs)

    def __str__(self):
        return self.title