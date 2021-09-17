# import pyrebase
# from datetime import datetime
# import math
# from django.contrib import auth
# from django.shortcuts import render, redirect
# from django.views.generic import TemplateView
# import firebase_admin
# from firebase_admin import credentials, firestore, auth
# import os
# # from .models import InventIn
# from django.http import HttpResponse
# # Create your views here.

import pyrebase
import math
from datetime import datetime
from django.contrib import auth
from django.template.loader import get_template
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
import firebase_admin
from firebase_admin import credentials, firestore, auth
from django.http import HttpResponse
import os
from xhtml2pdf import pisa
# from .models import InventIn
from django.http import HttpResponse


cred = credentials.Certificate("projectse-3b85c-firebase-adminsdk-zhqmv-178e227a95.json")
firebase_admin.initialize_app(cred)

config = {
    'apiKey': "AIzaSyBxmyEc-J_8JNxppZDWIBaEjnDrIPnhcbs",
    'authDomain': "projectse-3b85c.firebaseapp.com",
    'databaseURL': "https://projectse-3b85c-default-rtdb.firebaseio.com",
    'projectId': "projectse-3b85c",
    'storageBucket': "projectse-3b85c.appspot.com",
    'messagingSenderId': "292422960816",
    'appId': "1:292422960816:web:8847eaccf3af2d5b339d75",
    'measurementId': "G-PSY0SCZ38F"
}

firebase = pyrebase.initialize_app(config)
authe = firebase.auth()
db = firestore.client()
storage = firebase.storage()

userid = ''
positions=''
user_check=''
def home(request):
    return render(request,"home.html")


def logout(request):
    global userid
    firebase_admin.auth.revoke_refresh_tokens(userid, app=None)
    userid = ''
    return redirect('home')

def login(request):
    return render(request,"login.html")


def myprofile(request):
    global userid
    global positions
    global user_check
    uid = userid
    user_ref = db.collection('users').document(uid)
    user_dict = user_ref.get().to_dict()
    firstname = user_dict['firstname']
    lastname = user_dict['lastname']
    phone = user_dict['phone']
    position = user_dict['position']
    email = user_dict['email']
    user_id = user_dict['id']

    positions = position
    user_check=user_id
    # ====================================================
    # part Dowload
    str_bl = "\\"
    path_on_clound = ("images/" + user_id + ".jpg")
    path_on_pc = ("img/empic/" + user_id + ".jpg")
    # storage.child(path_on_clound).download("empic/M008.jpg")
    print("======== Dowload ID :" + user_id + " success!! ========")
    # ====================================================

    str_bl = ("\\")
    pic_id_1 = ("empic/" + user_id + ".jpg")
    print("=== read Picture Profile as : === >>> " + pic_id_1)
    print("=== read Profile id as      : === >>> " + user_id)

    return render(request, "myprofile.html", {
                                                'firstname': firstname,
                                                'lastname': lastname,
                                                'email': email,
                                                'id': user_id,
                                                'phone': phone,
                                                'position': position,
                                                'pic_id': pic_id_1})

def profile(request):
    global user_check
    user_id = request.GET.get('id')
    user_ref = db.collection('users').where('id','==',user_id).stream()
    u = ''
    for user in user_ref:
        u = user.to_dict()
    firstname = u['firstname']
    lastname = u['lastname']
    email = u['email']
    phone = u['phone']
    position = u['position']

    # #====================================================
    #part Dowload
    path_on_clound  =  ("images/" +user_id+ ".jpg")
    #path_on_pc      =  ("img/empic/"+user_id+".jpg")
    path_on_pc      =  ("img/empic/"+user_id+".jpg")
    storage.child(path_on_clound).download(path_on_pc)
    print ("======== Dowload ID :" +user_id+"success!! ========")
    # #====================================================

    userid_pc = ("empic/"+user_id+".jpg")
    print ("User_Id : "+user_id)
    print ("Load User ID from  : "+ userid_pc )
    return render(request, "profile.html", {"firstname" : firstname,
                                            "lastname"  : lastname,
                                            "id"        : user_id,
                                            "position"  : position,
                                            "email"     : email,
                                            "phone"     : phone,
                                            "pic_id"    : userid_pc,
                                            "user_check" : user_check})

def profileedit(request):
    user_id = request.GET.get('id')
    user_ref = db.collection('users').where('id','==',user_id).stream()
    u = ''
    for user in user_ref:
        u = user.to_dict()
    firstname = u['firstname']
    lastname = u['lastname']
    email = u['email']
    phone = u['phone']
    position = u['position']
    return render(request, "profileedit.html", {"firstname": firstname,"lastname": lastname, "id": user_id, "position": position,"email": email, "phone": phone})


def editprofile(request):
    firstname = request.POST.get('firstname').lower()
    lastname = request.POST.get('lastname').lower()
    phone = request.POST.get('phone')
    email = request.POST.get('email')
    password = request.POST.get('password')
    position = request.POST.get('position')
    add_photo = request.POST.get('add_photo')
    user_id = request.POST.get('id')

    if add_photo == "":
        #====================================================
        #part Dowload
        path_on_clound = "images/" + user_id + ".jpg"
        spath_on_pc = "img/empic/" + user_id + ".jpg"
        storage.child(path_on_clound).download(spath_on_pc)
        print ("======== Dowload success!! ========")
        print (" User ID : " + user_id )
        #====================================================
    else :
        #====================================================
        print (add_photo)
        #part upload
        strjpg = ".jpg"
        path_on_clound = "images/" + add_photo
        path_on_pc = "img/empic/" + str(add_photo)
        if add_photo != "":
            auto_p = os.path.abspath(path_on_pc)
            print("======Name Upload======  : -> "+add_photo)
            print("======Path Upload======  : -> "+auto_p)
            print("=======================  : -> "+auto_p)
            storage.child(path_on_clound).put(path_on_pc)
            print ("======== Upload success!! ========")
        else:
            print ("======== Not Upload!! ========")
        #====================================================

    user_ref = db.collection('users').where('id', '==', user_id).stream()
    uid = ''
    for user in user_ref:
        uid = user.id
    user_ref = db.collection('users').document(uid)

    try:
        user_ref.update(
            {"firstname": firstname, "lastname": lastname, "phone": phone, "position": position, "email": email})
        auth.update_user(uid, email=email)
        if password != '':
            auth.update_user(uid, password=password)
    except:
        print("Error")
    return redirect("/HR/")

def remove_user(request):
    try:
        user_id = request.GET.get('id')
        user_ref = db.collection('users').where('id', '==', user_id).stream()
        uid = ''
        for user in user_ref:
            uid = user.id
        user_ref = db.collection('users').document(uid)
        user_ref.update({"status": "un_employed"})
        auth.delete_user(uid)
        print(user_id)
        print(uid)
    except:
        print("Remove Error")
    return redirect("/HR/")

def hr(request):
    users_gen = db.collection('users').where('status','==','employed').stream()
    users_list = []
    global userid
    currect_user_ref = db.collection('users').document(userid)
    current_user_dict = currect_user_ref.get().to_dict()
    current_user_id = current_user_dict['id']

    for user in users_gen:
        dic = user.to_dict()
        users_list.append(user.to_dict())
    return render(request,"HR.html", {'users_list': users_list})

def history(request):
    global positions
    print("history",positions)
    trans = db.collection('transference').where('status', '!=', 'wait_for_checking').stream()
    history_list = []
    for tran in trans:
        tran_dict = tran.to_dict()

        if tran_dict['status'] == 'out_warehouse':

            product_id_list = []
            product_amount_list = []
            product_area_list = []

            for product_id in tran_dict['products_id']:
                product_id_list.append(product_id)
            for product_amount in tran_dict['products_val']:
                product_amount_list.append(product_amount)
            for product_area in tran_dict['area']:
                product_area_list.append(product_area)

            for i in range(len(product_amount_list)):
                product_info_gen = db.collection('products_info').where('product_id', '==', product_id_list[i]).stream()
                for product_info in product_info_gen:
                    product_name = (product_info.to_dict()['product_name'])
                    product_note = (product_info.to_dict())['note']
                history_data = {
                    'date': tran_dict['date'],
                    'product_id': product_id_list[i],
                    'name': product_name,
                    'status': tran_dict['status'],
                    'amount': product_amount_list[i],
                    'area': product_area_list[i],
                    'user_id': tran_dict['report_user_id'],
                    'note': product_note
                }
                history_list.append(history_data)
        else:
            product_info_gen = db.collection('products_info').where('product_id', '==',tran_dict['product_id']).stream()
            for product_info in product_info_gen:
                product_name = (product_info.to_dict()['product_name'])
                item_total = (product_info.to_dict())['amount_total']
                product_note = (product_info.to_dict())['note']
            history_data = {
                'date': tran_dict['date'],
                'product_id': tran_dict['product_id'],
                'name': product_name,
                'status': tran_dict['status'],
                'amount': tran_dict['amount'],
                'total': item_total,
                'area': tran_dict['area'],
                'user_id': tran_dict['report_user_id'],
                'note': product_note
            }
            history_list.append(history_data)

    return render(request, "history.html", {'history_list': history_list,"position":positions})


