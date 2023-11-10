from django.shortcuts import render,redirect,get_object_or_404
#from django.http import HttpResponse
from django.views import View
from .models import Post
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import PostUpdateForm
from django.utils.text import slugify
# Create your views here.
class Home(View):
    def get(self,request):
        posts=Post.objects.order_by('created')
        return render(request,'home/index.html',{'posts':posts})


class Post_detail(View):
    def get(self,request,post_id,post_slug):
       
        post=get_object_or_404(Post,pk=post_id,slug=post_slug)
        return render(request,'home/detail.html',{'post':post})
    

class Delete(LoginRequiredMixin,View):
    def get(self,request,post_id):
        
        post=get_object_or_404(Post,pk=post_id)
        if post.user.id==request.user.id:
            post.delete()
            messages.success(request,'Post deleted')
        else:
            messages.error(request,'This post can not be deleted!')   
        return redirect('home:home')     

class Update(LoginRequiredMixin,View):
    form_class=PostUpdateForm
    def get(self,request,post_id):
        
        post=get_object_or_404(Post,pk=post_id)
        form=self.form_class(instance=post)
        if not post.user.id==request.user.id:
            messages.error(request,'This post can not be updated!')
            return redirect('home:home')
        else:
            return render(request,'home/update.html',{'form':form})
    def post(self,request,post_id):
        post=Post.objects.get(pk=post_id)
        form=self.form_class(request.POST,instance=post)
        if not post.user.id==request.user.id:
            messages.error(request,'This post can not be updated!')
            return redirect('home:home')
        else:
            if form.is_valid():
                new_post=form.save(commit=False)
                new_post.slug=slugify(form.cleaned_data['body'][:30])
                new_post.save()
                messages.success(request,'Post has been updated')
                return redirect('home:post_detail',post.id,post.slug)

class Create(LoginRequiredMixin,View):
    form_class=PostUpdateForm
    def get(self,request):
        form=self.form_class()
        return render(request,'home/create.html',{'form':form})
    def post(self,request):
        
        form=self.form_class(request.POST)

        if form.is_valid():
            new_post=form.save(commit=False)
            new_post.slug=slugify(form.cleaned_data['body'][:30])
            new_post.user=request.user
            new_post.save()
            messages.success(request,'Post has been created')
            return redirect('home:post_detail',new_post.id,new_post.slug)
