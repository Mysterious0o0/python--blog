from django.shortcuts import render,get_object_or_404,redirect

# Create your views here.
from blog.models import Post

from .forms import CommentForm

def post_comment(request,post_pk):
    #获得要评论的文章
    post = get_object_or_404(Post,pk=post_pk)
    if request.method =='POST':
        form = CommentForm(request.POST)# 实例化表单对象
        if form.is_valid():
            comment = form.save(commit=False)#有表单对象得到模型对象???????
            #commit=False:不直接存到数据库中
            comment.post = post
            comment.save()
            # 可以直接重定向到post模型对象之中
            # 因为指定了get_absolute_url
            return redirect(post)
        else:
            #获取文章已有评论
            comment_list = post.comment_set.all()
            '''
            post 和 comment是一对多的关系，一个post有多个comment，故可以通过反向查找来获取post下的属性
            '''
            context = {
                'post': post,
                'form': form,
                'comment_list':comment_list,
            }
            return render(request,'blog/detail.html',locals())
    # 不是 post 请求，说明用户没有提交数据，重定向到文章详情页。
    return redirect(post)