def history2(request):
    global positions
    trans = db.collection('transference').where('status', '!=', 'wait_for_checking').stream()

    out_date = []
    out_amount = []
    out_id = []
    out_check = []

    in_date = []
    in_amount = []
    in_id = []
    in_check = []

    waste_date = []
    waste_amount = []
    waste_id = []
    waste_check = []

    lost_date = []
    lost_amount = []
    lost_id = []
    lost_check = []

    summary_list = []

    date_tmp = ''
    tmp = ''
    lst = []

    for tran in trans:
        tran_dict = tran.to_dict()

        if (tran_dict['status'] == 'in_warehouse'):

            month = tran_dict['date'].month
            year = tran_dict['date'].year

            if month == 1:
                month = 'January'
            elif month == 2:
                month = 'February'
            elif month == 3:
                month = 'March'
            elif month == 4:
                month = 'April'
            elif month == 5:
                month = 'May'
            elif month == 6:
                month = 'June'
            elif month == 7:
                month = 'July'
            elif month == 8:
                month = 'August'
            elif month == 9:
                month = 'Septenber'
            elif month == 10:
                month = 'October'
            elif month == 11:
                month = 'November'
            elif month == 12:
                month = 'December'

            date_tmp = str(month) + ' ' + str(year)
            in_date.append(date_tmp)
            in_amount.append(tran_dict['amount'])
            in_id.append(tran_dict['product_id'])
            in_check.append(False)
        elif (tran_dict['status'] == 'out_warehouse'):

            for product_id in tran_dict['products_id']:

                month = tran_dict['date'].month
                year = tran_dict['date'].year

                if month == 1:
                    month = 'January'
                elif month == 2:
                    month = 'February'
                elif month == 3:
                    month = 'March'
                elif month == 4:
                    month = 'April'
                elif month == 5:
                    month = 'May'
                elif month == 6:
                    month = 'June'
                elif month == 7:
                    month = 'July'
                elif month == 8:
                    month = 'August'
                elif month == 9:
                    month = 'Septenber'
                elif month == 10:
                    month = 'October'
                elif month == 11:
                    month = 'November'
                elif month == 12:
                    month = 'December'

                date_tmp = str(month) + ' ' + str(year)
                out_date.append(date_tmp)
                out_id.append(product_id)
                out_check.append(False)

            for amount in tran_dict['products_val']:
                out_amount.append(amount)

        elif (tran_dict['status'] == 'waste_warehouse'):

            month = tran_dict['date'].month
            year = tran_dict['date'].year

            if month == 1:
                month = 'January'
            elif month == 2:
                month = 'February'
            elif month == 3:
                month = 'March'
            elif month == 4:
                month = 'April'
            elif month == 5:
                month = 'May'
            elif month == 6:
                month = 'June'
            elif month == 7:
                month = 'July'
            elif month == 8:
                month = 'August'
            elif month == 9:
                month = 'Septenber'
            elif month == 10:
                month = 'October'
            elif month == 11:
                month = 'November'
            elif month == 12:
                month = 'December'

            date_tmp = str(month) + ' ' + str(year)
            waste_date.append(date_tmp)
            waste_amount.append(tran_dict['amount'])
            waste_id.append(tran_dict['product_id'])
            waste_check.append(False)
        elif (tran_dict['status'] == 'missing_warehouse'):

            month = tran_dict['date'].month
            year = tran_dict['date'].year

            if month == 1:
                month = 'January'
            elif month == 2:
                month = 'February'
            elif month == 3:
                month = 'March'
            elif month == 4:
                month = 'April'
            elif month == 5:
                month = 'May'
            elif month == 6:
                month = 'June'
            elif month == 7:
                month = 'July'
            elif month == 8:
                month = 'August'
            elif month == 9:
                month = 'Septenber'
            elif month == 10:
                month = 'October'
            elif month == 11:
                month = 'November'
            elif month == 12:
                month = 'December'

            date_tmp = str(month) + ' ' + str(year)
            lost_date.append(date_tmp)
            lost_amount.append(tran_dict['amount'])
            lost_id.append(tran_dict['product_id'])
            lost_check.append(False)

    # new_out_date= []
    # new_out_amount = []
    # new_out_id = []

    # new_in_date = []
    # new_in_amount =[]
    # new_in_id = []

    # new_waste_date = []
    # new_waste_amount = []
    # new_waste_id = []

    # new_lost_date = []
    # new_lost_amount = []
    # new_lost_id = []

    list_checking = []

    # ----------out---------------#
    for i in range(len(out_date)):
        for j in range(i + 1, len(out_date)):
            if (out_id[i] == out_id[j] and out_date[i] == out_date[j] and out_check[j] == False):
                out_amount[i] = out_amount[i] + out_amount[j]
                out_check[j] = True

    for i in range(len(out_date)):
        if (out_check[i] == False):
            # new_out_id.append(out_id[i])
            # new_out_date.append(out_date[i])
            # new_out_amount.append(out_amount[i])
            product_info_gen = db.collection('products_info').where('product_id', '==', out_id[i]).stream()
            for product_info in product_info_gen:
                product_name = (product_info.to_dict()['product_name'])
                item_total = (product_info.to_dict())['amount_total']
                product_note = (product_info.to_dict())['note']
            summary_data = {
                'date': out_date[i],
                'product_id': out_id[i],
                'name': product_name,
                'item_in': 0,
                'item_out': out_amount[i],
                'item_lost': 0,
                'item_waste': 0,
                'item_total': item_total,
                'note': product_note
            }
            summary_list.append(summary_data)
            list_checking.append(False)

    # -----------in--------------#
    for i in range(len(in_date)):
        for j in range(i + 1, len(in_date)):
            if (in_id[i] == in_id[j] and in_date[i] == in_date[j] and in_check[j] == False):
                in_amount[i] = in_amount[i] + in_amount[j]
                in_check[j] = True

    for i in range(len(in_date)):
        if (in_check[i] == False):
            # new_in_id.append(in_id[i])
            # new_in_date.append(in_date[i])
            # new_in_amount.append(in_amount)
            product_info_gen = db.collection('products_info').where('product_id', '==', in_id[i]).stream()
            for product_info in product_info_gen:
                product_name = (product_info.to_dict()['product_name'])
                item_total = (product_info.to_dict())['amount_total']
                product_note = (product_info.to_dict())['note']
            summary_data = {
                'date': in_date[i],
                'product_id': in_id[i],
                'name': product_name,
                'item_in': in_amount[i],
                'item_out': 0,
                'item_lost': 0,
                'item_waste': 0,
                'item_total': item_total,
                'note': product_note
            }
            summary_list.append(summary_data)
            list_checking.append(False)

    # -----------waste--------------#
    for i in range(len(waste_date)):
        for j in range(i + 1, len(waste_date)):
            if (waste_id[i] == waste_id[j] and waste_date[i] == waste_date[j] and waste_check[j] == False):
                waste_amount[i] = waste_amount[i] + waste_amount[j]
                waste_check[j] = True

    for i in range(len(waste_date)):
        if (waste_check[i] == False):
            # new_waste_id.append(waste_id[i])
            # new_waste_date.append(waste_date[i])
            # new_waste_amount.append(waste_amount)
            product_info_gen = db.collection('products_info').where('product_id', '==', waste_id[i]).stream()
            for product_info in product_info_gen:
                product_name = (product_info.to_dict()['product_name'])
                item_total = (product_info.to_dict())['amount_total']
                product_note = (product_info.to_dict())['note']
            summary_data = {
                'date': waste_date[i],
                'product_id': waste_id[i],
                'name': product_name,
                'item_in': 0,
                'item_out': 0,
                'item_lost': 0,
                'item_waste': waste_amount[i],
                'item_total': item_total,
                'note': product_note
            }
            summary_list.append(summary_data)
            list_checking.append(False)

    # -----------lost--------------#
    for i in range(len(lost_date)):
        for j in range(i + 1, len(lost_date)):
            if (lost_id[i] == lost_id[j] and lost_date[i] == lost_date[j] and lost_check[j] == False):
                lost_amount[i] = lost_amount[i] + lost_amount[j]
                lost_check[j] = True

    for i in range(len(lost_date)):
        if (lost_check[i] == False):
            # new_lost_id.append(lost_id[i])
            # new_lost_date.append(lost_date[i])
            # new_lost_amount.append(lost_amount)
            product_info_gen = db.collection('products_info').where('product_id', '==', lost_id[i]).stream()
            for product_info in product_info_gen:
                product_name = (product_info.to_dict()['product_name'])
                item_total = (product_info.to_dict())['amount_total']
                product_note = (product_info.to_dict())['note']
            summary_data = {
                'date': lost_date[i],
                'product_id': lost_id[i],
                'name': product_name,
                'item_in': 0,
                'item_out': 0,
                'item_lost': lost_amount[i],
                'item_waste': 0,
                'item_total': item_total,
                'note': product_note
            }
            summary_list.append(summary_data)
            list_checking.append(False)

    # ----------check-------------#
    new_summary_list = []
    for i in range(len(summary_list)):
        for j in range(i + 1, len(summary_list)):
            if (summary_list[i]['date'] == summary_list[j]['date'] and summary_list[i]['product_id'] == summary_list[j][
                'product_id'] and list_checking[j] == False):
                summary_list[i]['item_in'] = summary_list[i]['item_in'] + summary_list[j]['item_in']
                summary_list[i]['item_out'] = summary_list[i]['item_out'] + summary_list[j]['item_out']
                summary_list[i]['item_lost'] = summary_list[i]['item_lost'] + summary_list[j]['item_lost']
                summary_list[i]['item_waste'] = summary_list[i]['item_waste'] + summary_list[j]['item_waste']

                list_checking[j] = True

    for i in range(len(list_checking)):
        if (list_checking[i] == False):
            new_summary_list.append(summary_list[i])

    return render(request, "history2.html", {'summary_list': new_summary_list, 'position': positions})

