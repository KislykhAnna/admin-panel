from django.shortcuts import render
import pyrebase
from django.contrib import auth

config = {
    'apiKey': "AIzaSyBJFo031R9544xEGujo8DCaqpcc6qi-JC0",
    'authDomain': "testfirebase-d9e66.firebaseapp.com",
    'databaseURL': "https://testfirebase-d9e66.firebaseio.com",
    'projectId': "testfirebase-d9e66",
    'storageBucket': "testfirebase-d9e66.appspot.com",
    'messagingSenderId': "112622019277",
    'appId': "1:112622019277:web:1016a8a3aadf7b1a7d3f84"
}
firebase = pyrebase.initialize_app(config)
database = firebase.database()
authe = firebase.auth()

def signIn(request):

    return render(request, "signIn.html")

def postsign(request):
    email = request.POST.get('email')
    password = request.POST.get('pass')
    try:
        user = authe.sign_in_with_email_and_password(email, password)
    except:
        message="wrong email or password"
        return render(request, "signIn.html", {"message":message})
    print(user['idToken'])
    session_id = user['idToken']
    request.session['uid'] = str(session_id)
    return render(request, "welcome.html", {"e":email})

def logout(request):
    auth.logout(request)
    return render(request, 'signIn.html')

def signUp(request):
    return render(request, 'signUp.html')

def postsignup(request):
    name = request.POST.get('name')
    email = request.POST.get('email')
    password = request.POST.get('pass')
    try:
        user = authe.create_user_with_email_and_password(email, password)
    except:
        message = "unable to create account try again"
        return render(request, "signIn.html", {"message":message})
        uid = user['localId']
    data = {"name": name, "status": "1"}
    database.child("users").child(uid).child("details").set(data)
    return render(request, "signIn.html")

def check(request):
    records = database.child('Records').get().val()

    list = []
    for i in records:
        list.append(i)
    list.sort(reverse=True)
    print(list)

    comb_lis = zip(list, list, list)
    return render(request, 'check.html', {'comb_lis':comb_lis})

def post_check(request):
    uid = request.GET.get('z')

    topic = database.child('Records').child(uid).child('topic').get().val()
    carModel = database.child('Records').child(uid).child('carModel').get().val()
    comments = database.child('Records').child(uid).child('comments').get().val()
    date = database.child('Records').child(uid).child('date').get().val()
    userKey = database.child('Records').child(uid).child('user').get().val()

    return render(request, 'post_check.html', {'r': uid, 't':topic, 'cm':carModel, 'c':comments, 'd':date, 'u':userKey})

def record_submit(request):
    record = request.GET.get('currentrecord')
    topic = request.GET.get('topic')
    carModel = request.GET.get('carmodel')
    comments = request.GET.get('comments')
    date = request.GET.get('date')
    userKey = request.GET.get('userkey')

    data = {
        "topic": topic,
        "carmodel": carModel,
        "comments": comments,
        "date": date
    }
    database.child('Repairs').child(userKey).push(data)

    database.child('Records').child(record).remove()
    return render(request, "welcome.html")



