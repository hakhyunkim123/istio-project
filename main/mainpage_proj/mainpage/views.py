from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.urls import reverse

from django.http import HttpResponse, HttpResponseRedirect

from django.views.decorators.csrf import csrf_exempt
from django.utils.safestring import mark_safe
from urllib.parse import urlencode, quote_plus

import requests
import json

import os, sys

from my_jwt import get_jwt_token


TODO_URL = 'http://'+os.environ.get('TODO_IP')+ ':' +os.environ.get('TODO_PORT')
PROJECT_URL = 'http://' + os.environ.get('PROJECT_IP') + ':' + os.environ.get('PROJECT_PORT')
LOGIN_URL = 'http://' + os.environ.get('LOGIN_IP') + ':' + os.environ.get('LOGIN_PORT') 
MESSAGE_URL='http://'+os.environ.get('MESSAGE_IP')+":"+os.environ.get('MESSAGE_PORT')
USERID=""

def get_forward_headers(request):
    headers = {}

    if 'id' in request.session:
        headers['end-user'] = request.session.get('id')
        
    if 'Authorization' in request.session:
        headers['Authorization'] = request.session.get('Authorization')

    #request.META['Authorization'] = headers['Authorization']
    #request.META['end-user'] = request.session.get('id')

    return headers

def call_project(request, id) :
    headers = get_forward_headers(request)
    param_dict = { "userId" : id }

    URL = PROJECT_URL + '/api/proj/findProjectByUserId'
    response = requests.get(URL, headers = headers, params = param_dict)
    return response.json()

def front(request) :
    print('11111111111111111111111111111111111111111')
    print(request.META.get('testtt'))
    for header in request.META.items():
	    print(header)
    #print(request.META.items())
    headers = get_forward_headers(request)
    URL = TODO_URL + '/todo/list'
    project_data = call_project(request, request.session.get('id'))
    res=requests.get(URL, headers = headers)

    #print('==========================================================================================')
    #print(request.META.items())
    #print(request['REQUEST_METHOD'])

    if res and res.status_code == 200 :
        json_data=res.json()
        arr=[]
        for i in range(len(json_data)):
            arr.append({'content': json_data[i]['content'],'pk': json_data[i]['pk']})

        #project_data = call_project(request.session.get('id'))

        todo_content={'todos':arr, 'projects':project_data, 'todo_list_status':res.status_code}
        return render(request, 'mainpage/main.html', todo_content)
    else:
        error_msg = 'Todo List Error.'
        todo_content={'todo_list_error':error_msg, 'projects':project_data, 'todo_list_status':res.status_code}
        return render(request, 'mainpage/main.html', todo_content)

def index(request):
	if 'id' in request.session:
		return redirect(front)
	return redirect(login)
    #if not request.session.session_key:
    #    return redirect(login)
    #return redirect(front)

def create_todo(request):
    headers = get_forward_headers(request)
    user_input_str = request.POST['todoContent']
    URL = TODO_URL + '/todo/createTodo'
    todo_data={"content":user_input_str}
    
    res = requests.post(URL, headers = headers, data=todo_data)
    
    if res and res.status_code == 200 :
        return redirect(front)
    else :
        error_msg = 'Create Todo Error.'
        param_dict = { "todo_create_error" : error_msg }
        return redirect(front, param=param_dict)

def done_todo(request):
    headers = get_forward_headers(request)
    done_todo_id=request.GET['todoNum']
    URL = TODO_URL + '/todo/doneTodo'
    URL+="/"+done_todo_id
    res = requests.delete(URL, headers = headers)
    
    if res and res.status_code == 200 :
        return redirect(front)
    else :
        error_msg = 'Done Todo Error.'
        return render(request, 'mainpage/main.html', {'todo_done_error':error_msg})

@csrf_exempt
def add_project(request) :
    headers = get_forward_headers(request)
    if request.method == 'POST' :
        URL = PROJECT_URL + '/api/proj/projectInfo/' + str(request.session.get('id'))
        response=dict(request.POST)

        print(response)

        str2=str(response['projectName'][0]) + ':' + str(response['projectDescription'][0]) + ':'
        if response.get('user_id') != None :
            arr=response['user_id']
            for i in range(len(arr)):
                str2+=arr[i]+':'

        res = requests.post(URL, headers = headers, data=str2.encode('utf-8'))
    else :
        URL = LOGIN_URL + '/api/getUserIdAnNameList'
        res = requests.get(URL, headers = headers)
        return render(request, 'mainpage/mymodal.html', {'users' : res.json()})

    return redirect(front)

@csrf_exempt
def invite(request, project_id) :
    headers = get_forward_headers(request)
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
        res = requests.post(URL, headers = headers, data=str2)
    else :
        URL = PROJECT_URL + '/api/proj/invite/' + str(project_id)
        res = requests.get(URL, headers = headers)
        #print(res.json())
        return render(request, 'mainpage/invite.html', {'users' : res.json(), 'project_id' : project_id})

    return HttpResponse(status=204)