def history3(request):
    global positions
    trans = db.collection('transference').where('status','==','out_warehouse').stream()
    delivery_list = []
    for tran in trans:
        tran_dict = tran.to_dict()

        delivery_data = {
            'date' : tran_dict['date'],
            'recipient' : tran_dict['recipient'],
            'phone_number' : tran_dict['telephone'],
            'user_id' : tran_dict['report_user_id'],
            'address' : tran_dict['address'],
            'report_id' : tran_dict['report_id']
        }
        if tran_dict['address']!="":
            delivery_list.append(delivery_data)

    return render(request,"history3.html", {'delivery_list' : delivery_list,'position':positions})


def register(request):
    return render(request,"register.html")


def management(request):
    global positions
    try:
        products_gen = db.collection('products_info').stream()
        products_list = []
        for product in products_gen:
            product_dict = product.to_dict()
            product_id = product_dict['product_id']
            product_name = product_dict['product_name']
            product_amount = product_dict['amount_total']
            price_unit = product_dict['price_unit']
            weight_unit = product_dict['weight_unit']
            length = product_dict['length']
            height = product_dict['height']
            depth = product_dict['depth']
            size = str(length)+'*'+str(height)+'*'+str(depth)
            category = product_dict['category']
            note = product_dict['note']
            product_data = {
                'product_id': product_id,
                'product_name': product_name,
                'amount_total': product_amount,
                'price_unit': price_unit,
                'weight_unit': weight_unit,
                'size': size,
                'category': category,
                'note': note
            }
            products_list.append(product_data)
        return render(request,"management.html",{'products_list': products_list,'position':positions})
    except:
        return redirect('/management_alert/')

def management_alert(request):
    global positions
    try:
        products_gen = db.collection('products_info').stream()
        products_list = []
        for product in products_gen:
            product_dict = product.to_dict()
            product_id = product_dict['product_id']
            product_name = product_dict['product_name']
            product_amount = product_dict['amount_total']
            price_unit = product_dict['price_unit']
            weight_unit = product_dict['weight_unit']
            length = product_dict['length']
            height = product_dict['height']
            depth = product_dict['depth']
            size = str(length)+'*'+str(height)+'*'+str(depth)
            category = product_dict['category']
            note = product_dict['note']
            product_data = {
                'product_id': product_id,
                'product_name': product_name,
                'amount_total': product_amount,
                'price_unit': price_unit,
                'weight_unit': weight_unit,
                'size': size,
                'category': category,
                'note': note
            }
            products_list.append(product_data)
        return render(request,"management_alert.html",{'products_list': products_list,'position':positions})
    except:
        return render(request,"management_alert.html",{
                                                'products_list': products_list,
                                                'position':positions})

def product_ref(request):
    global positions
    product_id = request.GET.get('product_id')
    areas_gen = db.collection('areas').where('product_id','==',product_id).stream()
    product_gen = db.collection('products_info').where('product_id','==',product_id).stream()
    product_name = ''
    price_unit = 0
    size = ''
    weight_unit = 0
    amount_total = 0
    category = ''
    note = ''
    for product in product_gen:
        product_dict = product.to_dict()
        product_name = product_dict['product_name']
        price_unit = product_dict['price_unit']
        length = product_dict['length']
        height = product_dict['height']
        depth = product_dict['depth']
        size = str(length)+'*'+str(height)+'*'+str(depth)
        weight_unit = product_dict['weight_unit']
        amount_total = product_dict['amount_total']
        category = product_dict['category']
        note = product_dict['note']
    print(product_name)
    in_warehouse_list = []
    for area in areas_gen:
        area_dict = area.to_dict()
        if area_dict['product_id'] == product_id:
            area_id = area_dict['area_id']
            amount = area_dict['amount_left']
            data = {
                'area_id': area_id,
                'amount': amount
            }
            in_warehouse_list.append(data)

    print(product_name)
    return render(request,"product_ref.html",{
                                                'in_warehouse_list': in_warehouse_list,
                                                'product_id': product_id,
                                                'product_name': product_name,
                                                'size': size,
                                                'weight_unit': weight_unit,
                                                'amount_total': amount_total,
                                                'category': category,
                                                'price_unit': price_unit,
                                                'note': note,
                                                'position': positions
                                                })

def comingmanage(request):
    global positions
    try:
        # if db.collection('transference').exists:
        trans_gen = db.collection('transference').where('status','==','wait_for_checking').stream()
        wc_list = []
        for tran in trans_gen:
            tran_dict = tran.to_dict()
            product_id = tran_dict['product_id']
            product_value = tran_dict['amount']
            show = tran_dict['show']
            product_name = ''
            price_unit = 0
            weight_unit = 0
            note = ''
            size=''
            if show:
                product_info_gen = db.collection('products_info').where('product_id','==',product_id).stream()
                for product_info in product_info_gen:
                    product_name = (product_info.to_dict())['product_name']
                    price_unit = (product_info.to_dict())['price_unit']
                    weight_unit = (product_info.to_dict())['weight_unit']
                    size = str((product_info.to_dict())['length'])+"*"+str((product_info.to_dict())['height'])+"*"+str((product_info.to_dict())['depth'])
                    note = (product_info.to_dict())['note']
                    tran_data = {
                                'report_id': tran_dict['report_id'],
                                'product_id': product_id,
                                'product_value': product_value,
                                'date': tran_dict['date'],
                                'product_name': product_name,
                                'product_value': product_value,
                                'price_unit': price_unit,
                                'weight_unit': weight_unit,
                                'size': size,
                                'report_user_id': tran_dict['report_user_id'],
                                'import_user_id': tran_dict['import_user_id'],
                                'note': note
                                }
                    wc_list.append(tran_data)

        return render(request,"comingmanage.html", {'wc_list': wc_list,'position': positions})
    except:
        return redirect('/comingmanage_alert/')

