from django.shortcuts import render
import paramiko,time,os,json
from django.http.response import HttpResponse
from django.core.files.base import ContentFile
from django.urls import resolve
import csv
from App1.forms import ChooseTaskForm,LoginAuthentication,ScriptDetails,HomeForm,RunCommands,DocumentForm,CreateFolderPlaybook,CreateVPC,CreateSecurityGroup
from App1.forms import LB_CreateNode,LB_CreatePool,LB_DeletePool,LB_DeleteNode,Linux_CreateLogicalVolume,Linux_DeleteLogicalVolume,Linux_CreateVolumeGroup,Linux_DeleteVolumeGroup
from App1.forms import Windows_installFeature,Windows_uninstallFeature,Windows_ManageService,LB_ManagePool
from App1.forms import Manage_Fortigate
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from django.contrib.auth.models import User

import datetime
PROJECT_PATH = os.path.abspath(os.path.dirname(__name__)) 
print(PROJECT_PATH)
DocPath=PROJECT_PATH+"/App1/static/Documents/"
print(DocPath)
def Home(request):
    userList =User.objects.values()
    users=[]
    userDict={}
    for user in userList:
        users.append(user["username"])
    userDict["users"]=users
    return render(request,"Home.html",{"homeData" : userDict})
def mainMenu(request):
    option = request.GET.get('option', None)
    print(option)
    menuList={} 
    if  option=='DCPrivateCloud':
        menuList["option"]="DataCenter And Privatecloud"
    elif option=='PublicCloud':
        menuList["option"]="Public Cloud"
    elif option=='NetworkUC':
        menuList["option"]="Network and UC"
    return render(request,"main.html",{'tagsList' : menuList })
def dashboard(request):
    data={}
    data["dashboard"]="yes"
    return render(request,"Automations.html",{'data' : data})
def automations(request):
    finaldata={}
    if request.method == 'POST':
        print("in post method")
        urlValue=resolve(request.path_info).url_name
        print(urlValue)
        if urlValue=="scripts":
            try:
                form1 = ScriptDetails()
                inputData=request.POST.dict()
                csv_file = request.FILES["document"]
                BASE_PATH=PROJECT_PATH+"\\Documents"
                csv_file = request.FILES["document"]
                if not csv_file.name.endswith('.csv'):
                    finaldata["message"]="Failed to upload file, Please select valid csv file"
                    return render(request,"Automations.html", {'form': form1 , 'data' : finaldata})
                else:
                    full_filename = BASE_PATH+"\\"+request.FILES["document"].name
                    print("full filename is " + full_filename)
                    fout = open(full_filename, 'wb+')
                    for chunk in request.FILES['document'].chunks():
                        fout.write(chunk)
                    fout.close()
                if inputData["NewPassword"]!=inputData["ConformPassWord"]:
                    finaldata["message"]="Your password and confirmation password do not match, Please Check"
                    return render(request,"Automations.html", {'form': form1 , 'data' : finaldata})
                
                rootUserName=inputData["RootUserName"]
                rootPwd=inputData["RootPassword"]
                newUserName=inputData["NewUserName"]
                newPwd=inputData["NewPassword"]  
                newCfrmPwd=inputData["ConformPassWord"]
                ####### connecting to the server where script is placed ###########
                try:
                    ssh=paramiko.SSHClient()
                    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                    ssh.connect("172.22.110.194",22,"root","Pass@123")
                    sftp = ssh.open_sftp()
                    print(PROJECT_PATH+"\\Documents\\"+request.FILES["document"].name)
                    sftp.put(PROJECT_PATH+"/Documents/"+request.FILES["document"].name, "/root/scripts/Documents/"+request.FILES["document"].name)
                    cmd="ls"
                    stdin,stdout,stderr=ssh.exec_command(cmd)
                    outlines=stdout.readlines()
                    sftp.close()
                    ssh.close()
                    finaldata["status"]="Success"
                except Exception as e:
                    finaldata["status"]="Failed"
                    print("unable to connect device" ,str(e)) 
                return render(request,"Automations.html", {'form': form1 ,'data' : finaldata})  #, 'chnagepwdForm':form2, 
            except Exception as e:
                print(e)
                form = ScriptDetails()
                finaldata["headerMsg"]="Please Fill The Below Details..."
                return render(request,"Automations.html", {'form': form , 'data' : finaldata})
            form=RunCommands()
            return render(request,"Automations.html", {'form': form , 'data' : finaldata})
    else:
        urlValue=resolve(request.path_info).url_name
        print(urlValue)
        if urlValue=="automations":
            deviceDomain = request.GET.get('devType', None)
            option = request.GET.get('option',None)
            print(deviceDomain)
            print(option)
            form=RunCommands()
            if deviceDomain is not None :
                tagsDict={} 
                if deviceDomain=='AWS' and option =='PublicCloud':
                    tagsDict["securityGroupRulesManagement"]="Security GroupRules Management"
                    tagsDict["vpcCreation"]="Create VPC"
                    finaldata['deviceDomain']="AWS"
                    finaldata['option']="Public Cloud"
                    finaldata["tags"]=tagsDict  
                    finaldata["tag_display_msg"]="Below are the list of usecases in AWS, Please choose one" 
                                           
                elif deviceDomain=='LoadBalancer' and option == 'NetworkUC':
                    tagsDict["createPool"]="Create Pool"
                    tagsDict["deletePool"]="Delete Pool"
                    tagsDict["createNode"]="Create Node"
                    tagsDict["deleteNode"]="Delete Node"
                    finaldata["deviceDomain"]="LoadBalancer"
                    finaldata["option"]="Network and UC"
                    finaldata["tags"]=tagsDict
                    finaldata["tag_display_msg"]="Below are the list of usecases in LoadBalancer, Please choose one"
                                  
                elif deviceDomain=='Linux' and option == 'DCPrivateCloud':
                    tagsDict["createLogicalVolume"]="Create Logical Volume"
                    tagsDict["deleteLogicalVolume"]="Delete Logical Volume"
                    tagsDict["createVolumeGroup"]="Create Volume Group"
                    tagsDict["deleteVolumeGroup"]="Delete Volume Group"
                    finaldata["deviceDomain"]="Linux"
                    finaldata["option"]="DataCenter And Privatecloud"
                    finaldata["tags"]=tagsDict
                    finaldata["tag_display_msg"]="Below are the list of usecases in Linux, Please choose one"                   
                
                elif deviceDomain=='Windows' and option == 'DCPrivateCloud':
                    tagsDict["installFeature"]="Install New Feature"
                    tagsDict["uninstallFeature"]="Uninstall Feature"
                    tagsDict["manageService"]="Manage Service"
                    finaldata["deviceDomain"]="Windows"
                    finaldata["option"]="DataCenter And Privatecloud"
                    finaldata["tags"]=tagsDict
                    finaldata["tag_display_msg"]="Below are the list of usecases in Windows, Please choose one"
                    
                elif deviceDomain=='Network Security' and option == 'NetworkUC':
                    tagsDict["manage_Fortigate"]="Manage Fortigate"
                    finaldata["deviceDomain"]="Network Security"
                    finaldata["tags"]=tagsDict
                    finaldata["tag_display_msg"]="Below are the list of usecases in Network , Please choose one"
         
            return render(request,"main.html", {'tagsList' : finaldata})  
        elif urlValue=="scripts":
            finaldata["headerMsg"]="Please choose action from below list"
            form=ChooseTaskForm()
            return render(request,"Automations.html", {'form': form , 'data' : finaldata})
