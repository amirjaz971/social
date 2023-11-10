from django.shortcuts import render,redirect,get_object_or_404,get_list_or_404
from django.views import View
from .forms import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from home.models import Post
from .models import Relation
# Create your views here.
class Register(View):
    form_class=Register_form
    template_name='account/register.html'
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)
    
    def get(self,request):
        form=self.form_class()
        return render(request,self.template_name,{'form':form})
    def post(self,request):
        
        form=self.form_class(request.POST)
        if form.is_valid():
            cd=form.cleaned_data
            User.objects.create_user(cd['username'],cd['email'],cd['password'])
            messages.success(request,'Registered successfully!','success')
            return redirect('home:home')
        return render(request,self.template_name,{'form':form})


class User_login(View):
    form_class=Login_form
    template_name='account/login.html'
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)    
    def get(self,request):
        form=self.form_class()
        return render(request,self.template_name,{'form':form})
    def post(self,request):
        form=self.form_class(request.POST)
        if form.is_valid():
            cd=form.cleaned_data
            user=authenticate(request,username=cd['username'],password=cd['password'])
            if user is not None:
                login(request,user)
                messages.success(request,'Logged in successfully!','success')
                return redirect('home:home')
            
        return render(request,self.template_name,{'form':form})    
    

class User_logout(LoginRequiredMixin,View):
    #login_url='/account/login'
    def get(self,request):
        logout(request)
        messages.success(request,'logged out successfully')
        return redirect('home:home')   
    
class User_profile(LoginRequiredMixin,View):
    def get(self,request,user_id):
        is_following=False
        user=get_object_or_404(User,pk=user_id)
        posts=Post.objects.filter(user=user) 
        relation=Relation.objects.filter(from_user=request.user,to_user=user)
        if relation.exists():
            is_following=True


        return render(request,'account/profile.html',{'user':user,'posts':posts,'is_following':is_following}) 
     

class Follow(LoginRequiredMixin,View):
    def get(self,request,user_id):
        user=User.objects.get(pk=user_id)
        relation=Relation.objects.filter(from_user=request.user,to_user=user)
        if relation.exists():
            messages.error(request,'you already followed this user!')
        else:
            Relation(from_user=request.user,to_user=user).save()   
            messages.success(request,'You followed the user')
        return redirect('account:profile',user_id)     
class Unfollow(LoginRequiredMixin,View):
    def get(self,request,user_id):
        user=User.objects.get(pk=user_id)
        relation=Relation.objects.filter(from_user=request.user,to_user=user)
        if relation.exists():
            relation.delete()
            messages.success(request,'you unfollowed this user')
        else:
            messages.error(request,'you are not following this user')
        return redirect('account:profile',user_id)        