def comingmanage_alert(request):
    global positions
    try:
        # if db.collection('transference').exists:
        trans_gen = db.collection('transference').where('status', '==', 'wait_for_checking').stream()
        wc_list = []
        for tran in trans_gen:
            tran_dict = tran.to_dict()
            product_id = tran_dict['product_id']
            product_value = tran_dict['amount']
            show = tran_dict['show']
            product_name = ''
            price_unit = 0
            weight_unit = 0
            note = ''
            size = ''
            if show:
                product_info_gen = db.collection('products_info').where('product_id', '==', product_id).stream()
                for product_info in product_info_gen:
                    product_name = (product_info.to_dict())['product_name']
                    price_unit = (product_info.to_dict())['price_unit']
                    weight_unit = (product_info.to_dict())['weight_unit']
                    size = str((product_info.to_dict())['length']) + "*" + str(
                        (product_info.to_dict())['height']) + "*" + str((product_info.to_dict())['depth'])
                    note = (product_info.to_dict())['note']
                    tran_data = {
                        'report_id': tran_dict['report_id'],
                        'product_id': product_id,
                        'product_value': product_value,
                        'date': tran_dict['date'],
                        'product_name': product_name,
                        'product_value': product_value,
                        'price_unit': price_unit,
                        'weight_unit': weight_unit,
                        'size': size,
                        'report_user_id': tran_dict['report_user_id'],
                        'import_user_id': tran_dict['import_user_id'],
                        'note': note
                    }
                    wc_list.append(tran_data)

        return render(request, "comingmanage_alert.html", {'wc_list': wc_list, 'position': positions})
    except:
        return redirect('/comingmanage_alert/')


def add_product_for_checking(request):
    global positions
    try:
        product_id = request.POST.get('product_id')
        product_name = request.POST.get('product_name')
        price_unit = request.POST.get('price_unit')
        amount = request.POST.get('amount')
        category = request.POST.get('category')
        weight = request.POST.get('weight')
        length = request.POST.get('length')
        height = request.POST.get('height')
        depth = request.POST.get('depth')
        date = request.POST.get('date')
        time = request.POST.get('time')
        user_id = request.POST.get('user_id')
        note = request.POST.get('note')
        date_time = date + " " + time + " +07:00"  # time UTC+7
        date_time = datetime.fromisoformat(date_time)
        trans_ref = db.collection('transference')
        trans_gen = trans_ref.list_documents()

        if note == '' or note == None or note == ' ':
            note = '-'
        products_gen = db.collection('products_info').stream()
        for product in products_gen:
            product_dict = product.to_dict()
            if product_dict['product_id'] == product_id:
                print("product_id already exist")
                return redirect("/comingmanage_alert/")

        product_name = product_name.replace(" ", "_")
    except:
        print("Input error")
        return redirect("/comingmanage_alert/")

    try:
        user_check = db.collection('users').where('id', '==', user_id).stream()
        for check in user_check:
            ch = check.id
        sas = ch
    except:
        print("name error")
        return redirect("/comingmanage_alert/")

    try:
        count_trans = 1
        for tran in trans_gen:
            count_trans += 1
        report_id = 'wc' + str(count_trans).zfill(6)

        global userid
        current_user_ref = db.collection('users').document(userid).get()
        current_user_id = (current_user_ref.to_dict())['id']

        product_info = {
            "amount_total": 0,
            "product_id": product_id,
            "product_name": product_name,
            "price_unit": int(price_unit),
            "weight_unit": int(weight),
            "category": category,
            "length": int(length),
            "height": int(height),
            "depth": int(depth),
            "note": note
        }

        trans = {
            "product_id": product_id,
            "amount": amount,
            "date": date_time,
            "status": "wait_for_checking",
            "report_id": report_id,
            "import_user_id": user_id,
            "report_user_id": current_user_id,
            "show": True
        }
    except:
        print("ADD Dic error")
        return redirect("/comingmanage_alert/")

    try:
        print()
        db.collection('products_info').add(product_info)
        db.collection('transference').add(trans)
    except:
        print("Add error")
        return render(request, 'comingmanage_alert.html')
    return redirect('/comingmanage/')


def add_product_for_checking_old(request):
    global positions
    # try:
    product_id = request.POST.get('product_id')
    amount = request.POST.get('amount')
    date = request.POST.get('date')
    time = request.POST.get('time')
    user_id = request.POST.get('user_id')
    date_time = date + " " + time + " +07:00"  # time UTC+7
    date_time = datetime.fromisoformat(date_time)
    trans_ref = db.collection('transference')
    trans_gen = trans_ref.list_documents()
    is_work = False

    products_gen = db.collection('products_info').stream()
    for product in products_gen:
        product_dict = product.to_dict()
        if product_dict['product_id'] == product_id:
            is_work = True

    if is_work:
        user_check = db.collection('users').where('id', '==', user_id).stream()
        for check in user_check:
            ch = check.id
        sas = ch

        count_trans = 1
        for tran in trans_gen:
            count_trans += 1
        report_id = 'wc' + str(count_trans).zfill(6)

        global userid
        current_user_ref = db.collection('users').document(userid).get()
        current_user_id = (current_user_ref.to_dict())['id']

        trans = {
            "product_id": product_id,
            "amount": amount,
            "date": date_time,
            "status": "wait_for_checking",
            "report_id": report_id,
            "import_user_id": user_id,
            "report_user_id": current_user_id,
            "show": True
        }
        db.collection('transference').add(trans)
    elif not is_work:
        print("Not exist product_id, From add_product_for_checking_old")
        return redirect("/comingmanage_alert/")

    return redirect('/comingmanage/')


def choiceaddinven(request):
    global positions
    try:
        report_id = request.POST.get('report_id')
    except:
        print("Input error")
        return redirect('/comingmanage_alert/')
    try:
        report_doc = db.collection('transference').where('report_id', '==', report_id).stream()

        product_id = ''
        product_val = 0
        for i in report_doc:
            dic = i.to_dict()
            product_id = dic['product_id']
            product_val = dic['amount']

        if int(product_val)==0:
            return redirect('/comingmanage_alert/')

    except:
        print("Read error")
        return redirect('/comingmanage_alert/')

    try:
        product_doc = db.collection('products_info').where('product_id', '==', product_id).stream()
        for i in product_doc:
            dic_id = i.to_dict()
            depth = dic_id['depth']
            height = dic_id['height']
            length = dic_id['length']
            weight_unit = dic_id['weight_unit']
            size=str(length)+'*'+str(height)+'*'+str(depth)
        areas_product_gen = db.collection('areas').where('product_id', '==', product_id).stream()
        areas_empty_gen = db.collection('areas').where('product_id', '==', '-').stream()
    except:
        print('DATA ERROR')
        return redirect("/comingmanage_alert/")

    areas_list = []
    amount_total = int((4000 * 800) / (height * length))
    weight_unit_check = 3000/int(weight_unit)
    if amount_total > weight_unit_check:
        amount_total=weight_unit_check
    if amount_total <= weight_unit_check:
        amount_total = amount_total

    for area in areas_product_gen:
        dic = area.to_dict()
        if dic['amount_left'] < dic["amount_total"]:
            areas_list.append(area.to_dict())

    for area in areas_empty_gen:
        dic = area.to_dict()
        areas_list.append(area.to_dict())

    return render(request, "choiceaddinven.html" ,
                  {'areas_list': areas_list,
                   'product_id':product_id,
                   'amount':int(product_val),
                   'size':size,
                   'weight_unit':weight_unit,
                   'report_id':report_id,
                   'amount_total':int(amount_total),
                   'position': positions})

def damage_product(request):
    global positions
    report_id_damage = request.POST.get('report_id_damage')
    amount_waste = int(request.POST.get('amount_waste'))
    tran_gen = db.collection('transference').where('report_id', '==', report_id_damage).stream()

    for tran in tran_gen:
        key_tran = tran.id
    try:
        area_total_ref = db.collection('transference').document(key_tran).get()
        area_dic = area_total_ref.to_dict()
        amount_ref = area_dic['amount']
    except:
        return redirect('/comingmanage_alert/')

    amount_waste = amount_ref-amount_waste
    # print(amount_waste)
    db.collection('transference').document(key_tran).update({'amount': amount_waste})
    return redirect("/comingmanage/")


