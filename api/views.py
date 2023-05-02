from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth import logout
from sensorapi.utils import db
from django.contrib.auth.hashers import make_password,check_password
from bson import ObjectId

# Create your views here.

def loginpage(request):
    if request.method=="POST":
        email=request.POST.get("email")
        password=request.POST.get("password")
        user=db.usermodel.find_one({"email":email})
        if user is not None:
            if check_password(password,user["password"]):
                    request.session["is_superuser"]=user["is_superuser"]
                    request.session['user']=user['username']
                    return redirect("/adminpanel")
            else:
                return HttpResponse("Invalid password")
            
        else:
            return HttpResponse("invalid username")
    return render(request,"login.html")


def adminpage(request):
    user=request.session.get("user")
    if user is not None:
        is_superuser=request.session.get("is_superuser")
        users= db.usermodel.find({"is_superuser":False})
        staffs=db.usermodel.find({"is_staff":False})

        all=[]
        if is_superuser:
            users= db.usermodel.find({"is_superuser":False})
            staffs=db.residencemodel.find({"is_active":True})
            for user in users:
                user["id"]=str(user["_id"])
                all.append(user)
            for staff in staffs:
                staff["id"]=str(staff["_id"])
                all.append(staff)
        else:
            users= db.residencemodel.find({"is_active":True})
            for user in users:
                user["id"]=str(user["_id"])
                all.append(user)
    else:
        return redirect("login")

    return render(request,"adminpanel.html",{"users":all})


def adduser(request):
    user=request.session.get("user")
    if user is not None:
        if(request.method=="POST"):
            username=request.POST.get("username")
            fname=request.POST.get("fname")
            lname=request.POST.get("lname")
            email=request.POST.get("email")
            password=request.POST.get("password")
            admin=request.POST.get("staff")
            p1=make_password(password)
            if admin:
                admin=True
            else:
                admin=False
            user=db.usermodel.find_one({"email":email})
            if not user and admin:
                user1=db.usermodel.insert_one({"username":username,"email":email,"first_name":fname,"last_name":lname,"is_staff":admin,"password":p1,"is_active":True,"is_superuser":False})
                return redirect("adminpanel")
            
            elif not user :
                user1=db.residencemodel.insert_one({"username":username,"email":email,"first_name":fname,"last_name":lname,"is_staff":admin,"password":p1,"is_active":True,"is_superuser":False})
                return redirect("adminpanel")
        
            else:
                return HttpResponse("User with this email already exist!!")
        else:
            return redirect("login")
    superuser=request.session.get("is_superuser")
    print(superuser,type(superuser))
    return render(request,"adduser.html",{"superuser":superuser})


def deleteuser(request,id):
    user=request.session.get("user")
    if user is not None:
        user=db.usermodel.find_one({"_id":ObjectId(id)})
        if user is not None and user["is_staff"]:
            db.usermodel.delete_one({"_id":ObjectId(id)})
            return redirect("adminpanel")
        else:
            db.residencemodel.delete_one({"_id":ObjectId(id)})
            return redirect("adminpanel")
    else:
        return redirect("login")

    return render(request,"adminpanel.html")


def logoutpage(request):
    try:
        del request.session['is_superuser']
    except:
        logout(request)
        return redirect('login')
    return redirect('login')


def edituser(request,id):
    user=request.session.get("user")
    if user is not None:
        if( request.method=="POST"):
            username=request.POST.get("username")
            fname=request.POST.get("fname")
            lname=request.POST.get("lname")

            user=db.usermodel.find_one({"_id":ObjectId(id)})
            if user is not None and user["is_staff"]:
                db.usermodel.update_one({"_id":ObjectId(id)},{"$set":{"username":username,"first_name":fname,"last_name":lname}})
                return redirect("adminpanel")
            
            else:
                db.residencemodel.update_one({"_id":ObjectId(id)},{"$set":{"username":username,"first_name":fname,"last_name":lname}})
                return redirect("adminpanel")
        data=[]
        user=db.usermodel.find_one({"_id":ObjectId(id)})
        if user is not None and user["is_staff"]:
            data=db.usermodel.find_one({"_id":ObjectId(id)})
        else:
            data=db.residencemodel.find_one({"_id":ObjectId(id)})
    else:
        return redirect("login")
        
    return render(request,"edit.html",{"data":data})

