# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response, redirect
from django.http import HttpResponseRedirect
from django.contrib import auth
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.forms import UserCreationForm
from django.core.context_processors import csrf
from django.template import Context, Template
from django.template import RequestContext
from user_app.forms import UserRegForm, User_editForm, inline_Lot_pic_formset, editLotForm, changePasswordForm, addLotPicFormSet, add_my_lotForm
from datetime import datetime
from models import User, messages
from lot.models import Lot, Lot_pic

#=========================================================================

def ch_user(request):
    if ("is_auth_ok" in request.session):
        if request.session["is_auth_ok"] == "1" and request.user.is_authenticated():
            user = User.objects.get(id = request.session['user_id'])
            usr = {}
            usr['user_id'] = user.id
            usr['username'] = user.username
            return usr
        else:
            return None
    else:
        return None

#=========================================================================

def login(request):
    args = {}
    args.update(csrf(request))
    if request.POST:
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(username=username, password=password)        
        if user is not None and user.is_active:
            if user.check_password(password):
                auth.login(request, user)
                request.session["user_id"] = user.id
                request.session["is_auth_ok"] = '1'
                user.last_login = datetime.now()
                return redirect('http://localhost:8181/user/show_profil/')
            else:
                request.session["user_id"] = None
                request.session["is_auth_ok"] = '0'
                args['login_error'] = "Пользователь не найден или заблокирован, обратитесь к Администратору сайта."
                return render_to_response('login.html', args)
        else:
            request.session["is_auth_ok"] = '0'
            request.session["user_id"] = None
            args['login_error'] = "Пользователь не найден или заблокирован, обратитесь к Администратору сайта."
            return render_to_response('login.html', args)
    else:
		return render_to_response('login.html', args)

#=========================================================================

def logout(request):
    request.session["user_id"] = None
    request.session["is_auth_ok"] = '0'
    auth.logout(request)
    return redirect("/")

#=========================================================================

def register(request):
    if request.method == 'POST':
        form = UserRegForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username = form.cleaned_data['username'],
                password = form.cleaned_data['password2'],
                email = form.cleaned_data['email'],
                organization_name = form.cleaned_data['organization_name'],
                adress = form.cleaned_data['adress'],
                requisits = form.cleaned_data['requisits'],
                description = form.cleaned_data['description'],
                telephone = form.cleaned_data['telephone'],
                date_joined = datetime.now(),                                                
            )
            user.is_active = False
            user.save()
            return HttpResponseRedirect('/')
        else:
            err = {}
            err.update(csrf(request))
            err['form'] = form
            err['err'] = u"<p>Введенные Вами данные некорректны</p>"
            return render_to_response('register.html', err)
    else:
        form = UserRegForm()
        args = RequestContext(request, {'form': form})
        return render_to_response('register.html', args) 

#=========================================================================

def self_show_profile(request):
    args= {}
    args.update(csrf(request))
    if ("is_auth_ok" in request.session):
        if request.session["is_auth_ok"] == "1" and request.user.is_authenticated():
            args['this_user'] = User.objects.get(id = request.session["user_id"])
            args['user'] = ch_user(request)
            return render_to_response("self_profile.html", args)
        else:
            args = {}
            args.update(csrf(request))
            args['err']  = "сначала авторизуйтесь"
            return render_to_response('login.html' ,args)
    else:
        args = {}
        args.update(csrf(request))
        args['err']  = "сначала авторизуйтесь"
        return render_to_response('login.html' ,args)
#=========================================================================