# def cal_add_invent(request):
#     global positions
#     try:
#         product_id = request.POST.get('product_id')
#         report_id = request.POST.get('report_id')
#         size = request.POST.get('size')
#         weight = int(request.POST.get('weight'))
#         amount_ref = int(request.POST.get('amount'))
#         area_id = request.POST.get('area_id')
#         amount_input = int(request.POST.get('amount_input'))
#         lst_size = [int(x) for x in size.split('*')]
#         length = lst_size[0]
#         height = lst_size[1]
#         depth = lst_size[2]
#         inspector_id = request.POST.get('inspector_id')
#         date_check = request.POST.get('date_check')
#         time_check = request.POST.get('time_check')
#         date_time = date_check + " " + time_check + " +07:00"  # time UTC+7
#         date_time = datetime.fromisoformat(date_time)
#
#         del lst_size
#
#         areas_num_gen = db.collection('areas').where('area_id', '==', area_id).stream()
#         tran_gen = db.collection('transference').where('report_id', '==', report_id).stream()
#         for a in areas_num_gen:
#             key_area = a.id
#             dic = a.to_dict()
#             product_id_check = dic['product_id']
#         for tran in tran_gen:
#             key_tran = tran.id
#
#             area_total_ref = db.collection('areas').document(key_area).get()
#             area_dic = area_total_ref.to_dict()
#     except:
#         print("Input Error")
#         return redirect("/comingmanage_alert/")
#
#     try:
#         user_check = db.collection('users').where('id', '==', inspector_id).stream()
#         for check in user_check:
#             ch = check.id
#         sas = ch
#     except:
#         print("Nmae Error")
#         return redirect("/comingmanage_alert/")
#
#     try:
#         weight_left = area_dic['weight_left'] + (weight * amount_input)
#         amount_left = area_dic['amount_left'] + amount_input
#
#         amount_tran = amount_ref - amount_input
#         if amount_tran < 0:
#             return redirect("/comingmanage_alert/")
#
#         if amount_tran == 0 or weight_left == 3000:
#             db.collection('transference').document(key_tran).update({'show': False})
#
#         trans_gen = db.collection('transference').list_documents()
#         count = 0
#         for tran in trans_gen:
#             count += 1
#         new_report_id = 'in' + (str(count).zfill(6))
#
#         global userid
#         report_user_id = ((db.collection('users').document(userid).get()).to_dict())['id']
#         tran_in_data = {
#             'report_id': new_report_id,
#             'amount': amount_input,
#             'area': area_id,
#             'report_user_id': report_user_id,
#             'show': True,
#             'product_id': product_id,
#             'status': 'in_warehouse',
#             'date': date_time,
#             'inspector_user_id': inspector_id
#         }
#
#         info_gen = db.collection('products_info').where('product_id', '==', product_id).stream()
#         key_info = ''
#         for info in info_gen:
#             key_info = info.id
#         area_total_ref = db.collection('products_info').document(key_info).get()
#         area_dic = area_total_ref.to_dict()
#         amount_total = area_dic['amount_total'] + amount_input
#         print(amount_total)
#         amount_total_info = amount_total
#     except:
#         print("cal Error")
#         return redirect("/comingmanage_alert/")
#
#     if product_id == product_id_check:
#         db.collection('areas').document(key_area).update({
#             'amount_left': amount_left,
#             'weight_left': weight_left
#         })
#     elif product_id_check == '-':
#         amount_total = int((4000 * 800) / (height * length))
#         weight_unit_check = 3000 / int(weight)
#
#         if amount_total > weight_unit_check:
#             amount_total = weight_unit_check
#         if amount_total <= weight_unit_check:
#             amount_total = amount_total
#         print(amount_total)
#         print(weight_unit_check)
#         db.collection('areas').document(key_area).update({
#             'product_id': product_id,
#             'amount_total': amount_total,
#             'amount_left': amount_left,
#             'weight_left': weight_left,
#             'depth_product': depth,
#             'height_product': height,
#             'length_product': length
#         })
#     db.collection('transference').document(key_tran).update({'amount': amount_tran})
#     db.collection('transference').add(tran_in_data)
#     db.collection('products_info').document(key_info).update({'amount_total': amount_total_info})
#
#     return redirect("/comingmanage/")

def cal_add_invent(request):
    global positions
    try:
        product_id = request.POST.get('product_id')
        report_id = request.POST.get('report_id')
        size = request.POST.get('size')
        weight = int(request.POST.get('weight'))
        amount_ref = int(request.POST.get('amount'))
        area_id = request.POST.get('area_id')
        amount_input = int(request.POST.get('amount_input'))
        lst_size = [int(x) for x in size.split('*')]
        length = lst_size[0]
        height = lst_size[1]
        depth = lst_size[2]
        inspector_id = request.POST.get('inspector_id')
        date_check = request.POST.get('date_check')
        time_check = request.POST.get('time_check')
        date_time = date_check + " " + time_check + " +07:00"  # time UTC+7
        date_time = datetime.fromisoformat(date_time)

        del lst_size

        areas_num_gen = db.collection('areas').where('area_id', '==', area_id).stream()

        tran_gen = db.collection('transference').where('report_id', '==', report_id).stream()
        for a in areas_num_gen:
            key_area = a.id
            dic = a.to_dict()
            product_id_check = dic['product_id']
            amount_l = dic['amount_left']
            amount_t = dic['amount_total']
            if product_id_check != product_id and product_id != '-':
                return redirect('/comingmanage_alert/')
            elif product_id_check == product_id:
                if amount_l == amount_t or dic['weight_left'] == 3000:
                    return redirect('/comingmanage_alert/')
        for tran in tran_gen:
            key_tran = tran.id

            area_total_ref = db.collection('areas').document(key_area).get()
            area_dic = area_total_ref.to_dict()
    except:
        print("Input Error")
        return redirect("/comingmanage_alert/")

    try:
        user_check = db.collection('users').where('id', '==', inspector_id).stream()
        for check in user_check:
            ch = check.id
        sas = ch
    except:
        print("Nmae Error")
        return redirect("/comingmanage_alert/")

    try:
        weight_left = area_dic['weight_left'] + (weight * amount_input)
        amount_left = area_dic['amount_left'] + amount_input

        amount_tran = amount_ref - amount_input
        if amount_tran < 0:
            return redirect("/comingmanage_alert/")

        if amount_tran == 0 or weight_left == 3000:
            db.collection('transference').document(key_tran).update({'show': False})

        trans_gen = db.collection('transference').list_documents()
        count = 0
        for tran in trans_gen:
            count += 1
        new_report_id = 'in' + (str(count).zfill(6))

        global userid
        report_user_id = ((db.collection('users').document(userid).get()).to_dict())['id']
        tran_in_data = {
            'report_id': new_report_id,
            'amount': amount_input,
            'area': area_id,
            'report_user_id': report_user_id,
            'show': True,
            'product_id': product_id,
            'status': 'in_warehouse',
            'date': date_time,
            'inspector_user_id': inspector_id
        }

        info_gen = db.collection('products_info').where('product_id', '==', product_id).stream()
        key_info = ''
        for info in info_gen:
            key_info = info.id
        area_total_ref = db.collection('products_info').document(key_info).get()
        area_dic = area_total_ref.to_dict()
        amount_total = area_dic['amount_total'] + amount_input
        print(amount_total)
        amount_total_info = amount_total
    except:
        print("cal Error")
        return redirect("/comingmanage_alert/")

    if product_id == product_id_check:
        db.collection('areas').document(key_area).update({
            'amount_left': amount_left,
            'weight_left': weight_left
        })
    elif product_id_check == '-':
        amount_total = int((4000 * 800) / (height * length))
        weight_unit_check = 3000 / int(weight)

        if amount_total > weight_unit_check:
            amount_total = weight_unit_check
        if amount_total <= weight_unit_check:
            amount_total = amount_total
        print(amount_total)
        print(weight_unit_check)
        db.collection('areas').document(key_area).update({
            'product_id': product_id,
            'amount_total': amount_total,
            'amount_left': amount_left,
            'weight_left': weight_left,
            'depth_product': depth,
            'height_product': height,
            'length_product': length
        })
    db.collection('transference').document(key_tran).update({'amount': amount_tran})
    db.collection('transference').add(tran_in_data)
    db.collection('products_info').document(key_info).update({'amount_total': amount_total_info})

    return redirect("/comingmanage/")