# def Login(request):
#     finaldata={}
#     print(request.method)
# #     models.conncetion()
#     
#     if request.method=="POST":
#         print("in Login method")
#         if request.user.is_authenticated:
#             print("user is authenticated")
#         else:
#             print("user is not authenticated")
#         form=LoginAuthentication()
#         data=request.POST.dict()
#         print(data)
#         if data:
#             if data['userName']=="udaya545" and data["password"]=="09mu1a0545":
#                 return render(request, "index.html" , {'form': form , 'data' : finaldata})
#             else:
#                 finaldata['message']="Login failed, Provid valid user details"
#                 return render(request,"login.html", {'form':form ,'data': finaldata})
#     else:
#         form=LoginAuthentication()
#         return render(request, "login.html" , {'form': form , 'data' : finaldata})
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='accounts/login')
def index(request):
    userInfo={}
    print(request.user.get_username())
    userInfo["userName"]=request.user.get_username()
    if request.user.is_superuser:
        userInfo["is_admin"]="yes"
    else:
        userInfo["is_admin"]="no"
    return render(request,"index.html",{"userInfo" : userInfo})


def showChangePwdResults(request):
    with open(PROJECT_PATH+'/Documents/Results.json') as d:
        Results = json.load(d)
        
    print(Results)
    return render(request,"Automations.html", {'ChangePwdResults' : Results})

def runPlaybooks(request):
    return render(request, "ShowPlaybooks.html")

def ChangeManagement(request):
    print("in change management method")
    data={}
    data["tabs"]=["DC & Private Cloud","Public Cloud","Network and UC"]
    return render(request,"Automations.html",{'data':data})

def createFolderPlaybook(request):
    finaldata={}
    finaldata['headerMsg'] = "    Creating Folder   "
    if request.method == 'POST':
        form=CreateFolderPlaybook()
        data = request.POST.dict()
        if(data['ipAddress'] == '' or data['port'] == '' or data['username']== '' or data['password'] == ''):
            finaldata["status"]="Please fill all the details"
        else:
            ssh=paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(data['ipAddress'],data['port'],data['username'],data['password'])
            sftp = ssh.open_sftp()
            cmd='ansible-playbook /home/udaya545/ansible_playbooks/createFolder_linux.yml --extra-vars "path='+data["folderPath"]+'"'
            print(cmd)
            stdin,stdout,stderr=ssh.exec_command(cmd)
            outlines=stdout.readlines()
            print(outlines)
            sftp.close()
            ssh.close()
            if 'FAILED' in outlines:
                finaldata["status"]="We are unable to do this task on end device"
            else:
                finaldata["status"]="Folder created succesfully please check it once"
        return render(request,"RunPlaybooks.html",{'createFolderplaybookForm':form,'data':finaldata})
    form=CreateFolderPlaybook()
    print(form)
    return render(request,"RunPlaybooks.html",{'createFolderplaybookForm':form,'data':finaldata})

def createVPC(request):
    try:
        print(" in create VPC method")
        GetData={}
        if request.method == 'POST':
            option = request.GET.get('option',None)            
            GetData["option"]=option           
            data=request.POST.dict()            
            print(data)
            if "csrfmiddlewaretoken" in data:
                    del data['csrfmiddlewaretoken']
            vpc_name=data["vpc_name"]
            vpc_cidr=data["vpc_cidr"]
            vpc_state=data["vpc_state"]
            dns_support=data["dns_support"]
            dns_hostnames=data["dns_hostnames"]
            tenancy=data["tenancy"]
            executionType=data["Execution_method"]
            GetData["ScriptName"]="vpcCreation"
            GetData["Input"]=data
            print(executionType)
            
            if executionType=="ssh":
                cmd = 'ansible-playbook /etc/ansible/createVPC.yml --extra-vars "vpc_name='+vpc_name+' vpc_cidr='+vpc_cidr+' vpc_state='+vpc_state+' dns_support='+dns_support+' dns_hostnames='+dns_hostnames+' tenancy='+tenancy+'" --tags  "'+GetData["ScriptName"]+'" -vvvv'
                resp,flag,filePath = runPlayBook_SSH(cmd,GetData["ScriptName"])
                GetData["Output"]=resp
                if flag=="success":        
                    with open(DocPath+filePath, 'w') as fileP:
                        fileP.write(GetData["Output"])
                    GetData["filePath"]=filePath
                
            elif executionType=="jenkins":
                finalString1 = '" -d "'.join("{!s}={!s}".format(key,val) for (key,val) in data.items())
                finalString = '"{}"'.format(finalString1)
                cmd='curl -d ' + finalString + ' -i -X POST http://admin:admin@172.22.110.191:8080/job/'+GetData["ScriptName"]+'/buildWithParameters -H "Jenkins-Crumb:4587c8c2d29e8453ba570654c5248554"'
                resp,flag,filePath,statusOfTask=runPlayBook_Jenkins(cmd,GetData["ScriptName"])
                if statusOfTask:
                    GetData["Status"]=statusOfTask
                GetData["Output"]=resp
                if flag=="success":        
                    with open(DocPath+filePath, 'w') as fileP:
                        fileP.write(GetData["Output"])
                    GetData["filePath"]=filePath
                
            return render(request,"main.html",{'tagsList':GetData})
        else:
            form=CreateVPC()
            option = request.GET.get('option',None)
            GetData["headerMsg"]="Create New VPC"
            GetData["option"]=option
            GetData["tagName"]="vpcCreation"
            return render(request,"main.html",{'taskForm':form,'tagsList':GetData})
    except Exception as e:
        print(e)
        form=CreateVPC()
        return render(request,"Automations.html",{'creatVPCform':form,'data':{}})
    
