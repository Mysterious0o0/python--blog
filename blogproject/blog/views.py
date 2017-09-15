from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse
from .models import Post,Category,Tag
from comment.forms import CommentForm
#通用视图
from django.views.generic import ListView,DetailView
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
    paginate_by = 2


    def pagination_data(self,paginator,page,is_paginated):
        if not is_paginated:
            return {}
        first = False              # 首页
        left_has_more = False      # 省略号
        left = []                  # 当前页左边的页码
        page_number = page.number  # 当前页
        right = []                 # 当前页右边的页码
        right_has_more = False     # 省略号
        last = False               # 最后一页

        total_pages = paginator.num_pages# 总页数

        page_range = paginator.page_range# 获取整个分页的列表
        # 如果当前页为第一页
        if page_number == 1:
            right = page_range[page_number:page_number+2]
            if right[-1]<total_pages-1:
                right_has_more = True
            if right[-1]<total_pages:
                last = True
        # 如果当前是最后一页
        elif page_number == total_pages:
            left = page_range[(page_number-3) if(page_number-3)>0 else 0:page_number-1]
            if left[0]>2:
                left_has_more = True
            if left[0]>1:
                first = True
        # 中间页
        else:
            left = page_range[(page_number-3) if (page_number-3)>0 else 0:page_number-1]
            right = page_range[page_number:page_number+2]
            if right[-1]<total_pages-1:
                right_has_more = True
            if right[-1]<total_pages:
                last = True

            if left[0]>2:
                left_has_more = True
            if left[0]>1:
                first = True

        data = {
            'left':left,
            'right':right,
            'left_has_more':left_has_more,
            'right_has_more':right_has_more,
            'first':first,
            'last':last
        }
        return data

    def get_context_data(self,**kwargs):
        # 首先获取基类get_context_data()返回的context
        context = super().get_context_data(**kwargs)
        paginator = context.get('paginator')
        page = context.get('page_obj')
        is_paginated = context.get('is_paginated')
        paginator_data = self.pagination_data(paginator,page,is_paginated)

        context.update(paginator_data)
        return context







class ArchivesViews(IndexView):
    def get_queryset(self):
        # get_queryset()是调用父类的方法，直接返回所有数据
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

# def detail(request,pk):
#     post = get_object_or_404(Post,pk=pk)
#     post.increase_views()
#     post.body = markdown.markdown(post.body,extensions = [
#         'markdown.extensions.extra',
#         'markdown.extensions.codehilite',
#         'markdown.extensions.toc',
#     ])
#     form = CommentForm()
#     comment_list = post.comment_set.all()
#     context = {
#         'post':post,
#         'form':form,
#         'comment_list':comment_list
#     }
#     return render(request,'blog/detail.html',context=context)

class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/detail.html'
    context_object_name = 'post'
    def get(self,request,*args,**kwargs):
        # 获取单个文章，覆用父类的get方法，而get_queryset方法是覆用父类获取所有文章列表的
        response = super().get(request,*args,**kwargs)
        # self.object实际上是post的对象
        #为了调用post里的increase_views()方法使阅读量加一
        self.object.increase_views()
        return response

    def get_object(self, queryset=None):
        post = super().get_object(queryset)
        post.body = markdown.markdown(post.body,extensions = [
                'markdown.extensions.extra',
                'markdown.extensions.codehilite',
                'markdown.extensions.toc',
        ])
        return post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = CommentForm()
        # 下面的self.object()必须返回post才行
        comment_list = self.object.comment_set.all()
        context.update({#context已有post，所以只需要更新就好
            'form':form,
            'comment_list':comment_list
        })
        return context

class TagView(IndexView):
    def get_queryset(self):
        tag = get_object_or_404(Tag,pk=self.kwargs.get('pk'))
        return super().get_queryset().filter(tage=tag)