def damage(request):
    global positions
    try:
        product_id_damage = request.POST.get('product_id_damage')
    except:
        return redirect('/management_alert/')

    product_doc = db.collection('products_info').where('product_id', '==', product_id_damage).stream()
    for i in product_doc:
        dic_id = i.to_dict()
    try:
        weight_unit = dic_id['weight_unit']
        areas_product_gen = db.collection('areas').where('product_id', '==', product_id_damage).stream()
        areas_list = []
    except:
        print('DATA ERROR')
        return redirect("/management_alert/")

    for area in areas_product_gen:
        dic = area.to_dict()
        areas_list.append(area.to_dict())

    return render(request, "damage.html" ,
                  {'areas_list': areas_list,
                   'product_id_damage':product_id_damage,
                   'position': positions})

def cal_manage_damage(request):
    global positions
    try:
        product_id = request.POST.get('product_id')
        inspector_id = request.POST.get('inspector_id')
        date_check = request.POST.get('date_check')
        time_check = request.POST.get('time_check')
        date_time = date_check + " " + time_check + " +07:00"  # time UTC+7
        date_time = datetime.fromisoformat(date_time)
        area_id = request.POST.get('area_id')
        status1 = request.POST.get('status')
        amount_input = int(request.POST.get('amount_input'))

        areas_num_gen = db.collection('areas').where('area_id','==',area_id).stream()
        product_info_num_gen = db.collection('products_info').where('product_id', '==', product_id).stream()
        for a in areas_num_gen:
            key_area = a.id
            dic = a.to_dict()
            product_id_check = dic['product_id']
        cc=product_id_check

        if cc != product_id:
            return redirect("/management_alert/")

        for tran in product_info_num_gen:
            key_product= tran.id

            area_total_ref = db.collection('areas').document(key_area).get()
            area_dic = area_total_ref.to_dict()
    except:
        return redirect("/management_alert/")

    try:
        user_check = db.collection('users').where('id', '==', inspector_id).stream()
        for check in user_check:
            ch = check.id
        sas=ch

        weight_left = area_dic['weight_left']
        amount_left = area_dic['amount_left']

        trans_gen = db.collection('transference').list_documents()
        count = 0
        for tran in trans_gen:
            count += 1
        new_report_id = 'in'+ (str(count).zfill(6))

        global userid
        report_user_id = ((db.collection('users').document(userid).get()).to_dict())['id']
        status_add=''
        if status1=='waste':
            status_add='waste_warehouse'
        if status1=='missing':
            status_add = 'missing_warehouse'
        tran_in_data = {
            'report_id': new_report_id,
            'amount': amount_input,
            'area': area_id,
            'report_user_id': report_user_id,
            'show': True,
            'product_id': product_id,
            'status': status_add,
            'date':date_time,
            'inspector_user_id':inspector_id
        }
        info_gen = db.collection('products_info').where('product_id', '==', product_id).stream()
        key_info=''
        for info in info_gen:
            key_info = info.id
        area_total_ref = db.collection('products_info').document(key_info).get()
        area_dic = area_total_ref.to_dict()
        amount_total = area_dic['amount_total'] - amount_input
    except:
        return redirect("/management_alert/")

    weight_left = weight_left - (int(area_dic['weight_unit'])*int(amount_input))
    amount_left = int(amount_left)-int(amount_input)
    print(status1)
    print(weight_left)
    print(amount_total)
    print(amount_left)
    print(tran_in_data)
    if amount_left<0:
        return redirect("/management_alert/")
    db.collection('products_info').document(key_info).update({'amount_total': amount_total})
    db.collection('areas').document(key_area).update({'amount_left': amount_left,'weight_left': weight_left})
    db.collection('transference').add(tran_in_data)
    return redirect("/management/")

def damageinven(request):
    return render(request, "damageinven.html")

def movechoice(request):
    return render(request, "movechoice.html")

class InventInView(TemplateView):
    template_name = 'InView.html'

def post_signin(request):
    email = request.POST.get('email')
    password = request.POST.get('pass')
    global userid

    try:
        user = authe.sign_in_with_email_and_password(email, password)

    except:
        message = "invalid cerediantials"
        return render(request, "login.html",{"msg":message})
    uid = user['localId']
    userid = uid
    user_ref = db.collection('users').document(uid)
    user_dict = user_ref.get().to_dict()
    # firstname = user_dict['firstname']
    # lastname = user_dict['lastname']
    # phone = user_dict['phone']
    # position = user_dict['position']

    try:
        if user_dict['last_login'].exists:
            user_ref.update({'last_login': firestore.SERVER_TIMESTAMP})

    except:
        user_ref.set({'last_login': firestore.SERVER_TIMESTAMP}, merge=True)

    return redirect('/myprofile/')


def signup(request):
    firstname = request.POST.get('firstname').lower()
    lastname = request.POST.get('lastname').lower()
    phone = request.POST.get('phone')
    email = request.POST.get('email')
    password = request.POST.get('password')
    position = request.POST.get('position')

    users_ref = db.collection('users')
    users_gen = users_ref.list_documents()
    users_list = []
    for user in users_gen:
        users_list.append(user.get().to_dict())
    users_count_str = str(len(users_list)+1)
    del users_list
    users_count_str = users_count_str.zfill(3)
    user_id = ''
    if position == "manager":
        user_id = "M" + users_count_str
    else:
        user_id = "E" + users_count_str

    try:
        user = authe.create_user_with_email_and_password(email, password)
        uid = user['localId']
        data = {
            "firstname": firstname,
            "lastname": lastname,
            "phone": phone,
            "email": email,
            "position": position,
            "id": user_id,
            "last_login": "never",
            "status": "employed"}
        db.collection("users").document(uid).set(data)
    except:
        message = "Unable to create account try again"
        return render(request, "register.html", {"msg": message})
    return redirect('/HR/')


def Test(request):
    # a = ['A', 'B', 'C', 'D', 'E']
    # s1 = ""
    # s2 = ""
    # s3 = ""
    # s4 = ""
    # show = []
    # for i in range(2):
    #     s1 = s1 + str(i + 1)
    #     for j in range(2):
    #         s2 = s1 + str(j + 1)
    #         for item in a:
    #             s3 = s2 + item
    #             for k in range(3):
    #                 s4 = s3 + str(k + 1)
    #                 show.append(s4)
    #             s4 = ""
    #         s3 = ""
    #     s2 = ""
    #     s1 = ""
    #
    #
    # for area_id in show:
    #     data = {
    #         "area_id": area_id,
    #         "product_id": "-",
    #         "weight_left": 0,
    #         "depth_product": 0,
    #         "height_product": 0,
    #         "length_product": 0,
    #         "amount_left": 0,
    #         "amount_total": 0
    #     }
    #     db.collection('areas').add(data)
    #
    # for i in show:
    #     print(i)
    # print(len(show))
    # -------------------------------------------------------------------------add area
    # data = {
    #     "category":"table",
    #     "note": "",
    #     "product_id": "000004",
    #     "price_unit": 5000,
    #     "product_name":"table(black)",
    #     "weight_unit":5,
    #     "zone":"kitchen"
    #     }
    # db.collection('products_info').add(data)

    # data = {
    #     "category": "shelf",
    #     "note": "",
    #     "product_id": "000003",
    #     "price_unit": 1200,
    #     "product_name": "table(black)",
    #     "weight_unit": 30,
    #     "zone": "livingroom"
    # }
    # db.collection('products_info').add(data)
    # -------------------------------------------------------------------------add product_info
    # data = {
    #     "category": "shelf",
    #     "note": "",
    #     "product_id": "000003",
    #     "price_unit": 1200,
    #     "product_name": "table(black)",
    #     "weight_unit": 30,
    #     "zone": "livingroom"
    # }
    # db.collection('products_info').add(data)
    # -------------------------------------------------------------------------add product_info
    return render(request, "Testngongo.html")