def edit_profile(request):
    if ("is_auth_ok" in request.session):
        if request.session["is_auth_ok"] == "1" and request.user.is_authenticated():
            try:
                args = {}
                args.update(csrf(request))
                args['this_user'] = User.objects.get(id = request.session["user_id"])
                args['user'] = ch_user(request)
                data = {
                'org_pic': args['this_user'].org_pic.url,
                'email': args['this_user'].email,
                'organization_name': args['this_user'].organization_name,
                'adress': args['this_user'].adress,
                'requisits': args['this_user'].requisits,
                'description': args['this_user'].description,
                'telephone': args['this_user'].telephone,
                }
                if request.method == 'POST':
                    form_from_request = User_editForm(request.POST, request.FILES)
                    if form_from_request.is_valid():
                        if request.user.is_authenticated():
                            user = User.objects.get(id = request.session["user_id"])
                            user.email = form_from_request.cleaned_data['email']
                            user.organization_name = form_from_request.cleaned_data['organization_name']
                            user.adress = form_from_request.cleaned_data['adress']
                            user.requisits = form_from_request.cleaned_data['requisits']
                            user.description = form_from_request.cleaned_data['description']
                            user.telephone = form_from_request.cleaned_data['telephone']
                            if form_from_request.cleaned_data['org_pic'] is not None:
                                user.org_pic = form_from_request.cleaned_data['org_pic']
                            else:
                                pass
                            user.save()
                            return redirect("http://localhost:8181/user/show_profil/")
                        else:
                            args = {}
                            args.update(csrf(request))
                            args['err']  = "сначала авторизуйтесь"
                            return render_to_response('login.html' ,args)
                    else:                        
                        args['form'] = User_editForm(request)
                        args['err'] = u"Введенные Вами данные неверны, повторите ввод!"
                        return render_to_response("edit_profile.html", args)
                else:
                    args['form'] = User_editForm(data)
                    return render_to_response('edit_profile.html', args)

            except ObjectDoesNotExist:
                args = {}
                args['err'] = "Ошибка при проверке формы"
                return render_to_response('general_error.html', args)
        else:
            args = {}
            args.update(csrf(request))
            args['err']  = "сначала авторизуйтесь"
            return render_to_response('login.html' ,args)
    else:
        args = {}
        args.update(csrf(request))
        args['err']  = "сначала авторизуйтесь"
        return render_to_response('login.html' ,args)

#=========================================================================

def change_password(request):
    args = {}
    args.update(csrf(request))
    if ("is_auth_ok" in request.session):
        if request.session["is_auth_ok"] == "1" and request.user.is_authenticated():
            args['user'] = ch_user(request)
            args['this_user'] = User.objects.get(id = request.session["user_id"])
            if request.method == 'POST':
                form = changePasswordForm(request.POST)
                if form.is_valid():
                    user = User.objects.get(id = request.session["user_id"])
                    if user.check_password(form.cleaned_data['old_password']):
                        user.set_password(form.cleaned_data['password2']) 
                        user.save()
                        username = user.username
                        password = form.cleaned_data['password2']
                        user = auth.authenticate(username=username, password=password)        
                        auth.login(request, user)
                        request.session["user_id"] = user.id
                        request.session["is_auth_ok"] = '1'
                        args["msg"] = "Пароль успешно изменен!"
                        return redirect("http://localhost:8181/user/show_profil/", args)
                    else:
                        args.update(csrf(request))
                        args['form'] = changePasswordForm()
                        args["err"] = "Старый пароль неверен, повторите попытку!"
                        return render_to_response("edit_password.html", args)
                else:
                    args.update(csrf(request))
                    args['form'] = changePasswordForm()
                    args["err"] = "Пароли не совпадают, повторите ввод"
                    return render_to_response("edit_password.html", args)
            else:
                args['form'] = changePasswordForm()
                args['тест'] = request.session["user_id"]
                return render_to_response("edit_password.html", args)
        else:
            args = {}
            args.update(csrf(request))
            args['err']  = "сначала авторизуйтесь"
            return render_to_response('login.html' ,args)
    else:
        args = {}
        args.update(csrf(request))
        args['err']  = "сначала авторизуйтесь"
        return render_to_response('login.html' ,args)


#=========================================================================