def createSecurityGroup(request):
    try:
        print(" in create securityGroupRulesManagement method")
        GetData={}
        if request.method == 'POST':
            data=request.POST.dict()
            option = request.GET.get('option',None)            
            GetData["option"]=option  
            if "csrfmiddlewaretoken" in data:
                    del data['csrfmiddlewaretoken']
            security_group_state = data["security_group_state"]
            security_group_name = data["security_group_name"]
            security_group_description = data["security_group_description"]
            vpc_id = data["vpc_id"]
            ingress_protocol = data["ingress_protocol"]
            ingress_port_from = data["ingress_port_from"]
            ingress_port_to = data["ingress_port_to"]
            ingress_destination_cidr_block = data["ingress_destination_cidr_block"]
            egress_protocol = data["egress_protocol"]
            egress_port_to = data["egress_port_to"]
            egress_destination_cidr_block = data["egress_destination_cidr_block"]
            executionType = data["Execution_method"]
            GetData["ScriptName"]="securityGroupRulesManagement"
            GetData["Input"]=data
            print(executionType)
            
            if executionType=="ssh":
                cmd = '''ansible-playbook /etc/ansible/createVPC.yml --extra-vars "security_group_state='''+security_group_state+'''
                             security_group_name='''+security_group_name+''' security_group_description='''+security_group_description+'''
                            vpc_id='''+vpc_id+''' ingress_protocol='''+ingress_protocol+''' ingress_port_from='''+ingress_port_from+''' 
                            ingress_port_to='''+ingress_port_to+''' ingress_destination_cidr_block='''+ingress_destination_cidr_block+'''
                            egress_protocol='''+egress_protocol+''' egress_port_to='''+egress_port_to+''' egress_destination_cidr_block='''+egress_destination_cidr_block+'''"
                             --tags  "'''+GetData["ScriptName"]+'''" -vvvv'''
                resp,flag,filePath = runPlayBook_SSH(cmd,GetData["ScriptName"])
                GetData["Output"]=resp
                if flag=="success":        
                    with open(DocPath+filePath, 'w') as json_file:
                        json.dump(GetData, json_file)
                    GetData["filePath"]=filePath
                
            elif executionType=="jenkins":
                finalString1 = '" -d "'.join("{!s}={!s}".format(key,val) for (key,val) in data.items())
                finalString = '"{}"'.format(finalString1)
                cmd='curl -d ' + finalString + ' -i -X POST http://admin:admin@172.22.110.191:8080/job/'+GetData["ScriptName"]+'/buildWithParameters -H "Jenkins-Crumb:4587c8c2d29e8453ba570654c5248554"'
                resp,flag,filePath,statusOfTask=runPlayBook_Jenkins(cmd,GetData["ScriptName"])
                if statusOfTask:
                    GetData["Status"]=statusOfTask
                GetData["Output"]=resp
                if flag=="success":        
                    with open(DocPath+filePath, 'w') as fileP:
                        fileP.write(GetData["Output"])
                    GetData["filePath"]=filePath
                
            return render(request,"main.html",{'tagsList':GetData})
        else:
            form=CreateSecurityGroup()
            option = request.GET.get('option',None)
            GetData["headerMsg"]="New SecurityGroup Creation"
            GetData["option"]=option
            GetData["tagName"]="securityGroupRulesManagement"
            return render(request,"main.html",{'taskForm':form,'tagsList':GetData})
    except Exception as e:
        print(e)
        form=CreateSecurityGroup()
        return render(request,"Automations.html",{'CreateSecurityGroup':form,'data':{}})
    
def createNode_LB(request):
    try:
        print(" in createNode_LB method")
        GetData={}
        if request.method == 'POST':
            data=request.POST.dict()
            option = request.GET.get('option',None)            
            GetData["option"]=option  
            if "csrfmiddlewaretoken" in data:
                    del data['csrfmiddlewaretoken']
            host=data["host"]
            node_name=data["node_name"]
            executionType = data["Execution_method"]
            GetData["ScriptName"]="createNode"
            GetData["Input"]=data
            print(executionType)
            if executionType=="ssh":
                ssh=paramiko.SSHClient()
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh.connect("172.22.110.192",22,"root","Pass@1234")
                cmd = 'ansible-playbook /etc/ansible/LoadBalancer.yaml --extra-vars "host='+host+' node_name='+node_name+'" --tags  "'+GetData["ScriptName"]+'" -vvvv'
                resp,flag,filePath = runPlayBook_SSH(cmd,GetData["ScriptName"])
                GetData["Output"]=resp
                if flag=="success":        
                    with open(DocPath+filePath, 'w') as json_file:
                        json.dump(GetData, json_file)
                    GetData["filePath"]=filePath
                
            elif executionType=="jenkins":
                finalString1 = '" -d "'.join("{!s}={!s}".format(key,val) for (key,val) in data.items())
                finalString = '"{}"'.format(finalString1)
                cmd='curl -d ' + finalString + ' -i -X POST http://admin:admin@172.22.110.191:8080/job/'+GetData["ScriptName"]+'/buildWithParameters -H "Jenkins-Crumb:4587c8c2d29e8453ba570654c5248554"'
                resp,flag,filePath,statusOfTask=runPlayBook_Jenkins(cmd,GetData["ScriptName"])
                if statusOfTask:
                    GetData["Status"]=statusOfTask
                GetData["Output"]=resp
                if flag=="success":        
                    with open(DocPath+filePath, 'w') as fileP:
                        fileP.write(GetData["Output"])
                    GetData["filePath"]=filePath
         
            return render(request,"main.html",{'tagsList':GetData})
        else:
            form=LB_CreateNode()
            option = request.GET.get('option',None)
            GetData["headerMsg"]="Create Node"
            GetData["option"]=option
            GetData["tagName"]="createNode"
            return render(request,"main.html",{'taskForm':form,'tagsList':GetData})
    except Exception as e:
        print(e)
        form=LB_CreateNode()
        return render(request,"Automations.html",{'LB_CreateNodeForm':form,'data':{}})
   