def render_pdf_view(request):
    global positions
    this_report_id = request.POST.get('system', None)
    transgen = db.collection('transference').where('status', '==', 'out_warehouse').stream()
    report_list = []
    for tran in transgen:
        dict_get = tran.to_dict()
        report_id = dict_get['report_id']
        if this_report_id == report_id:
            address = dict_get['address']
            recipient = dict_get['recipient']
            phone = dict_get['telephone']
            date = dict_get['date']
            products_id = dict_get['products_id']
            products_val = dict_get['products_val']
            if len(products_id) > 1:
                for i in range(1, len(products_id)):
                    tmp1 = products_id[i]
                    if tmp1 == products_id[i - 1]:
                        products_val[i] += products_val[i - 1]
                        products_id.pop(i - 1)
                        products_val.pop(i - 1)
                    if len(products_id) == 1:
                        break

            products_name = []
            for pro_id in products_id:
                p_id = pro_id
                product_info_gen = db.collection('products_info').where('product_id', '==', pro_id).stream()
                for product_info in product_info_gen:
                    product_name = (product_info.to_dict())['product_name']
                    products_name.append(product_name)
            tran_data = {
                'report_id': report_id,
                'date': date,
                'address': address,
                'phone': phone,
                'recipient': recipient,
                'products_id': products_id,
                'products_val': products_val,
                'products_name': products_name
            }
            report_list.append(tran_data)

    template_path = 'pdf.html'
    context = {'report_list': report_list,
               'this': this_report_id,
               }
    response = HttpResponse(content_type='application/pdf')
    filename = str(report_id)
    response['Content-Disposition'] = ' filename=' + filename + ".pdf"
    template = get_template(template_path)
    html = template.render(context)
    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response


def Delete_Order(request):
    Delete_Order = int(request.POST.get('Delete_Order'))
    report_id = request.POST.get('report_id')
    global userid
    current_user_ref = db.collection('users').document(userid).get()
    user_id = (current_user_ref.to_dict())['id']
    trans_ref = db.collection('transference')
    query_status = trans_ref.where('status', '==', "out_warehouse").stream()

    query_del = trans_ref.where('report_id', '==', report_id).stream()

    print(report_id)

    area = []
    product_id = []
    product_val = []
    id = ""
    for q in query_del:
        id = q.id
        tran_dict = q.to_dict()
        area = tran_dict['area']
        product_id = tran_dict['products_id']
        product_val = tran_dict['products_val']
        print(id)
        print(area)
    if (Delete_Order <= len(area)):
        if (Delete_Order > 0):
            area.pop(Delete_Order - 1)
            product_id.pop(Delete_Order - 1)
            product_val.pop(Delete_Order - 1)
            print(area)
            db.collection('transference').document(id).update(
                {"area": area, "products_id": product_id, "products_val": product_val})
            return redirect('/soleoutmanage_delete/')

    return redirect('/soleoutmanage_alert/')


def soleoutmanage_Delete(request):
    global positions
    location_id = request.POST.get('location_id')
    amount_out = request.POST.get('amount_out')

    global userid

    current_user_ref = db.collection('users').document(userid).get()
    user_id = (current_user_ref.to_dict())['id']

    trans_ref = db.collection('transference')
    query_status = trans_ref.where('status', '==', "out_warehouse").stream()

    product_id = []
    product_val = []
    area_id = []
    name_pro = []
    report_id = ""

    try:
        amount = int(amount_out)
    except:

        for q in query_status:
            id = q.id
            tran_dict = q.to_dict()
            address_non = tran_dict['address']
            report_user = tran_dict['report_user_id']
            report_id = tran_dict['report_id']
            if (address_non == ""):
                if (user_id == report_user):
                    print(id)
        area_ref = db.collection('areas')
        product_ref = db.collection('products_info')
        query_area = area_ref.where('area_id', '==', location_id).stream()

        area_pro_id = ''

        for q in query_area:
            tran_dict = q.to_dict()

            area_pro_id = tran_dict['product_id']

        query_prod_info = product_ref.where('product_id', '==', area_pro_id).stream()
        for q in query_prod_info:
            tran_dict = q.to_dict()

        query_fine_id = trans_ref.where('status', '==', "out_warehouse").stream()

        id = ""

        for q in query_fine_id:
            tran_dict = q.to_dict()
            report_user = tran_dict['report_user_id']
            if (tran_dict['address'] == ""):
                if (user_id == report_user):
                    report_id = tran_dict['report_id']
                print(report_id)

        query_statement = trans_ref.where('report_id', '==', report_id).stream()
        for q in query_statement:
            tran_dict = q.to_dict()
            id = q.id
            product_id = tran_dict['products_id']
            product_val = tran_dict['products_val']
            area_id = tran_dict['area']

        x = 0
        while (x < len(product_id)):
            query_name = product_ref.where('product_id', '==', product_id[x]).stream()
            for q in query_name:
                tran_dict = q.to_dict()
                name_pro.append(tran_dict['product_name'])
            x += 1

        print(product_id)
        print(product_val)
        print(area_id)

        run_add_dict = 0
        wc_list = []

        while (run_add_dict < len(product_id)):
            transx = {
                "Order": run_add_dict + 1,
                "product_id": product_id[run_add_dict],
                "product_name": name_pro[run_add_dict],
                "area": area_id[run_add_dict],
                "amount": product_val[run_add_dict]
            }
            run_add_dict += 1
            wc_list.append(transx)

        return render(request, "soleoutmanage_delete.html",
                      {'wc_list': wc_list, 'report_id': report_id, 'position': positions})


def SoleOut(request):
    global positions
    product_id = request.POST.get('product_id')

    area_ref = db.collection('areas')
    product_ref = db.collection('products_info')

    query_prod_info = product_ref.where('product_id', '==', product_id).stream()
    query_area = area_ref.where('product_id', '==', product_id).stream()

    info_id = ''
    info_name = ''
    info_depth = 0
    info_heigth = 0
    info_length = 0
    info_price_unit = 0

    area_id = ""
    area_amount = 0
    wc_list = []

    for q in query_prod_info:
        tran_dict = q.to_dict()
        info_id = tran_dict['product_id']
        info_name = tran_dict['product_name']
        info_depth = tran_dict['depth']
        info_length = tran_dict['length']
        info_heigth = tran_dict['height']
        info_price_unit = tran_dict['price_unit']

    for q in query_area:
        tran_dict = q.to_dict()
        area_id = tran_dict['area_id']
        area_amount = tran_dict['amount_left']
        tran_data = {"area_id": area_id,
                     "amount_left": area_amount}
        wc_list.append(tran_data)

    if (info_id == ""):
        return redirect('/soleoutmanage_alert/')

    return render(request, "soleout.html", {"info_id": info_id,
                                            "info_name": info_name,
                                            "info_depth": info_depth,
                                            "info_heigth": info_heigth,
                                            "info_length": info_length,
                                            "info_price_unit": info_price_unit,
                                            'wc_list': wc_list,
                                            'position': positions})


