# coding:utf8

from django.shortcuts import render,reverse,redirect
from django.http import HttpResponse
from article.models import CategoryModel,ArticleModel,CommentModel
from config import PAGE_NUM
from mutils import phjson
from django.views.decorators.http import require_http_methods
from forms import FrontRegistForm,FrontLoginForm,\
    FrontEmailForm,FrontResetPwd,AddCommentForm
from django.core.cache import cache
from mutils.phemail import send_email
from frontauth.models import FrontUserModel
from frontauth.utils import login,logout
from frontauth.decorators import front_login_require
from django.db.models import Q
from django.db.models import Count

def article_list(request,category_id=0,page=1):
    categorys = CategoryModel.objects.all()
    articles = ArticleModel.objects.all().order_by('-create_time')
    articles = articles.annotate(comment_num=Count('commentmodel'))
    page = int(page)
    category_id = int(category_id)
    top_articles = None
    if category_id > 0:
        articles = articles.filter(category__pk=category_id)
        articles = articles.values()
    else:
        top_articles = articles.filter(top__isnull=False).order_by('-top__create_time')[:3]
        articles = [article for article in articles.values() if article not in top_articles.values()]
    start = (page-1)*PAGE_NUM
    end = start + PAGE_NUM
    articles = list(articles[start:end])
    context = {
        'articles':articles,
        'c_page':page,
    }
    if request.is_ajax():
        return phjson.json_result(data=context)
    else:
        context['categorys'] = categorys
        context['top_articles'] = top_articles
        context['c_category'] = CategoryModel.objects.filter(pk=category_id).first()
        return render(request,'front_article_list.html',context)

def article_detail(request,article_id=''):
    if article_id:
        article = ArticleModel.objects.filter(pk=article_id).first()
        if article:
            comments = article.commentmodel_set.all()
            context = {
                'article':article,
                'categorys':CategoryModel.objects.all(),
                'c_category_id':article.category.id,
                'tags':article.tags.all(),
                'comments':comments
            }
            return render(request, 'front_article_detail.html',context)

        else:
            return phjson.json_params_error('文章id输入错误')

    return phjson.json_params_error('文章id不能为空')

@require_http_methods(['GET','POST'])
def front_login(request):
    if request.method == 'GET':
        return render(request,'front_login.html')
    else:
        form = FrontLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = login(request,email,password)
            if user:
                remember = form.cleaned_data.get('remember')
                next_url = request.GET.get('next')
                session_ex = None
                if not remember:
                    session_ex = 0
                request.session.set_expiry(session_ex)
                if next_url:
                    return redirect(next_url)
                else:
                    return redirect(reverse('front_index'))
            else:
               return render(request, 'front_login.html', {'error': u'用户名或密码错误'})
        else:
            return render(request, 'front_login.html',{'error':form.get_error()})

@require_http_methods(['GET','POST'])
def regist(request):
    if request.method == 'GET':
        return render(request,'front_regist.html')
    else:
        form = FrontRegistForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            data = {
                'email':email,
                'username':username,
                'password':password
            }
            subject = u'注册我的博客'
            message = u'请点击以下链接确认注册我的博客 '
            if send_email(request,email,'front_check_email',data,subject,message):
                return HttpResponse(u'邮箱发送成功')
            else:
                return HttpResponse(u'邮箱发送失败')
        else:
            return render(request,'front_regist.html',{'error':form.get_error()})

def check_email(request,code):
    data = cache.get(code)
    email = data.get('email')
    username = data.get('username')
    password = data.get('password')
    user = FrontUserModel.objects.filter(email=email).first()
    if user:
        return HttpResponse(u'注册失败，邮箱已存在')

    user = FrontUserModel(email=email,password=password,username=username)
    user.save()
    return HttpResponse(u'注册成功')

@require_http_methods(['GET','POST'])
def forget_password(request):
    if request.method == 'GET':
        return render(request,'front_forget_pwd.html')
    else:
        form = FrontEmailForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            user = FrontUserModel.objects.filter(email=email).first()
            if user:
                if send_email(request,email,'front_reset_password'):
                    return HttpResponse(u'邮箱发送成功')
                else:
                    return HttpResponse(u'邮箱发送失败')
            else:
                return HttpResponse(u'没有该用户')
        else:
            return render(request, 'front_forget_pwd.html',{'error':form.get_error()})

@require_http_methods(['GET','POST'])
def reset_password(request,code):
    if request.method == 'GET':
        return render(request,'front_reset_password.html')
    else:
        form = FrontResetPwd(request.POST)
        if form.is_valid():
            password = form.cleaned_data.get('password')
            email = cache.get(code)
            user = FrontUserModel.objects.filter(email=email).first()
            if user:
                user.password = password
                return HttpResponse(u'密码修改成功')
            else:
                return render(request, 'front_reset_password.html',{'error':u'用户不存在'})
        return render(request,'front_reset_password.html',{'error':form.get_error()})

#评论
@require_http_methods(['POST'])
@front_login_require
def front_comment(request):
    form = AddCommentForm(request.POST)
    if form.is_valid():
        article_id = form.cleaned_data.get('article_id')
        content = form.cleaned_data.get('content')
        article = ArticleModel.objects.filter(pk=article_id).first()
        if not article:
            return phjson.json_params_error(u'没有该文章')
        comment = CommentModel(article=article,content=content,author=request.front_user)
        comment.save()
        return redirect(reverse('front_article_detail',kwargs={'article_id':article_id}))
    else:
        return phjson.json_params_error(form.get_error())

@require_http_methods(['GET'])
def search(request):
    query = request.GET.get('query')
    articles = ArticleModel.objects.filter(Q(title__icontains=query)|Q(content__icontains=query))
    categorys = CategoryModel.objects.all()
    articles = articles.annotate(comment_num=Count('commentmodel'))
    context = {
        'articles':articles,
        'categorys':categorys,
        'hide_load':True
    }
    return render(request,'front_article_list.html',context)