def deleteNode_LB(request):
    
    try:
        print(" in deleteNode_LB method")
        GetData={}
        if request.method == 'POST':
            data=request.POST.dict()
            option = request.GET.get('option',None)            
            GetData["option"]=option  
            if "csrfmiddlewaretoken" in data:
                    del data['csrfmiddlewaretoken']
            
            node_name=data["node_name"]
            executionType = data["Execution_method"]
            GetData["ScriptName"]="deleteNode"
            GetData["Input"]=data
            print(executionType)
            if executionType=="ssh":
                ssh=paramiko.SSHClient()
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh.connect("172.22.110.192",22,"root","Pass@1234")
                cmd = 'ansible-playbook /etc/ansible/LoadBalancer.yaml --extra-vars "node_name='+node_name+'" --tags  "'+GetData["ScriptName"]+'" -vvvv'
                resp,flag,filePath = runPlayBook_SSH(cmd,GetData["ScriptName"])
                GetData["Output"]=resp
                if flag=="success":        
                    with open(DocPath+filePath, 'w') as json_file:
                        json.dump(GetData, json_file)
                    GetData["filePath"]=filePath
                
            elif executionType=="jenkins":
                finalString1 = '" -d "'.join("{!s}={!s}".format(key,val) for (key,val) in data.items())
                finalString = '"{}"'.format(finalString1)
                cmd='curl -d ' + finalString + ' -i -X POST http://admin:admin@172.22.110.191:8080/job/'+GetData["ScriptName"]+'/buildWithParameters -H "Jenkins-Crumb:4587c8c2d29e8453ba570654c5248554"'
                resp,flag,filePath,statusOfTask=runPlayBook_Jenkins(cmd,GetData["ScriptName"])
                if statusOfTask:
                    GetData["Status"]=statusOfTask
                GetData["Output"]=resp
                if flag=="success":        
                    with open(DocPath+filePath, 'w') as fileP:
                        fileP.write(GetData["Output"])
                    GetData["filePath"]=filePath
         
            return render(request,"main.html",{'tagsList':GetData})
        else:
            form=LB_DeleteNode()
            option = request.GET.get('option',None)
            GetData["headerMsg"]="Delete Node"
            GetData["option"]=option
            GetData["tagName"]="deleteNode"
            return render(request,"main.html",{'taskForm':form,'tagsList':GetData})
    except Exception as e:
        print(e)
        form=LB_DeleteNode()
        return render(request,"Automations.html",{'LB_DeleteNodeForm':form,'data':{}})
   

def createPool_LB(request):
    try:
        print(" in createPool_LB method")
        GetData={}
        if request.method == 'POST':
            data=request.POST.dict()
            option = request.GET.get('option',None)            
            GetData["option"]=option  
            if "csrfmiddlewaretoken" in data:
                    del data['csrfmiddlewaretoken']
            pool_name=data["pool_name"]
            partition=data["partition"]
            lb_method=data["lb_method"]
            slow_ramp_time=data["slow_ramp_time"]
            executionType = data["Execution_method"]
            GetData["ScriptName"]="createPool"
            GetData["Input"]=data
            print(executionType)
            
            if executionType=="ssh":
                cmd = 'ansible-playbook /etc/ansible/LoadBalancer.yaml --extra-vars "partition='+partition+' lb_method='+lb_method+'  slow_ramp_time='+slow_ramp_time+'" --tags  "'+GetData["ScriptName"]+'" -vvvv'
                resp,flag,filePath = runPlayBook_SSH(cmd,GetData["ScriptName"])
                GetData["Output"]=resp
                if flag=="success":        
                    with open(DocPath+filePath, 'w') as json_file:
                        json.dump(GetData, json_file)
                    GetData["filePath"]=filePath
                
            elif executionType=="jenkins":
                finalString1 = '" -d "'.join("{!s}={!s}".format(key,val) for (key,val) in data.items())
                finalString = '"{}"'.format(finalString1)
                cmd='curl -d ' + finalString + ' -i -X POST http://admin:admin@172.22.110.191:8080/job/'+GetData["ScriptName"]+'/buildWithParameters -H "Jenkins-Crumb:4587c8c2d29e8453ba570654c5248554"'
                resp,flag,filePath,statusOfTask=runPlayBook_Jenkins(cmd,GetData["ScriptName"])
                if statusOfTask:
                    GetData["Status"]=statusOfTask
                GetData["Output"]=resp
                if flag=="success":        
                    with open(DocPath+filePath, 'w') as fileP:
                        fileP.write(GetData["Output"])
                    GetData["filePath"]=filePath
           
            return render(request,"main.html",{'tagsList':GetData})
        else:
            form=LB_CreatePool()
            option = request.GET.get('option',None)
            GetData["headerMsg"]="Create Pool"
            GetData["option"]=option
            GetData["tagName"]="createPool"
            return render(request,"main.html",{'taskForm':form,'tagsList':GetData})
    except Exception as e:
        print(e)
        form=LB_CreatePool()
        return render(request,"Automations.html",{'LB_createPoolForm':form,'data':{}})
   

def deletePool_LB(request):
    try:
        print(" in deletePool_LB method")
        GetData={}
        if request.method == 'POST':
            data=request.POST.dict()
            option = request.GET.get('option',None)            
            GetData["option"]=option  
            if "csrfmiddlewaretoken" in data:
                    del data['csrfmiddlewaretoken']
            pool_name=data["pool_name"]
            partition=data["partition"]
            executionType = data["Execution_method"]
            GetData["ScriptName"]="deletePool"
            GetData["Input"]=data
            print(executionType)
            
            if executionType=="ssh":
                cmd = 'ansible-playbook /etc/ansible/LoadBalancer.yaml --extra-vars "pool_name='+pool_name+' partition='+partition+'" --tags  "'+GetData["ScriptName"]+'" -vvvv'
                resp,flag,filePath = runPlayBook_SSH(cmd,GetData["ScriptName"])
                GetData["Output"]=resp
                if flag=="success":        
                    with open(DocPath+filePath, 'w') as json_file:
                        json.dump(GetData, json_file)
                    GetData["filePath"]=filePath
                
                    
            elif executionType=="jenkins":
                finalString1 = '" -d "'.join("{!s}={!s}".format(key,val) for (key,val) in data.items())
                finalString = '"{}"'.format(finalString1)
                cmd='curl -d ' + finalString + ' -i -X POST http://admin:admin@172.22.110.191:8080/job/'+GetData["ScriptName"]+'/buildWithParameters -H "Jenkins-Crumb:4587c8c2d29e8453ba570654c5248554"'
                resp,flag,filePath,statusOfTask=runPlayBook_Jenkins(cmd,GetData["ScriptName"])
                if statusOfTask:
                    GetData["Status"]=statusOfTask
                GetData["Output"]=resp
                if flag=="success":        
                    with open(DocPath+filePath, 'w') as fileP:
                        fileP.write(GetData["Output"])
                    GetData["filePath"]=filePath
           
            return render(request,"main.html",{'tagsList':GetData})
        else:
            form=LB_DeletePool()
            option = request.GET.get('option',None)
            GetData["headerMsg"]="Delete Pool"
            GetData["option"]=option
            GetData["tagName"]="deletePool"
            return render(request,"main.html",{'taskForm':form,'tagsList':GetData})
    except Exception as e:
        print(e)
        form=LB_DeletePool()
        return render(request,"Automations.html",{'LB_DeletePoolForm':form,'data':{}})