def show_me_my_lot(request):
    args = {}
    args.update(csrf(request))
    if ("is_auth_ok" in request.session):
        if request.session["is_auth_ok"] == "1" and request.user.is_authenticated():
            args['user'] = ch_user(request)
            args['this_user'] = User.objects.get(id = request.session["user_id"])
            args['lots'] = Lot.objects.filter( User_creator =  request.session["user_id"])
            args['this_user'] = User.objects.get(id = request.session["user_id"])
            return render_to_response("my_lots.html", args)
        else:
            args = {}
            args.update(csrf(request))
            args['err']  = "сначала авторизуйтесь"
            return render_to_response('login.html' ,args)
    else:
        args = {}
        args.update(csrf(request))
        args['err']  = "сначала авторизуйтесь"
        return render_to_response('login.html' ,args)

#=========================================================================


def add_my_lot(request):
    args = {}
    args.update(csrf(request))
    if ("is_auth_ok" in request.session):
        if request.session["is_auth_ok"] == "1" and request.user.is_authenticated():    
            args['this_user'] = User.objects.get(id = request.session["user_id"])
            args['user'] = ch_user(request)
            if request.method == 'POST':
                form1 = addLotPicFormSet(request.POST, request.FILES)
                form2 = add_my_lotForm(request.POST, request.FILES)
                if form1.is_valid() and form2.is_valid():
                    lot = Lot.objects.create(
                            Lot_title = form2.cleaned_data['Lot_title'],
                            Lot_details = form2.cleaned_data['Lot_details'],
                            Lot_shortName = form2.cleaned_data['Lot_shortName'],
                            Lot_Category = form2.cleaned_data['Lot_Category'],
                            Lot_price = form2.cleaned_data['Lot_price'],
                            Lot_publick = form2.cleaned_data['Lot_publick'],
                            Lot_end = form2.cleaned_data['Lot_end'],
                            Lot_state = form2.cleaned_data['Lot_state'],
                            Lot_main_icon = form2.cleaned_data['Lot_main_icon'],
                            Lot_date = datetime.now(),
                            Lot_discount = False,
                            Lot_popular = False,
                            Lot_like = 0,
                            User_creator = args['this_user'],
                            Lot_viewv = 0,
                        )
                    lot.save()
                    for form in form1:
                        if form.cleaned_data.get('LotPic_title') is not None:
                            if form.cleaned_data.get('LotPic_img') is not None:
                                if form.is_valid():
                                    lot_pic = Lot_pic.objects.create(
                                        LotPic_title = form.cleaned_data['LotPic_title'],
                                        LotPic_img = form.cleaned_data['LotPic_img'],
                                        LotPic_obj = lot,
                                        )
                                    lot_pic.save()
                                else:
                                    args['err'] = u"Вы ввели неверную информацию"
                                    return render_to_response("general_error.html", args)
                            else:
                                args["err"] = u"Вы не выбрали изображение"
                                return render_to_response("general_error.html", args)
                        else:
                            continue
                    return redirect("http://localhost:8181/user/show_me_my_lot/")
                else:
                    args["err"] = "Вы ввели неверную информацию, повторите ввод!"
                    args["form"] = addLotPicFormSet(request.POST, request.FILES)
                    return render_to_response("add_my_lot.html", args)
            else:
                args["form"] = add_my_lotForm
                args["form_pic"] = addLotPicFormSet
                return render_to_response("add_my_lot.html", args)
        else:
            args = {}
            args.update(csrf(request))
            args['err']  = "сначала авторизуйтесь"
            return render_to_response('login.html' ,args)
    else:
        args = {}
        args.update(csrf(request))
        args['err']  = "сначала авторизуйтесь"
        return render_to_response('login.html' ,args)


#=========================================================================


