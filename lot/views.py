# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http.response import HttpResponse, Http404
from django.template.loader import get_template
from django.template import Context
from django.shortcuts import render_to_response, redirect
from django.core.exceptions import ObjectDoesNotExist
from lot.models import Category, Lot, Lot_pic, Comments_Lot
from forms import CommentForm
from django.core.context_processors import csrf
from django.contrib import auth
from user_app.models import User

def ch_user(request):
    if ("is_auth_ok" in request.session):
        if request.session["is_auth_ok"] == "1":
            user = User.objects.get(id = request.session['user_id'])
            usr = {}
            usr['user_id'] = user.id
            usr['username'] = user.username
            return usr
        else:
            return None
    else:
        return None

def main(request):
	args = {}
	args['categories'] = Category.objects.filter(Category_publick = True)
	args['user'] = ch_user(request)
	return render_to_response('home_and_categories.html', args)

def get_lots(request, Category_id = 1):
	args = {}
	args.update(csrf(request))
	args['user'] = ch_user(request)
	args['Lots'] = Lot.objects.filter(Lot_Category = Category_id).filter(Lot_publick = True).filter(Lot_end = False)
	return render_to_response('in_to_category.html', args)

def get_lot_detail(request, Lot_id=1):
	comment_form = CommentForm
	args = {}
	lot_viv = Lot.objects.get(id = Lot_id)
	lot_viv.Lot_viewv += 1
	lot_viv.save()
	args.update(csrf(request))
	args['user'] = ch_user(request)
	args['lot'] = Lot.objects.get(id=Lot_id)
	args['comments'] = Comments_Lot.objects.filter(comments_for_lot = Lot_id)
	args['images'] = Lot_pic.objects.filter(LotPic_obj = Lot_id)
	args['form'] = comment_form
	return render_to_response('Lot_detail.html', args)

def add_comment(request, Lot_id):
    if request.POST and ("pause" not in request.session):
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit = False)
            comment.comments_for_lot = Lot.objects.get(id = Lot_id)
            form.save()
            request.session.set_expiry(60)
            request.session['pause'] = True
    return redirect('http://localhost:8181/show/show_details/%s/' % Lot_id)

def search(request):
	#if request.method == "GET":
		args = {}
		args['queryset'] = request.GET['search_inquiry']
		args["results"] = Lot.objects.filter(Lot_title = args['queryset']).filter(Lot_publick = True).filter(Lot_end = False)
		return render_to_response('search_result.html', args)
