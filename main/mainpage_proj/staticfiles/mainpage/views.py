from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.urls import reverse

from django.http import HttpResponse, HttpResponseRedirect

from django.views.decorators.csrf import csrf_exempt
from django.utils.safestring import mark_safe
import os, requests
import json

TODO_URL = 'http://'+os.environ.get('TODO_IP')+ ':' +os.environ.get('TODO_PORT')
PROJECT_URL = 'http://' + os.environ.get('PROJECT_IP') + ':' + os.environ.get('PROJECT_PORT')
LOGIN_URL = 'http://' + os.environ.get('LOGIN_IP') + ':' + os.environ.get('LOGIN_PORT') 
MESSAGE_URL='http://'+os.environ.get('MESSAGE_IP')+":"+os.environ.get('MESSAGE_PORT')
USERID=""

# ============================================================================================================================ #
def call_project(id) :
    param_dict = { "userId" : id }

    URL = PROJECT_URL + '/api/proj/findProjectByUserId'
    response = requests.get(URL, params = param_dict)
    return response.json()

def front(request) :
    URL = TODO_URL + '/todo/list'
    response=requests.get(URL)
    json_data=response.json()
    arr=[]
    for i in range(len(json_data)):
        arr.append({'content': json_data[i]['content'],'pk': json_data[i]['pk']})

    project_data = call_project(request.session.get('id'))

    todo_content={'todos':arr, 'projects':project_data}
    return render(request, 'mainpage/main.html', todo_content)
# ============================================================================================================================ #

def index(request):
    if not request.session.session_key:
        return redirect(login)
    return redirect(front)

def create_todo(request):
    user_input_str = request.POST['todoContent']
    URL = TODO_URL + '/todo/createTodo'
    todo_data={"content":user_input_str}
    requests.post(URL, data=todo_data)
    return redirect(front)

def done_todo(request):
    done_todo_id=request.GET['todoNum']
    URL = TODO_URL + '/todo/doneTodo'
    URL+="/"+done_todo_id
    requests.delete(URL)
    return redirect(front)

# ============================================================================================================================ #
@csrf_exempt
def add_project(request) :
    if request.method == 'POST' :
        URL = PROJECT_URL + '/api/proj/projectInfo/' + request.session.get('id')
        response=dict(request.POST)

        print(response)

        str2=str(response['projectName'][0]) + ':' + str(response['projectDescription'][0]) + ':'
        if response.get('user_id') != None :
            arr=response['user_id']
            for i in range(len(arr)):
                str2+=arr[i]+':'

        print(str2)

        res = requests.post(URL, data=str2.encode('utf-8'))
    else :
        URL = LOGIN_URL + '/api/getUserIdAnNameList'
        res = requests.get(URL)
        return render(request, 'mainpage/mymodal.html', {'users' : res.json()})

    return redirect(front)

@csrf_exempt
def invite(request, project_id) :
    if request.method == 'POST' :
        URL = PROJECT_URL + '/api/proj/invite/' + str(project_id)
        response=dict(request.POST)
        print(response)
        print(response['user_id'])
        arr=response['user_id']
        str2=""
        for i in range(len(arr)):
            str2+=arr[i]+":"
        print(str2)
        res = requests.post(URL, data=str2)
    else :
        URL = PROJECT_URL + '/api/proj/invite/' + str(project_id)
        res = requests.get(URL)
        #print(res.json())
        return render(request, 'mainpage/invite.html', {'users' : res.json(), 'project_id' : project_id})

    return HttpResponse(status=204)
# ============================================================================================================================ #

def notice_list(request, project_id) :
    proj_list = call_project(request.session.get('id'))

    URL = PROJECT_URL + '/proj/noticeList/' + str(project_id) 
    res = requests.get(URL)
    return render(request, 'mainpage/notice_list.html', {'posts' : res.json(), 'project_id' : project_id, 'projects' : proj_list})

def get_project_detail(request, project_id) :
    URL = PROJECT_URL + '/proj/noticeList/' + str(project_id) 
    res = requests.get(URL)
    return res.json()

def goto_proj(request, project_id) :
    proj_list = call_project(request.session.get('id'))
    posts = get_project_detail(request, project_id)
    # chat 
    URL = MESSAGE_URL+'/getChat/'+str(project_id)
    response=requests.get(URL)
    json_data=response.json()
    arr=[]
    if json_data != None :
        for i in range(len(json_data)):
            arr.append({'content': json_data[i]['content'], 'user': json_data[i]['user']})
    content={'contents':arr, 
            'posts': posts,
            'project_id': project_id, 
            'projects': proj_list, 
            'room_name_json':  mark_safe(json.dumps(str(project_id))),
            'userId':request.session.get('id')
            }
    return render(request, 'mainpage/project_detail.html', content)

@csrf_exempt
def notice_new(request, project_id):
    proj_list = call_project(request.session.get('id'))

    if request.method == "POST":
        URL = PROJECT_URL + '/proj/createNotice/' + str(project_id)
        res = requests.post(URL, data = request.POST)
        return redirect('notice_list', project_id=project_id)
    return render(request, 'mainpage/notice_new.html', {'author' : request.session.get('id'), 'project_id' : project_id, 'projects' : proj_list})

@csrf_exempt
def notice_edit(request, notice_id, project_id):
    proj_list = call_project(request.session.get('id'))

    GET_POST_URL = PROJECT_URL + '/proj/noticeDetail/' + str(notice_id)
    notice_detail = requests.get(GET_POST_URL)
    post = notice_detail.json()
    if request.method == "POST":
        URL = PROJECT_URL + '/proj/updateNotice/' + str(notice_id)
        res = requests.put(URL, data = request.POST)
        if res.status_code == 200 :
            return redirect('notice_detail', notice_id=notice_id, project_id=project_id)
    return render(request, 'mainpage/notice_edit.html', {'post': post, 'notice_id' : notice_id, 'project_id' : project_id, 'projects' : proj_list})

def notice_detail(request, notice_id, project_id):
    proj_list = call_project(request.session.get('id'))

    URL = PROJECT_URL + '/proj/noticeDetail/' + str(notice_id)
    post = requests.get(URL)
    return render(request, 'mainpage/notice_detail.html', {'post': post.json(), 'notice_id' : notice_id, 'project_id' : project_id, 'projects' : proj_list})

def notice_delete(request, notice_id, project_id):
    URL = PROJECT_URL + '/proj/deleteNotice/' + str(notice_id)
    res = requests.delete(URL)
    return redirect('notice_list', project_id=project_id)

def goto_chat(request) :
    return redirect('notice_list') # update needed.

@csrf_exempt
def login(request) :
    if  request.method == "POST" :
        URL = LOGIN_URL + '/logincheck'
        res = requests.post(URL, data = request.POST)
        if res.status_code == 200 :
            request.session['id'] = request.POST.get('id')
            request.session['password'] = request.POST.get('password')
            #print(request.session.get('id'))
            global USERID
            USERID=request.session.get('id')
            print(USERID)
            print('login success!')
            return redirect('front')
        else :
            print('login error')
            return render(request, 'mainpage/login.html', {'error' : 'username or password is incorrect'})
    
    return render(request, 'mainpage/login.html')

def whoami():
    return USERID
