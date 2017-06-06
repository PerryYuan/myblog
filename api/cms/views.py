# coding:utf8
from django.shortcuts import render,redirect,reverse
from django.http import HttpResponse,JsonResponse
from forms import LoginForm,UpdateProfileForm,UpdateEmailForm,\
    AddCategoryForm,AddTagForm,AddArticleForm,\
    UpdateArticleForm,DeleteArticleForm,TopArticleForm,\
    CategoryForm,CategoryEditerForm

from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from cmsauth.models import CMSUser
from django.core.cache import cache
from django.core import mail
import hashlib
import time
import qiniu
from article.models import CategoryModel,ArticleModel,TagModel,TopModel
from mutils import phjson
import config
from django.db.models import Count
from mutils.phemail import send_email

@login_required
def article_manage(request,page=1,category_id=0):
    articles = None
    categorys = CategoryModel.objects.all()
    category_id = int(category_id)
    print category_id
    if category_id > 0:
        articles = ArticleModel.objects.filter(category__pk=category_id).all().order_by('-top__create_time', '-create_time')
    else:
        articles = ArticleModel.objects.all().order_by('-top__create_time', '-create_time')
    c_page = int(page)
    PAGE_NUM = config.PAGE_NUM
    t_page = articles.count()/PAGE_NUM
    if articles.count() % PAGE_NUM > 0:
        t_page += 1
    start = (c_page-1)*PAGE_NUM
    end = start+PAGE_NUM
    articles = articles[start:end]

    page = c_page-1
    pages = []
    while page%5>0 and page<c_page:
        pages.append(page)
        page -= 1
    page = c_page
    while page<=t_page:
        pages.append(page)
        if page % 5 == 0:
            break
        page += 1
    pages.sort()
    context = {
        'articles':articles,
        'pages':pages,
        't_page':t_page,
        'c_page':c_page,
        'categorys':categorys,
        'c_category':category_id
    }
    return render(request,'article_manage.html',context)

@login_required
@require_http_methods(['GET','POST'])
def add_article(request):
    if request.method == 'GET':
        categorys = CategoryModel.objects.all()
        tags = TagModel.objects.all()
        context = {
            'categorys':categorys,
            'tags':tags
        }
        return render(request,'add_article.html',context)
    else:
        form = AddArticleForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data.get('title')
            category = form.cleaned_data.get('category')
            desc = form.cleaned_data.get('desc')
            thumbnail = form.cleaned_data.get('thumbnail')
            tags = request.POST.getlist('tags[]')
            print '-'*30
            print tags
            print '-'*30
            content = form.cleaned_data.get('content')
            categoryModel = CategoryModel.objects.get(pk=category)
            article = ArticleModel(title=title,
                         desc=desc,
                         thumbnail=thumbnail,
                         category=categoryModel,
                         content=content,
                         author=request.user)
            article.save()
            if tags:
                for tag in tags:
                    tag = TagModel.objects.get(pk=tag)
                    if tag:
                        article.tags.add(tag)
            return phjson.json_result()
        else:
            return phjson.json_params_error(form.get_error())

@login_required
@require_http_methods(['GET','POST'])
def update_article(request,pk=''):
    if request.method == 'GET':
        categorys = CategoryModel.objects.all()
        tags = TagModel.objects.all()
        article = ArticleModel.objects.filter(pk=pk).first()
        tag_ids = []
        if article.tags.all().count()>0:
            tag_ids = [tag.id for tag in article.tags.all()]
        context = {'categorys': categorys,
                   'tags': tags,
                   'article':article,
                   'tag_ids':tag_ids
                   }
        return render(request, 'article_update.html', context)
    else:
        form = UpdateArticleForm(request.POST)
        if  form.is_valid():
            uid = form.cleaned_data.get('uid')
            article = ArticleModel.objects.filter(uid=uid).first()
            if article:
                title = form.cleaned_data.get('title')
                category = form.cleaned_data.get('category')
                desc = form.cleaned_data.get('desc')
                thumbnail = form.cleaned_data.get('thumbnail')
                tags = request.POST.getlist('tags[]')
                content = form.cleaned_data.get('content')
                categoryModel = CategoryModel.objects.get(pk=category)

                article.title = title
                article.desc = desc
                article.thumbnail = thumbnail
                article.content = content
                article.category = categoryModel
                article.tags.clear()
                article.save()

                if tags:
                    for tag in tags:
                        tag = TagModel.objects.get(pk=tag)
                        if tag:
                            article.tags.add(tag)
                return phjson.json_result()
        else:
            return phjson.json_params_error(form.get_error())