def editLot(request, lot_ids = 1):
    args = {}
    args.update(csrf(request))
    if ("is_auth_ok" in request.session):
        if request.session["is_auth_ok"] == "1" and request.user.is_authenticated():    
            args['this_user'] = User.objects.get(id = request.session["user_id"])
            args['user'] = ch_user(request)
            lot = Lot.objects.get(id = lot_ids)
            if request.method == "POST":
                form = editLotForm(request.POST, request.FILES)
                if form.is_valid():
                    lot.Lot_title = form.cleaned_data['Lot_title']
                    lot.Lot_details = form.cleaned_data['Lot_details']
                    lot.Lot_shortName = form.cleaned_data['Lot_shortName']
                    lot.Lot_Category = form.cleaned_data['Lot_Category']
                    lot.Lot_price = form.cleaned_data['Lot_price']
                    lot.Lot_publick = form.cleaned_data['Lot_publick']
                    lot.Lot_end = form.cleaned_data['Lot_end']
                    lot.Lot_state = form.cleaned_data['Lot_state']
                    if form.cleaned_data["Lot_main_icon"] is not None:
                        lot.Lot_main_icon = form.cleaned_data['Lot_main_icon']
                    lot.save()
                    return redirect("http://localhost:8181/user/show_me_my_lot/")
                else:
                    args["err"] = u"Вы ввели неверные данные!"
                    return render_to_response("general_error.html", args)
            else:
                data = {
                        'Lot_title': lot.Lot_title,
                        'Lot_details': lot.Lot_details,
                        'Lot_shortName': lot.Lot_shortName,
                        'Lot_Category': lot.Lot_Category,
                        'Lot_price': lot.Lot_price,
                        'Lot_publick': lot.Lot_publick,
                        'Lot_end': lot.Lot_end,
                        'Lot_state': lot.Lot_state,
                        'Lot_main_icon': lot.Lot_main_icon.url,
                        'Lot_date': lot.Lot_date,
                        'Lot_discount': lot.Lot_discount,
                        'Lot_popular': lot.Lot_popular,
                        'Lot_like': lot.Lot_like,
                        'User_creator': lot.User_creator,
                        'Lot_viewv': lot.Lot_viewv,
                        }
                args.update(csrf(request))
                args['form'] = editLotForm(data)
                args['form2'] = inline_Lot_pic_formset(instance = lot)
                args['curent_main_icon'] = lot.Lot_main_icon.url
                return render_to_response("edit_lot.html", args)
        else:
                args = {}
                args.update(csrf(request))
                args['err']  = "сначала авторизуйтесь"
                return render_to_response('login.html' ,args)
    else:
        args = {}
        args.update(csrf(request))
        args['err']  = "сначала авторизуйтесь"
        return render_to_response('login.html' ,args)


#=========================================================================


def dellot(request, lot_ids = None):
    args = {}
    args.update(csrf(request))
    if ("is_auth_ok" in request.session):
        if request.session["is_auth_ok"] == "1" and request.user.is_authenticated():    
            args['this_user'] = User.objects.get(id = request.session["user_id"])
            args['user'] = ch_user(request)
            lot_ids = lot_ids.split('_')
            for corent_lot_chek in lot_ids:
                this_lot = Lot.objects.get(id = corent_lot_chek)
                if this_lot.User_creator != args['this_user'] or this_lot.User_creator is None:
                    args["err"] = u"Это не то!"
                    return render_to_response("general_error.html", args) 
            for curent_lot in lot_ids:
                this_lot = Lot.objects.get(id = curent_lot)
                this_lot.delete()

            return redirect("http://localhost:8181/user/show_me_my_lot/")


#=========================================================================


def show_my_req(request, user_id = 0):
    args = {}
    args['seller'] = User.objects.get(id = user_id)
    length = Lot.objects.filter( User_creator =  user_id)
    args['length'] = len(length)
    return render_to_response("show_my_requisits.html", args)

#=========================================================================

def my_messages(request):
    args = {}
    args['user'] = ch_user(request)
    args['this_user'] = User.objects.get(id = request.session["user_id"])
    us_id = User.objects.get(id = request.session["user_id"]).id
    args['my_messages'] = messages.objects.filter(mess_Recipient = us_id)
    args['new_mess_only'] = messages.objects.filter(mess_Recipient = us_id).filter(message_ReadUnread = False)
    args['mess_count'] = len(args['new_mess_only'])
    return render_to_response("my_messages.html", args)

#=======================================================================

def readmessage(request)


