def notice_list(request, project_id) :
    headers = get_forward_headers(request)
    proj_list = call_project(request,request.session.get('id'))

    URL = PROJECT_URL + '/proj/noticeList/' + str(project_id) 
    res = requests.get(URL, headers = headers)
    return render(request, 'mainpage/notice_list.html', {'posts' : res.json(), 'project_id' : project_id, 'projects' : proj_list})

def get_project_detail(request, project_id) :
    headers = get_forward_headers(request)
    URL = PROJECT_URL + '/proj/noticeList/' + str(project_id) 
    res = requests.get(URL, headers = headers)
    return res.json()

def goto_proj(request, project_id) :
    headers = get_forward_headers(request)
    proj_list = call_project(request, request.session.get('id'))
    posts = get_project_detail(request, project_id)
    
    # chat 
    URL = MESSAGE_URL+'/getChat/'+str(project_id)
    response=requests.get(URL, headers = headers)
    if response and response.status_code == 200 :
        json_data=response.json()
        arr=[]
        if json_data != None :
            for i in range(len(json_data)):
                arr.append({'content': json_data[i]['content'], 'user': json_data[i]['user']})
    else :
        status = res.status_code
        arr = 'Chat Error!!!!!!!'
            
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
    headers = get_forward_headers(request)
    proj_list = call_project(request, request.session.get('id'))

    if request.method == "POST":
        URL = PROJECT_URL + '/proj/createNotice/' + str(project_id)
        res = requests.post(URL, headers = headers, data = request.POST)
        return redirect('notice_list', project_id=project_id)
    return render(request, 'mainpage/notice_new.html', {'author' : request.session.get('id'), 'project_id' : project_id, 'projects' : proj_list})

@csrf_exempt
def notice_edit(request, notice_id, project_id):
    headers = get_forward_headers(request)
    proj_list = call_project(request, request.session.get('id'))

    GET_POST_URL = PROJECT_URL + '/proj/noticeDetail/' + str(notice_id)
    notice_detail = requests.get(GET_POST_URL, headers = headers)
    post = notice_detail.json()
    if request.method == "POST":
        URL = PROJECT_URL + '/proj/updateNotice/' + str(notice_id)
        res = requests.put(URL, headers = headers, data = request.POST)
        if res.status_code == 200 :
            return redirect('notice_detail', notice_id=notice_id, project_id=project_id)
    return render(request, 'mainpage/notice_edit.html', {'post': post, 'notice_id' : notice_id, 'project_id' : project_id, 'projects' : proj_list})

def notice_detail(request, notice_id, project_id):
    headers = get_forward_headers(request)
    proj_list = call_project(request, request.session.get('id'))

    URL = PROJECT_URL + '/proj/noticeDetail/' + str(notice_id)
    post = requests.get(URL, headers = headers)
    return render(request, 'mainpage/notice_detail.html', {'post': post.json(), 'notice_id' : notice_id, 'project_id' : project_id, 'projects' : proj_list})

def notice_delete(request, notice_id, project_id):
    headers = get_forward_headers(request)
    URL = PROJECT_URL + '/proj/deleteNotice/' + str(notice_id)
    res = requests.delete(URL, headers = headers)
    return redirect('notice_list', project_id=project_id)

def goto_chat(request) :
    return redirect('notice_list') # update needed.

@csrf_exempt
def login(request) :
    if  request.method == "POST" :
        headers = {}
        headers['end-user'] = request.POST.get('id')
        headers['Authorization'] = 'Bearer ' + get_jwt_token()
        URL = LOGIN_URL + '/logincheck'
        res = requests.post(URL, headers=headers, data = request.POST)
        if res.status_code == 200 :
            request.session['id'] = request.POST.get('id')
            request.session['password'] = request.POST.get('password')

            jwt_token = get_jwt_token()
            request.session['Authorization'] = str(jwt_token)

            #Authorization =  urlencode({'Authoriztion': jwt_token})
            #Authorization =  urlencode(jwt_token)

            #url = '{}?{}'.format('https://52.231.52.58:30724/front/', jwt_token)
            #response.headers = {'Authorization' : jwt_token}
            
            #response = redirect(reverse('front'))

            response = HttpResponseRedirect(reverse('front'))
            #response = render(request, 'mainpage/main.html', {})
            response['end-user'] = request.POST.get('id')
            response['Authorization'] = str(jwt_token)
            response['testtt'] = 'abcd'
			
            #response = requests.get('http://20.41.82.195:9000/front/')
            #print(requests.history)

            global USERID
            USERID=request.session.get('id')
            #print(USERID)
            #print(request.session.get('authorization'))
            #print(request.META.items())
            print('login success!')
            return response
            #return redirect(url)
        else :
            print('login error')
            return render(request, 'mainpage/login.html', {'error' : 'username or password is incorrect'})
    
    return render(request, 'mainpage/login.html')

def whoami():
    return USERID