def managePool_LB(request):
    try:
        print(" in managePool_LB method")
        GetData={}
        if request.method == 'POST':
            data=request.POST.dict()
            option = request.GET.get('option',None)            
            GetData["option"]=option
            if "csrfmiddlewaretoken" in data:
                    del data['csrfmiddlewaretoken']
            pool_name=data["pool_name"]
            state=data["state"]
            partition=data["partition"]
            executionType = data["Execution_method"]
            GetData["ScriptName"]="managePool"
            GetData["Input"]=data
            print(executionType)

            if executionType=="ssh":
                cmd = 'ansible-playbook /etc/ansible/LoadBalancer.yaml --extra-vars "pool_name='+pool_name+' partition='+partition+'" --tags  "'+GetData["ScriptName"]+'" -vvvv'
                resp,flag,filePath = runPlayBook_SSH(cmd,GetData["ScriptName"])
                GetData["Output"]=resp
                if flag=="success":
                    with open(DocPath+filePath, 'w') as json_file:
                        json.dump(GetData, json_file)
                    GetData["filePath"]=filePath

            elif executionType=="jenkins":
                finalString1 = '" -d "'.join("{!s}={!s}".format(key,val) for (key,val) in data.items())
                finalString = '"{}"'.format(finalString1)
                cmd='curl -d ' + finalString + ' -i -X POST http://admin:admin@172.22.110.191:8080/job/'+GetData["ScriptName"]+'/buildWithParameters -H "Jenkins-Crumb:4587c8c2d29e8453ba570654c5248554"'
                resp,flag,filePath,statusOfTask=runPlayBook_Jenkins(cmd,GetData["ScriptName"])
                if statusOfTask:
                    GetData["Status"]=statusOfTask
                GetData["Output"]=resp
                if flag=="success":        
                    with open(DocPath+filePath, 'w') as fileP:
                        fileP.write(GetData["Output"])
                    GetData["filePath"]=filePath

            return render(request,"main.html",{'tagsList':GetData})
        else:
            form=LB_ManagePool()
            option = request.GET.get('option',None)
            GetData["headerMsg"]="Manage Pool"
            GetData["option"]=option
            GetData["tagName"]="managePool"
            return render(request,"main.html",{'taskForm':form,'tagsList':GetData})
    except Exception as e:
        print(e)
        form=LB_ManagePool()
        return render(request,"Automations.html",{'LB_ManagePoolForm':form,'data':{}})
    
def createLogicalVolume_Linux(request):
    try:
        print(" in createLogicalVolume_Linux method")
        GetData={}
        if request.method == 'POST':
            data=request.POST.dict()
            option = request.GET.get('option',None)            
            GetData["option"]=option
            print(data)
            if "csrfmiddlewaretoken" in data:
                    del data['csrfmiddlewaretoken']
            server=data["server"]
            volume_group_name=data["volume_group_name"]
            logical_volume_name=data["logical_volume_name"]
            physcal_extent_size=data["physcal_extent_size"]
            physical_volumes = data["physical_volumes"]
            executionType = data["Execution_method"]
            GetData["ScriptName"]="createLogicalVolume"
            GetData["Input"]=data
            print(executionType)
            
            if executionType=="ssh":
                cmd = '''ansible-playbook /etc/ansible/Linux.yml --extra-vars "server='''+server+''' 
                         volume_group_name='''+volume_group_name+''' logical_volume_name='''+logical_volume_name+'''
                         physcal_extent_size='''+physcal_extent_size+''' physical_volumes='''+physical_volumes+''' " --tags  "'''+GetData["ScriptName"]+'''" -vvvv'''
                resp,flag,filePath = runPlayBook_SSH(cmd,GetData["ScriptName"])
                GetData["Output"]=resp
                if flag=="success":        
                    with open(DocPath+filePath, 'w') as json_file:
                        json.dump(GetData, json_file)
                    GetData["filePath"]=filePath
                    
            elif executionType=="jenkins":
                finalString1 = '" -d "'.join("{!s}={!s}".format(key,val) for (key,val) in data.items())
                finalString = '"{}"'.format(finalString1)
                cmd='curl -d ' + finalString + ' -i -X POST http://admin:admin@172.22.110.191:8080/job/'+GetData["ScriptName"]+'/buildWithParameters -H "Jenkins-Crumb:4587c8c2d29e8453ba570654c5248554"'
                resp,flag,filePath,statusOfTask=runPlayBook_Jenkins(cmd,GetData["ScriptName"])
                if statusOfTask:
                    GetData["Status"]=statusOfTask
                GetData["Output"]=resp
                if flag=="success":        
                    with open(DocPath+filePath, 'w') as fileP:
                        fileP.write(GetData["Output"])
                    GetData["filePath"]=filePath
                   
            return render(request,"main.html",{'tagsList':GetData})
        else:
            form=Linux_CreateLogicalVolume()
            option = request.GET.get('option',None)
            GetData["headerMsg"]="Create LogicalVolume"
            GetData["option"]=option
            GetData["tagName"]="createLogicalVolume"
            return render(request,"main.html",{'taskForm':form,'tagsList':GetData})
    except Exception as e:
        print(e)
        form=Linux_CreateLogicalVolume()
        return render(request,"Automations.html",{'Linux_createLogicalVolume':form,'data':{}})
    
def deleteLogicalVolume_Linux(request):
    try:
        print(" in deleteLogicalVolume_Linux method")
        GetData={}
        if request.method == 'POST':
            data=request.POST.dict()
            option = request.GET.get('option',None)            
            GetData["option"]=option
            print(data)
            if "csrfmiddlewaretoken" in data:
                    del data['csrfmiddlewaretoken']
            server=data["server"]
            #username=data["username"]
            #password=data["password"]
            volume_group_name=data["volume_group_name"]
            logical_volume_name=data["logical_volume_name"]
            executionType = data["Execution_method"]
            GetData["ScriptName"]="deleteLogicalVolume"
            GetData["Input"]=data
            print(executionType)
            
            if executionType=="ssh":
                cmd = '''ansible-playbook /etc/ansible/Linux.yml --extra-vars "server='''+server+'''
                         volume_group_name='''+volume_group_name+''' logical_volume_name='''+logical_volume_name+'''" --tags  "'''+GetData["ScriptName"]+'''" -vvvv'''
                resp,flag,filePath = runPlayBook_SSH(cmd,GetData["ScriptName"])
                GetData["Output"]=resp
                if flag=="success":        
                    with open(DocPath+filePath, 'w') as json_file:
                        json.dump(GetData, json_file)
                    GetData["filePath"]=filePath
                
            elif executionType=="jenkins":
                finalString1 = '" -d "'.join("{!s}={!s}".format(key,val) for (key,val) in data.items())
                finalString = '"{}"'.format(finalString1)
                cmd='curl -d ' + finalString + ' -i -X POST http://admin:admin@172.22.110.191:8080/job/'+GetData["ScriptName"]+'/buildWithParameters -H "Jenkins-Crumb:4587c8c2d29e8453ba570654c5248554"'
                resp,flag,filePath,statusOfTask=runPlayBook_Jenkins(cmd,GetData["ScriptName"])
                if statusOfTask:
                    GetData["Status"]=statusOfTask
                GetData["Output"]=resp
                if flag=="success":        
                    with open(DocPath+filePath, 'w') as fileP:
                        fileP.write(GetData["Output"])
                    GetData["filePath"]=filePath
    
            return render(request,"main.html",{'tagsList':GetData})
        else:
            form=Linux_DeleteLogicalVolume()
            option = request.GET.get('option',None)
            GetData={}
            GetData["headerMsg"]="Delete LogicalVolume"
            GetData["option"]=option
            GetData["tagName"]="deleteLogicalVolume"
            return render(request,"main.html",{'taskForm':form,'tagsList':GetData})
    except Exception as e:
        print(e)
        form=Linux_DeleteLogicalVolume()
        return render(request,"Automations.html",{'Linux_DeleteLogicalVolume':form,'data':{}})