def soleoutmanage(request):
    global positions
    location_id = request.POST.get('location_id')
    amount_out = request.POST.get('amount_out')

    global userid
    user_id = userid

    current_user_ref = db.collection('users').document(userid).get()
    user_id = (current_user_ref.to_dict())['id']

    trans_ref = db.collection('transference')
    query_status = trans_ref.where('status', '==', "out_warehouse").stream()
    trans_gen = trans_ref.list_documents()

    product_id = []
    product_val = []
    area_id = []
    wc_list = []

    report_id = ""

    try:
        amount = int(amount_out)
    except:

        for q in query_status:
            id = q.id
            tran_dict = q.to_dict()
            address_non = tran_dict['address']
            report_user = tran_dict['report_user_id']
            if (address_non == ""):
                if (user_id == report_user):
                    db.collection('transference').document(id).delete()
                # print(id)

        date_time = "2021-01-01" + " " + "00:00" + " +07:00"  # time UTC+7
        date_time = datetime.fromisoformat(date_time)
        count_trans = 1
        for tran in trans_gen:
            count_trans += 1
        report_id = 'out' + str(count_trans).zfill(6)
        trans = {
            "report_id": report_id,
            "report_user_id": user_id,
            "address": "",
            "area": area_id,
            "products_id": product_id,
            "products_val": product_val,
            "picture": "",
            "recipient": "",
            "status": "out_warehouse",
            "telephone": "",
            "date": date_time
        }
        db.collection('transference').add(trans)
        return render(request, "soleoutmanage.html", {'report_id': report_id, 'position': positions})

    area_ref = db.collection('areas')
    product_ref = db.collection('products_info')

    query_area = area_ref.where('area_id', '==', location_id).stream()

    info_name = ''
    info_depth = 0
    info_heigth = 0
    info_length = 0
    info_price_unit = 0
    area_ids = ''
    area_pro_id = ''

    name_pro = []
    amount_left = 0
    for q in query_area:
        tran_dict = q.to_dict()
        area_ids = tran_dict['area_id']
        area_pro_id = tran_dict['product_id']

        amount_left = int(tran_dict['amount_left'])

    query_prod_info = product_ref.where('product_id', '==', area_pro_id).stream()
    for q in query_prod_info:
        tran_dict = q.to_dict()
        info_name = tran_dict['product_name']
        info_depth = tran_dict['depth']
        info_length = tran_dict['length']
        info_heigth = tran_dict['height']
        info_price_unit = tran_dict['price_unit']
        print(info_name)

    if (amount > amount_left):
        x = []
        query_area = area_ref.where('product_id', '==', area_pro_id).stream()
        for q in query_area:
            tran_dict = q.to_dict()
            area_id = tran_dict['area_id']
            area_amount = tran_dict['amount_left']
            tran_data = {"area_id": area_id,
                         "amount_left": area_amount}
            x.append(tran_data)

        return render(request, "soleout.html", {"info_id": area_pro_id,
                                                "info_name": info_name,
                                                "info_depth": info_depth,
                                                "info_heigth": info_heigth,
                                                "info_length": info_length,
                                                "info_price_unit": info_price_unit,
                                                'wc_list': x,
                                                'position': positions})

    query_fine_id = trans_ref.where('status', '==', "out_warehouse").stream()

    id = ""

    for q in query_fine_id:
        tran_dict = q.to_dict()
        report_user = tran_dict['report_user_id']
        if (tran_dict['address'] == ""):
            if (user_id == report_user):
                report_id = tran_dict['report_id']
            print(report_id)

    query_statement = trans_ref.where('report_id', '==', report_id).stream()
    for q in query_statement:
        tran_dict = q.to_dict()
        id = q.id
        product_id = tran_dict['products_id']
        product_val = tran_dict['products_val']
        area_id = tran_dict['area']
    x = 0
    while (x < len(product_id)):
        query_name = product_ref.where('product_id', '==', product_id[x]).stream()
        for q in query_name:
            tran_dict = q.to_dict()
            name_pro.append(tran_dict['product_name'])
        x += 1

    check_same = 0
    check_same_state = False

    print(product_id)
    print(product_val)
    print(area_id)
    while (check_same < len(product_id)):
        if (product_id[check_same] == area_pro_id):
            if (area_id[check_same] == area_ids):
                if (product_val[check_same] == amount):
                    check_same_state = True
                    break
        check_same += 1
    if (check_same_state == False):
        product_id.append(area_pro_id)
        area_id.append(area_ids)
        product_val.append(amount)
        name_pro.append(info_name)

    run_add_dict = 0

    while (run_add_dict < len(product_id)):
        transx = {
            "Order": run_add_dict + 1,
            "product_id": product_id[run_add_dict],
            "product_name": name_pro[run_add_dict],
            "area": area_id[run_add_dict],
            "amount": product_val[run_add_dict]
        }
        run_add_dict += 1
        wc_list.append(transx)

    # print(id)

    db.collection('transference').document(id).update(
        {"area": area_id, "products_id": product_id, "products_val": product_val})

    return render(request, "soleoutmanage.html", {'report_id': report_id, 'wc_list': wc_list, 'position': positions})


def soleoutmanage_alert(request):
    global positions
    location_id = request.POST.get('location_id')
    amount_out = request.POST.get('amount_out')

    global userid

    current_user_ref = db.collection('users').document(userid).get()
    user_id = (current_user_ref.to_dict())['id']

    trans_ref = db.collection('transference')
    query_status = trans_ref.where('status', '==', "out_warehouse").stream()
    trans_gen = trans_ref.list_documents()

    product_id = []
    product_val = []
    area_id = []
    name_pro = []
    report_id = ""

    try:
        amount = int(amount_out)
    except:

        for q in query_status:
            id = q.id
            tran_dict = q.to_dict()
            address_non = tran_dict['address']
            report_user = tran_dict['report_user_id']
            report_id = tran_dict['report_id']
            if (address_non == ""):
                if (user_id == report_user):
                    print(id)
        area_ref = db.collection('areas')
        product_ref = db.collection('products_info')
        query_area = area_ref.where('area_id', '==', location_id).stream()
        info_name = ''
        area_ids = ''
        area_pro_id = ''

        for q in query_area:
            tran_dict = q.to_dict()
            area_ids = tran_dict['area_id']
            area_pro_id = tran_dict['product_id']

        query_prod_info = product_ref.where('product_id', '==', area_pro_id).stream()
        for q in query_prod_info:
            tran_dict = q.to_dict()
            info_name = tran_dict['product_name']

        query_fine_id = trans_ref.where('status', '==', "out_warehouse").stream()

        id = ""

        for q in query_fine_id:
            tran_dict = q.to_dict()
            report_user = tran_dict['report_user_id']
            if (tran_dict['address'] == ""):
                if (user_id == report_user):
                    report_id = tran_dict['report_id']
                print(report_id)

        query_statement = trans_ref.where('report_id', '==', report_id).stream()
        for q in query_statement:
            tran_dict = q.to_dict()
            id = q.id
            product_id = tran_dict['products_id']
            product_val = tran_dict['products_val']
            area_id = tran_dict['area']

        x = 0
        while (x < len(product_id)):
            query_name = product_ref.where('product_id', '==', product_id[x]).stream()
            for q in query_name:
                tran_dict = q.to_dict()
                name_pro.append(tran_dict['product_name'])
            x += 1

        check_same = 0
        check_same_state = False

        print(product_id)
        print(product_val)
        print(area_id)

        run_add_dict = 0
        wc_list = []

        while (run_add_dict < len(product_id)):
            transx = {
                "Order": run_add_dict + 1,
                "product_id": product_id[run_add_dict],
                "product_name": name_pro[run_add_dict],
                "area": area_id[run_add_dict],
                "amount": product_val[run_add_dict]
            }
            run_add_dict += 1
            wc_list.append(transx)

        return render(request, "soleoutmanage_alert.html",
                      {'wc_list': wc_list, 'report_id': report_id, 'position': positions})


def xxxx(request):
    report_id = request.POST.get('report_id')

    print(report_id)

    address = request.POST.get('address')
    recipient = request.POST.get('recipient')
    telephone = request.POST.get('telephone')

    date = request.POST.get('date_out')
    time = request.POST.get('time')

    print(date)
    print(time)

    date_time = date + " " + time + " +07:00"  # time UTC+7

    print(date_time)

    date_time = datetime.fromisoformat(date_time)
    trans_ref = db.collection('transference')
    area_ref = db.collection('areas')
    product_ref = db.collection('products_info')
    id = ""
    query_statement = trans_ref.where('report_id', '==', report_id).stream()
    area = []
    amount = []
    product = []
    for q in query_statement:
        id = q.id
        print(id)
        tran_dict = q.to_dict()
        product = tran_dict['products_id']
        amount = tran_dict['products_val']
        area = tran_dict['area']

    i = 0

    while (i < len(product)):
        query_area = area_ref.where('area_id', '==', area[i]).stream()
        query_prod = product_ref.where('product_id', '==', product[i]).stream()

        for q in query_area:
            tran_dict = q.to_dict()
            minus_item = int(tran_dict['amount_left']) - amount[i]
            id_area = q.id
            db.collection('areas').document(id_area).update({'amount_left': minus_item})

        for q in query_prod:
            tran_dict = q.to_dict()
            minus_item = int(tran_dict['amount_total']) - amount[i]
            id_pro_info = q.id
            db.collection('products_info').document(id_pro_info).update({'amount_total': minus_item})
        i += 1

    db.collection('transference').document(id).update({"address": address,
                                                       "recipient": recipient,
                                                       "telephone": telephone,
                                                       "date": date_time, })
    return redirect('/management/')