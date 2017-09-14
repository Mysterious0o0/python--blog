from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse
from .models import Post,Category
from comment.forms import CommentForm
#通用视图
from django.views.generic import ListView
# Create your views here.
import markdown
# def index(request):
#     # return HttpResponse('<h1> hello Django<h1>')
#     post_list = Post.objects.all().order_by('-created_time')#按时间先后排序，新的在前，把负号去了，就旧的在前.order_by('')按什么排序
#     return render(request,'blog/index.html',context={'post_list':post_list})

class IndexView(ListView):
    '''
    model：将 model 指定为 Post，告诉 Django 我要获取的模型是 Post。 
    template_name：指定这个视图渲染的模板。 
    context_object_name：指定获取的模型列表数据保存的变量名。这个变量会被传递给模板。
    '''
    model = Post
    template_name = 'blog/index.html'
    #这个名字不能随便取，必须和模板中的变量相同
    context_object_name = 'post_list'

def detail(request,pk):
    post = get_object_or_404(Post,pk=pk)
    post.increase_views()
    post.body = markdown.markdown(post.body,extensions = [
        'markdown.extensions.extra',
        'markdown.extensions.codehilite',
        'markdown.extensions.toc',
    ])
    form = CommentForm()
    comment_list = post.comment_set.all()
    context = {
        'post':post,
        'form':form,
        'comment_list':comment_list
    }
    return render(request,'blog/detail.html',context=context)

class ArchivesViews(IndexView):
    def get_queryset(self):
        # 一定要注意created_time__year ：两个下划线
        return super().get_queryset().filter(
            created_time__year = self.kwargs.get('year'),
            created_time__month = self.kwargs.get('month')
        )

# def archives(request,year,month):
#     post_list = Post.objects.filter(created_time__year = year,created_time__month = month)
#     # print(post_list)
#     return render(request,'blog/index .html',context={'post_list': post_list})

class CategoryView(IndexView):
    def get_queryset(self):
        cate = get_object_or_404(Category,pk=self.kwargs.get('pk'))
        # 下面的filter(category = cate)中的category是post.category
        return super().get_queryset().filter(category = cate)