def createVolumeGroup_Linux(request):
    try:
        print(" in createVolumeGroup_Linux method")
        GetData={}
        if request.method == 'POST':
            data=request.POST.dict()
            option = request.GET.get('option',None)            
            GetData["option"]=option
            print(data)
            if "csrfmiddlewaretoken" in data:
                    del data['csrfmiddlewaretoken']
            server=data["server"]
            #username=data["username"]
            #password=data["password"]
            volume_group_name=data["volume_group_name"]
            physical_volumes = data["physical_volumes"]
            physcal_extent_size=data["physcal_extent_size"]      
            executionType = data["Execution_method"]
            GetData["ScriptName"]="createVolumeGroup"
            GetData["Input"]=data
            print(executionType)
            
            if executionType=="ssh":
                cmd = '''ansible-playbook /etc/ansible/Linux.yml --extra-vars "server='''+server+''' 
                         volume_group_name='''+volume_group_name+''' physical_volumes='''+physical_volumes+''' physcal_extent_size='''+physcal_extent_size+''' " --tags  "createVolumeGroup" -vvvv'''
                resp,flag,filePath = runPlayBook_SSH(cmd,GetData["ScriptName"])
                GetData["Output"]=resp
                if flag=="success":        
                    with open(DocPath+filePath, 'w') as json_file:
                        json.dump(GetData, json_file)
                    GetData["filePath"]=filePath
                    
            elif executionType=="jenkins":
                finalString1 = '" -d "'.join("{!s}={!s}".format(key,val) for (key,val) in data.items())
                finalString = '"{}"'.format(finalString1)
                cmd='curl -d ' + finalString + ' -i -X POST http://admin:admin@172.22.110.191:8080/job/'+GetData["ScriptName"]+'/buildWithParameters -H "Jenkins-Crumb:4587c8c2d29e8453ba570654c5248554"'
                resp,flag,filePath,statusOfTask=runPlayBook_Jenkins(cmd,GetData["ScriptName"])
                if statusOfTask:
                    GetData["Status"]=statusOfTask
                GetData["Output"]=resp
                if flag=="success":        
                    with open(DocPath+filePath, 'w') as fileP:
                        fileP.write(GetData["Output"])
                    GetData["filePath"]=filePath
            
            return render(request,"main.html",{'tagsList':GetData})
        else:
            form=Linux_CreateVolumeGroup()
            option = request.GET.get('option',None)
            GetData={}
            GetData["headerMsg"]="Create VolumeGroup"
            GetData["option"]=option
            GetData["tagName"]="createVolumeGroup"
            return render(request,"main.html",{'taskForm':form,'tagsList':GetData})
    except Exception as e:
        print(e)
        form=Linux_CreateVolumeGroup()
        return render(request,"Automations.html",{'Linux_CreateVolumeGroup':form,'data':{}})
def deleteVolumeGroup_Linux(request):
    try:
        print(" in deleteVolumeGroup_Linux method")
        GetData={}
        if request.method == 'POST':
            data=request.POST.dict()
            option = request.GET.get('option',None)            
            GetData["option"]=option
            print(data)
            if "csrfmiddlewaretoken" in data:
                    del data['csrfmiddlewaretoken']
            server=data["server"]
            #username=data["username"]
            #password=data["password"]
            volume_group_name=data["volume_group_name"]
            executionType = data["Execution_method"]
            GetData["ScriptName"]="deleteVolumeGroup"
            GetData["Input"]=data
            print(executionType)
            
            if executionType=="ssh":
                cmd = '''ansible-playbook /etc/ansible/Linux.yml --extra-vars "server='''+server+''' 
                         volume_group_name='''+volume_group_name+''' " --tags  "'''+GetData["ScriptName"]+'''" -vvvv'''
                resp,flag,filePath = runPlayBook_SSH(cmd,GetData["ScriptName"])
                GetData["Output"]=resp
                if flag=="success":        
                    with open(DocPath+filePath, 'w') as json_file:
                        json.dump(GetData, json_file)
                    GetData["filePath"]=filePath
                    
            elif executionType=="jenkins":
                finalString1 = '" -d "'.join("{!s}={!s}".format(key,val) for (key,val) in data.items())
                finalString = '"{}"'.format(finalString1)
                cmd='curl -d ' + finalString + ' -i -X POST http://admin:admin@172.22.110.191:8080/job/'+GetData["ScriptName"]+'/buildWithParameters -H "Jenkins-Crumb:4587c8c2d29e8453ba570654c5248554"'
                resp,flag,filePath,statusOfTask=runPlayBook_Jenkins(cmd,GetData["ScriptName"])
                if statusOfTask:
                    GetData["Status"]=statusOfTask
                GetData["Output"]=resp
                if flag=="success":        
                    with open(DocPath+filePath, 'w') as fileP:
                        fileP.write(GetData["Output"])
                    GetData["filePath"]=filePath
                    
            return render(request,"main.html",{'tagsList':GetData})
        else:
            form=Linux_DeleteVolumeGroup()
            option = request.GET.get('option',None)
            GetData["headerMsg"]="Delete VolumeGroup"
            GetData["option"]=option
            GetData["tagName"]="deleteVolumeGroup"
            return render(request,"main.html",{'taskForm':form,'tagsList':GetData})
    except Exception as e:
        print(e)
        form=Linux_DeleteVolumeGroup()
        return render(request,"Automations.html",{'Linux_DeleteVolumeGroup':form,'data':{}})
    