@login_required
@require_http_methods(['POST'])
def add_category(request):
    form = AddCategoryForm(request.POST)
    if form.is_valid():
        name = form.cleaned_data.get('name',None)
        if CategoryModel.objects.filter(name=name).first():
            return phjson.json_params_error(message=u'分类已存在，不需要再次添加')
        category = CategoryModel(name=name)
        category.save()
        return phjson.json_result(data={'id':category.id,'name':category.name})
    else:
        return phjson.json_params_error(message=form.get_error())

@login_required
@require_http_methods(['POST'])
def add_tag(request):
    form = AddTagForm(request.POST)
    if form.is_valid():
        name = form.cleaned_data.get('name')
        if TagModel.objects.filter(name=name).first():
            return phjson.json_params_error(u'标签名已存在，无需再次添加')
        tag = TagModel(name=name)
        tag.save()
        data = {'id':tag.id,'name':tag.name}
        print '*'*30
        print data
        print '*' * 30
        return phjson.json_result(data=data)
    else:
        return phjson.json_params_error(form.get_error())


def cms_login(request):
    if request.method == "GET":
        return render(request,'cms_login.html')
    else:
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username',None)
            password = form.cleaned_data.get('password',None)
            remember = form.cleaned_data.get('remember',None)
            user = authenticate(username=username,password=password)
            if user:
                login(request,user)
                session_ex = None
                if not remember:
                    session_ex = 0
                request.session.set_expiry(session_ex)
                nextUrl = request.GET.get('next',None)
                if nextUrl:
                    return redirect(nextUrl)
                return redirect(reverse('cms_index'))
            return render(request,'cms_login.html',{'error':u'用户名或密码错误'})
        else:
            return render(request,'cms_login.html',{'error':form.get_error()})

@login_required
def cms_setting(request):
    return render(request,'cms_setting.html')

@login_required
@require_http_methods(['POST'])
def update_profile(request):
    form = UpdateProfileForm(request.POST)
    if form.is_valid():
        username = form.cleaned_data.get('username',None)
        avatar = form.cleaned_data.get('avatar',None)
        user = request.user
        if username != user.username:
            user.username = username
            user.save()
        if  avatar:
            cms_user = CMSUser.objects.filter(user__pk=user.pk).first()
            if not cms_user:
                cms_user = CMSUser(avatar=avatar, user=user)
            elif cms_user.avatar != avatar:
                cms_user.avatar = avatar
            cms_user.save()
        return phjson.json_result()
    else:
        return phjson.json_params_error(message=form.get_error())

@login_required
@require_http_methods(['GET'])
def send_email_ok(request):
    return render(request,'cms_emailsuccess.html')

@login_required
@require_http_methods(['GET'])
def send_email_fail(request):
    return render(request, 'cms_emailfail.html')

@login_required
@require_http_methods(['GET','POST'])
def update_email(request):
    if request.method == 'GET':
        return render(request,'update_email.html')
    else:
        form = UpdateEmailForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            if send_email(request,email,'cms_check_email'):
                return redirect(reverse('cms_send_email_ok'))
            return redirect(reverse('cms_send_email_fail'))
        else:
            return render(request,'update_email.html',{'error':form.get_error()})


