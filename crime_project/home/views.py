from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.template import loader
from django.http import HttpResponse
from . models import *
from .models import PoliceUser
from .forms import PoliceLoginForm
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.shortcuts import render, HttpResponse



# Create your views here.
def index(request):
    return render(request, 'index.html')


def register(request):
    if request.method == "POST":
        firstname = request.POST['first_name']
        lastname = request.POST['last_name']
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password1']
        cpwd = request.POST['password2']
        if password == cpwd:
            if User.objects.filter(username=username).exists():
                messages.info(request, "⚠️ Username already taken")
                return redirect('register')
            elif User.objects.filter(email=email).exists():
                messages.info(request, "⚠️ Email already taken")
            else:
                user = User(first_name=firstname, last_name=lastname, email=email, username=username, password=password)
                user.save()

                # ---------
                police_user = PoliceUser(user=user)
                police_user.save()
                # ---------
                print("User Created")
        else:
            messages.info(request, "⚠️ Password Not Match")
            return redirect('register')
        return redirect('login')
    else:
        return render(request, 'register.html')


def login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        if User.objects.filter(username=username, password=password):
            data = User.objects.get(username=username, password=password)
            if data.username != "admin":

                request.session['uid'] = data.id
                request.session['username'] = data.username
                template = loader.get_template('user_home.html')
                context = {'session': request.session['username']}
                return HttpResponse(template.render(context, request))
            # elif data.username=="admin":
            #     template = loader.get_template('admin_home.html')
            #     context = {}
            #     return HttpResponse(template.render(context,request))
            else:
                return redirect('/user_home')
    return render(request, 'login.html')

# ----------
def police_login(request):
    if request.method == 'POST':
        form = PoliceLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None and hasattr(user, 'policeuser'):
                auth.login(request, user)
                request.session['police_user_id'] = user.policeuser.id  # Set the police_user_id in the session
                print(request.session['police_user_id'])
                return redirect('police_dashboard')
    else:
        form = PoliceLoginForm()

    return render(request, 'police_login.html', {'form': form})
# -----------


def about(request):
    return render(request, 'about.html')

def police_dashboard(request):
    context = {'username': request.user.username}
    return render(request, 'police_home.html', context)

def user_home(request):
    context = {'username': request.user.username}
    return render(request, 'user_home.html', context)



def complaint(request):
    if request.method == "POST":
        complaint = request.POST.get('complaint')
        name = request.POST.get('name')
        pin = request.POST.get('pin')
        address = request.POST.get('address')
        detail = request.POST.get('detail')

        if complaint and name and pin and address and detail:
            com = complaints()
            com.complaint = complaint
            com.details = detail
            com.address = address
            com.name = name
            com.pincode = pin
            com.user_id = request.session['uid']
            print(com)
            com.save()
            return HttpResponse("<script> alert('Your complaint was added. We will get back to you soon.');window.location='user_home';</script>")
        else:
            return HttpResponse("<script> alert('Please provide all the required data.');window.location='complaint';</script>")


    obj1=complaints.objects.all()
    return render(request,'complaint.html')

def replay(request):
    if request.method == "POST":
        # complaint = request.POST.get('complaint')
        replay = request.POST.get('replay')

        if replay:
            com = replays()
            # com.complaint = complaint
            com.replay = replay
            com.save()
            return HttpResponse("<script>alert('Replay was added.');window.location='police_dashboard';</script>")
        else:
            return HttpResponse("<script>alert('Please provide both complaint and replay.');window.location='replay';</script>")

    return render(request, 'replay.html')

def view_complaint(request):
    obj=complaints.objects.all()
    return render(request,'view_complaint.html',{'com':obj})

def view_complaintuser(request):
    id = request.session['uid']
    complaint = complaints.objects.filter(user_id=id)
    return render(request, 'view_complaintuser.html', {'uc': complaint})

def police_profile(request):
    police_user_id = request.session.get('police_user_id')
    if police_user_id:
        police_user = PoliceUser.objects.get(id=police_user_id)
        return render(request, 'police_profile.html', {'p': police_user})
    else:
        # Handle the case when police_user_id is not found in the session
        return HttpResponse("Error: Police user ID not found in session.")



def fir(request):
    # Retrieve the police stations and crime types from the database
    # police_stations = PoliceUser.objects.all
    # police_stations = PoliceUser.objects.all()
    police_stations =[]
    ps =  PoliceUser.objects.all()
    for p in ps:
        police_stations.append({"id":p.id,"station":p.station})

    crime_type =[]
    ct= crime_types.objects.all()
    for c in ct:
        crime_type.append({"id": c.id, "type": c.ctypes})


    if request.method == 'POST':
        # Process the form submission
        police_station_id = request.POST.get('police_station')
        crime_type_id = request.POST.get('crime_type')
        criminal_name = request.POST.get('criminal_name')
        criminal_address = request.POST.get('criminal_address')
        description = request.POST.get('description')

        # Create a new FIR object
        print(police_station_id,crime_type_id,criminal_name,criminal_address,)
        fir_obj = fir(police_station_id=police_station_id, crime_type_id=crime_type_id, criminal_name=criminal_name, criminal_address=criminal_address, description=description)
        fir_obj.save()

        return HttpResponse("<script>alert('FIR was added.');window.location='/police_dashboard';</script>")

    return render(request, 'fir_form.html', {'police_stations': police_stations, 'crime_types': crime_type})

def forgetpassword(request):
	if request.method=="POST":
		username=request.POST['username']
		data=User.objects.get(username=username)
		if data:
			password=request.POST['newpassword']
			cpassword=request.POST['conpassword']
			if password==cpassword:
				data.password=password; messages.info(request,"Password Changed Successfully")
				data.save(); return redirect('login')
			else:
				return HttpResponse("<script> alert('Password Mismatch');window.location='/forgetpassword';</script>")
	return render(request,'passwordchange.html')

def logout(request):
    auth.logout(request)
    return redirect('/')