def installFeatureWindows(request):
    try:
        print("in installFeatureWindows method")
        GetData={}
        if request.method == 'POST':
            data=request.POST.dict()
            option = request.GET.get('option',None)            
            GetData["option"]=option
            print(data)
            if "csrfmiddlewaretoken" in data:
                    del data['csrfmiddlewaretoken']
            server=data["server"]
            #sername=data["username"]
            #assword=data["password"]
            windows_feature_name=data["windows_feature_name"]
            executionType = data["Execution_method"]
            GetData["ScriptName"]="installFeature"
            GetData["Input"]=data
            print(executionType)
            ########################## Executing Playbook via SSH #######################
            if executionType=="ssh":
                cmd = '''ansible-playbook /etc/ansible/Windows.yml --extra-vars "server='''+server+''' 
                         windows_feature_name='''+windows_feature_name+''' " --tags  "'''+GetData["ScriptName"]+'''" -vvvv'''
                resp,flag,filePath = runPlayBook_SSH(cmd,GetData["ScriptName"])
                GetData["Output"]=resp
                if flag=="success":        
                    with open(DocPath+filePath, 'w') as json_file:
                        json.dump(GetData, json_file)
                    GetData["filePath"]=filePath
                    
            ########################## Executing Playbook via Jenkins ####################   
            elif executionType=="jenkins":
                finalString1 = '" -d "'.join("{!s}={!s}".format(key,val) for (key,val) in data.items())
                finalString = '"{}"'.format(finalString1)
                cmd='curl -d ' + finalString + ' -i -X POST http://admin:admin@172.22.110.191:8080/job/'+GetData["ScriptName"]+'/buildWithParameters -H "Jenkins-Crumb:4587c8c2d29e8453ba570654c5248554"'
                resp,flag,filePath,statusOfTask=runPlayBook_Jenkins(cmd,GetData["ScriptName"])
                if statusOfTask:
                    GetData["Status"]=statusOfTask
                GetData["Output"]=resp
                if flag=="success":        
                    with open(DocPath+filePath, 'w') as fileP:
                        fileP.write(GetData["Output"])
                    GetData["filePath"]=filePath
                
            return render(request,"main.html",{'tagsList':GetData})
        else:
            form=Windows_installFeature()
            option = request.GET.get('option',None)
            GetData["headerMsg"]="Install Feature"
            GetData["option"]=option
            GetData["tagName"]="installFeature"
            return render(request,"main.html",{'taskForm':form,'tagsList':GetData})
    except Exception as e:
        print(e)
        form=Windows_installFeature()
        return render(request,"Automations.html",{'installFeatureWindows':form,'data':{}})
    
def uninstallFeatureWindows(request):
    try:
        print("in uninstallFeatureWindows method")
        GetData={}
        if request.method == 'POST':
            data=request.POST.dict()
            option = request.GET.get('option',None)            
            GetData["option"]=option
            print(data)
            if "csrfmiddlewaretoken" in data:
                    del data['csrfmiddlewaretoken']
            server=data["server"]
            #username=data["username"]
            #password=data["password"]
            windows_feature_name=data["windows_feature_name"]
            executionType = data["Execution_method"]
            GetData["ScriptName"]="uninstallFeature"
            GetData["Input"]=data
            print(executionType)
            ########################## Executing Playbook via SSH #######################
            if executionType=="ssh":
                cmd = '''ansible-playbook /etc/ansible/Windows.yml --extra-vars "server='''+server+''' 
                         windows_feature_name='''+windows_feature_name+''' " --tags "'''+GetData["ScriptName"]+'''"  -vvvv'''
                resp,flag,filePath = runPlayBook_SSH(cmd,GetData["ScriptName"])
                GetData["Output"]=resp
                if flag=="success":        
                    with open(DocPath+filePath, 'w') as json_file:
                        json.dump(GetData, json_file)
                    GetData["filePath"]=filePath
                    
            ########################## Executing Playbook via Jenkins ####################   
            elif executionType=="jenkins":
                finalString1 = '" -d "'.join("{!s}={!s}".format(key,val) for (key,val) in data.items())
                finalString = '"{}"'.format(finalString1)
                cmd='curl -d ' + finalString + ' -i -X POST http://admin:admin@172.22.110.191:8080/job/'+GetData["ScriptName"]+'/buildWithParameters -H "Jenkins-Crumb:4587c8c2d29e8453ba570654c5248554"'
                resp,flag,filePath,statusOfTask=runPlayBook_Jenkins(cmd,GetData["ScriptName"])
                if statusOfTask:
                    GetData["Status"]=statusOfTask
                GetData["Output"]=resp
                if flag=="success":        
                    with open(DocPath+filePath, 'w') as fileP:
                        fileP.write(GetData["Output"])
                    GetData["filePath"]=filePath
                
            return render(request,"main.html",{'tagsList':GetData})
        else:
            form=Windows_uninstallFeature()
            option = request.GET.get('option',None)
            GetData["headerMsg"]="Uninstall Feature"
            GetData["option"]=option
            GetData["tagName"]="uninstallFeature"
            return render(request,"main.html",{'taskForm':form,'tagsList':GetData})
    except Exception as e:
        print(e)
        form=Windows_uninstallFeature()
        return render(request,"Automations.html",{'uninstallFeatureWindows':form,'data':{}})
    
def manageServiceWindows(request):
    try:
        print("in manageServiceWindows method")
        GetData={}
        if request.method == 'POST':
            data=request.POST.dict()
            option = request.GET.get('option',None)            
            GetData["option"]=option
            print(data)
            if "csrfmiddlewaretoken" in data:
                    del data['csrfmiddlewaretoken']
            server=data["server"]
            #username=data["username"]
            #password=data["password"]
            windows_service_name=data["windows_service_name"]
            windows_service_state=data["windows_service_state"]
            executionType = data["Execution_method"]
            GetData["ScriptName"]="manageService"
            GetData["Input"]=data
            print(executionType)
            ########################## Executing Playbook via SSH #######################
            if executionType=="ssh":
                cmd = '''ansible-playbook /etc/ansible/Windows.yml --extra-vars "server='''+server+''' 
                         windows_service_name='''+windows_service_name+''' windows_service_state='''+windows_service_state+'''"
                        --tags "'''+GetData["ScriptName"]+'''" -vvvv'''
                resp,flag,filePath = runPlayBook_SSH(cmd,GetData["ScriptName"])
                GetData["Output"]=resp
                if flag=="success":        
                    with open(DocPath+filePath, 'w') as json_file:
                        json.dump(GetData, json_file)
                    GetData["filePath"]=filePath
            ########################## Executing Playbook via Jenkins ####################   
            elif executionType=="jenkins":
                finalString1 = '" -d "'.join("{!s}={!s}".format(key,val) for (key,val) in data.items())
                finalString = '"{}"'.format(finalString1)
                cmd='curl -d ' + finalString + ' -i -X POST http://admin:admin@172.22.110.191:8080/job/'+GetData["ScriptName"]+'/buildWithParameters -H "Jenkins-Crumb:4587c8c2d29e8453ba570654c5248554"'
                resp,flag,filePath,statusOfTask=runPlayBook_Jenkins(cmd,GetData["ScriptName"])
                if statusOfTask:
                    GetData["Status"]=statusOfTask
                GetData["Output"]=resp
                if flag=="success":        
                    with open(DocPath+filePath, 'w') as fileP:
                        fileP.write(GetData["Output"])
                    GetData["filePath"]=filePath
            print(GetData)  
            return render(request,"main.html",{'tagsList':GetData})
        else:
            form=Windows_ManageService()
            option = request.GET.get('option',None)
            GetData["headerMsg"]="Manage Service"
            GetData["option"]=option
            GetData["tagName"]="manageService"
            return render(request,"main.html",{'taskForm':form,'tagsList':GetData})
    except Exception as e:
        print(e)
        form=Windows_ManageService()
        return render(request,"Automations.html",{'manageService':form,'data':{}})
   