@require_http_methods(['GET'])
def qiniu_token(request):
    # 1. 先要设置AccessKey和SecretKey
    access_key = "N9R_gvgX9GoeyvAjDYlgIzMDXVvsvHFjMPW_0o23"
    secret_key = "aCY_SAqTIyQI3h0sQskSnYPQO2Z1iXTKh_Osio3g"
    # 2. 授权
    q = qiniu.Auth(access_key, secret_key)
    # 3. 设置七牛空间
    bucket_name = 'myblog'
    # 4. 生成token
    token = q.upload_token(bucket_name)
    # 5. 返回token,key必须为uptoken
    return JsonResponse({'uptoken': token})
    return phjson.json_result(kwargs={'uptoken':token})

@login_required
@require_http_methods(['GET'])
def check_email(request,code):
    email = cache.get(code)
    if email:
        user = request.user
        user.email = email
        user.save(update_fields=['email'])
        return redirect(reverse('cms_index'))
    else:
        return HttpResponse(u'邮箱验证过期')

def cms_logout(request):
    logout(request)
    return redirect(reverse('cms_login'))

# @login_required
@require_http_methods(['POST'])
def delete_article(request):
    form = DeleteArticleForm(request.POST)
    if form.is_valid():
        uid = form.cleaned_data.get('uid')
        article = ArticleModel.objects.get(pk=uid)
        if article:
            article.delete()
            return phjson.json_result()
        else:
            return phjson.json_params_error(u'该文章不存在')
    else:
        return phjson.json_params_error(form.get_error())

@require_http_methods(['POST'])
def top_article(request):
    form = TopArticleForm(request.POST)
    if form.is_valid():
        uid = form.cleaned_data.get('uid')
        article = ArticleModel.objects.get(pk=uid)
        if article:
            top = article.top
            if not top:
                top = TopModel()
            top.save()

            article.top = top
            article.save(update_fields=['top'])
            return phjson.json_result()
        else:
            return phjson.json_params_error(u'该文章不存在')
    else:
        return phjson.json_params_error(form.get_error())

@require_http_methods(['POST'])
def untop_article(request):
    form = TopArticleForm(request.POST)
    if form.is_valid():
        uid = form.cleaned_data.get('uid')
        article = ArticleModel.objects.get(pk=uid)
        if article:
            top = article.top
            if not top:
                return phjson.json_params_error(u'该文章没有置顶')
            article.top.delete()
            return phjson.json_result()
        else:
            return phjson.json_params_error(u'该文章不存在')
    else:
        return phjson.json_params_error(form.get_error())

#分类
@login_required
@require_http_methods(['GET'])
def category_manage(request):
    categorys = CategoryModel.objects.all().annotate(article_num=Count('articlemodel'))
    print categorys
    context = {
        'categorys':categorys
    }
    return render(request,'category_manage.html',context)

@login_required
@require_http_methods(['POST'])
def category_editer(request):
    form = CategoryEditerForm(request.POST)
    if form.is_valid():
        id = form.cleaned_data.get('id')
        category = CategoryModel.objects.filter(pk=id).first()
        if category:
            name = form.cleaned_data.get('name')
            category.name = name
            category.save(update_fields=['name'])
            return phjson.json_result()
        else:
            return phjson.json_params_error(u'该分类不存在')
    else:
        return phjson.json_params_error(form.get_error())

@login_required
@require_http_methods(['POST'])
def category_delete(request):
    form = CategoryForm(request.POST)
    if form.is_valid():
        id = form.cleaned_data.get('id')
        category = CategoryModel.objects.filter(pk=id).first()
        if category:
            if category.articlemodel_set.count()<=0:
                category.delete()
                return phjson.json_result()
            else:
                return phjson.json_params_error(u'该分类存在数据不能删除')
        else:
            return phjson.json_params_error(u'该分类不存在')
    else:
        return phjson.json_params_error(form.get_error())