#########################

def manageFortigate(request):
    
    try:
        print("in manageFortigate method")
        GetData={}
        if request.method == 'POST':
            data=request.POST.dict()
            option = request.GET.get('option',None)            
            GetData["option"]=option
            print(data)
            if "csrfmiddlewaretoken" in data:
                    del data['csrfmiddlewaretoken']
            state=data["state"]
            address_name=data["address_name"]
            address_type=data["address_type"]
            ip_and_cidr=data["ip_and_cidr"]
            executionType = data["Execution_method"]
            GetData["ScriptName"]="manage_Fortigate"
            GetData["Input"]=data
            print(executionType)
            ########################## Executing Playbook via SSH #######################
            if executionType=="ssh":
                cmd = '''ansible-playbook /etc/ansible/Network.yml --extra-vars "state='''+state+''' 
                         address_name='''+address_name+''' address_type='''+address_type+''' ip_and_cidr='''+ip_and_cidr+'''"
                        --tags "'''+GetData["ScriptName"]+'''" -vvvv'''
                resp,flag,filePath = runPlayBook_SSH(cmd,GetData["ScriptName"])
                GetData["Output"]=resp
                if flag=="success":        
                    with open(DocPath+filePath, 'w') as json_file:
                        json.dump(GetData, json_file)
                    GetData["filePath"]=filePath
            ########################## Executing Playbook via Jenkins ####################   
            elif executionType=="jenkins":
                finalString1 = '" -d "'.join("{!s}={!s}".format(key,val) for (key,val) in data.items())
                finalString = '"{}"'.format(finalString1)
                cmd='curl -d ' + finalString + ' -i -X POST http://admin:admin@172.22.110.191:8080/job/'+GetData["ScriptName"]+'/buildWithParameters -H "Jenkins-Crumb:4587c8c2d29e8453ba570654c5248554"'
                resp,flag,filePath,statusOfTask=runPlayBook_Jenkins(cmd,GetData["ScriptName"])
                if statusOfTask:
                    GetData["Status"]=statusOfTask
                GetData["Output"]=resp
                if flag=="success":        
                    with open(DocPath+filePath, 'w') as fileP:
                        fileP.write(GetData["Output"])
                    GetData["filePath"]=filePath
            
            print(GetData)  
            return render(request,"main.html",{'tagsList':GetData})
        else:
            form=Manage_Fortigate()
            GetData={}
            GetData["headerMsg"]="Manage Fortigate"
            return render(request,"Automations.html",{'manageFortigate':form,'data':GetData})
    except Exception as e:
        print(e)
        form=Manage_Fortigate()
        return render(request,"Automations.html",{'manageFortigate':form,'data':{}})
    
    
def runPlayBook_SSH(cmd,tag):
    try:
        print("\n\n ************ We are executing below command via SSH ************* \n\n")
        print(cmd)
        ssh=paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect("172.22.110.192",22,"root","Pass@1234")
        stdin,stdout,stderr=ssh.exec_command(cmd)
        outlines=stdout.readlines()
        print(stdout.readlines())
        print(stderr.readlines())
        resp ='\n'.join(outlines)
        print("\n ================== Results for the above cmd ================ \n")
        print(resp)
        flag = "success"
        DT = datetime.datetime.now()
        part1=DT.strftime("%Y%m%d")
        part2=DT.strftime("%H%M%S")
        resultSaveAt=tag+"_"+part1+"_"+part2+".txt"
        print(resultSaveAt)
    except Exception as e:
        print("\n Exception occuered in runPlayBook_SSH method:: "+e)
        resp="Error Occured , Try again"
        flag="fail"
        resultSaveAt=""
    return resp,flag,resultSaveAt

def runPlayBook_Jenkins(cmd,tag):
    try:
        print("\n\n *********** We are executing below command via Jenkins ************ \n\n")
        print(cmd)
        statusOfTask=""
        ssh=paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect("172.22.110.191",22,"root","Pass@1234")
        stdin,stdout,stderr=ssh.exec_command(cmd)
        cmd1='curl http://admin:admin@172.22.110.191:8080/job/'+tag+'/lastBuild/consoleText'
        time.sleep(60)
        stdin,stdout,stderr=ssh.exec_command(cmd1)
        outlines=stdout.readlines()
        for i in outlines:
            if "Finished:" in i:
                statusOfTask=i.split("Finished:")
                print(type(statusOfTask))
                statusOfTask=statusOfTask[1]
                print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
        resp ='\n'.join(outlines)
        print("\n ================== Results for the above cmd ================ \n")
        flag = "success"
        DT = datetime.datetime.now()
        part1=DT.strftime("%Y%m%d")
        part2=DT.strftime("%H%M%S")
        resultSaveAt=tag+"_"+part1+"_"+part2+".txt"
        print(resultSaveAt)
    except Exception as e:
        print("\n Exception occuered in runPlayBook_SSH method:: "+e)
        resp="Error Occured , Try again"
        flag="fail"
        resultSaveAt=""
    return resp,flag,resultSaveAt,statusOfTask
def downloadResults(request):
    
    data = request.GET.dict()
    with open("/root/AutomationWebApp/App1/static/Documents/"+data['filePath'], 'r') as fileP:
        content=fileP.read()
    #content=file("/AutomationStuff/App1/static/Documents/"+data['filePath']).read()
    print("********** printing results before downloading **************")
    print(data)

    response = HttpResponse(content,content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename="'+data['filePath']+'"'
    
    print(response)
    print("-------------------------------------------------------------")
    response['X-Frame-Options']=" "
    return response
    

