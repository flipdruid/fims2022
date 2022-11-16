from nturl2path import url2pathname
from this import d
from django.shortcuts import render, get_object_or_404, reverse
from django.http import HttpResponse, HttpResponseRedirect, Http404, JsonResponse, response
from django.core.paginator import Paginator
from django.db.models import Q
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.decorators import login_required, permission_required
# from mmaptsp2.models import Mmap, Beneficiary, Branchcode, Sccn
# from mmpaptsp2.models import Client, Clientaccountcode
from .models import Aws, Awsaccounts
from datetime import datetime, timedelta
import boto3
import pyperclip

@login_required(login_url= '/users/login')
def index(request):
    awsUbuntuInfo = {}
    awsWindowsInfo = {}
    user                =       request.user
    awsServers          =       Aws.objects.all()

    awsUbuntus          =       awsServers.filter(serverType='Ubuntu')
    awsWindows          =       awsServers.filter(serverType='Windows')

    disablestartRestartButton   =   "disabled"   
    startRestart                =   "Start"
    # Start for AWS Ubuntu Servers
    for awsUbuntu  in awsUbuntus:
        ubuntuSession = boto3.Session( 
                      aws_access_key_id=awsUbuntu.accessKeyID, 
                      aws_secret_access_key=awsUbuntu.secretAccessKey, 
                      region_name=awsUbuntu.region
                      )
        ubuntu_client  =  ubuntuSession.client('ec2') 
        
        ubuntuResponse      =   ubuntu_client.describe_instance_status(
            InstanceIds     =   [awsUbuntu.instanceID],
            IncludeAllInstances =   True
        )

       
        ubuntuInstanceStatus          = ubuntuResponse['InstanceStatuses'][0]['InstanceStatus']['Status']
        ubuntuSystemStatus            = ubuntuResponse['InstanceStatuses'][0]['SystemStatus']['Status']
        ubuntuInstanceStates          = ubuntuResponse['InstanceStatuses'][0]['InstanceState']['Name']

       

        if str(ubuntuInstanceStatus) == 'ok' and str(ubuntuSystemStatus) == 'ok' and str(ubuntuInstanceStates )=='running':
            # disableStopButton    =   ""
            # serverReady                 =   "Ready"
            startRestart                =   "Restart"
            disablestartRestartButton   =   ""
           

        elif str(ubuntuInstanceStatus) != 'ok' and str(ubuntuSystemStatus) != 'ok' and str(ubuntuInstanceStates )=='running':
            disablestartRestartButton   =   "disabled"   
                
            startRestart                 =   "Restart"

        
        elif str(ubuntuInstanceStatus) != 'ok' and str(ubuntuSystemStatus) != 'ok' and str(ubuntuInstanceStates )=='stopped':
            startRestart                 =   "Start"
            disablestartRestartButton    =   ""
            

        # for RDP Button enable/disable


            
        # else:
        #     # disableStopButton    =   "disabled"
        #     serverReady          =   "Not Ready"
        #     startReboot          =   "Start"       

        
        if str(ubuntuInstanceStates )=='running':
            disableStopButton    =   ""
        else:
            disableStopButton    =   "disabled"       

        awsUbuntuInfo[awsUbuntu.id] = { 
                                'database'                  : awsUbuntu.database,
                                'instanceName'              : awsUbuntu.instanceName,
                                'ubuntuInstanceStatus'      : ubuntuInstanceStatus, 
                                'ubuntuSystemStatus'        : ubuntuSystemStatus,
                                'disableStopButton'         : disableStopButton,
                                # 'serverReady'           : serverReady,
                                'disablestartRestartButton' : disablestartRestartButton,
                                'startRestart'              : startRestart,
                                'ubuntuInstanceStates'      : ubuntuInstanceStates,   
                                         
                                }
        ubuntuSession          =   None
        ubuntu_client          =   None
        ubuntuResponse         =   None

    # End for AWS Ubuntu Servers

    # Start for AWS Windows Servers

    for awsWindow  in awsWindows:
        windowsSession = boto3.Session( 
                      aws_access_key_id=awsWindow.accessKeyID, 
                      aws_secret_access_key=awsWindow.secretAccessKey, 
                      region_name=awsWindow.region
                      )
        windows_client  =  windowsSession.client('ec2') 
        
        windowResponse      =   windows_client.describe_instance_status(
            InstanceIds     =   [awsWindow.instanceID],
            IncludeAllInstances =   True
        )

       
        windowInstanceStatus          = windowResponse['InstanceStatuses'][0]['InstanceStatus']['Status']
        windowSystemStatus            = windowResponse['InstanceStatuses'][0]['SystemStatus']['Status']
        windowInstanceStates          = windowResponse['InstanceStatuses'][0]['InstanceState']['Name']

        disableRDPButton             =   "disabled"

        if str(windowInstanceStatus) == 'ok' and str(windowSystemStatus) == 'ok' and str(windowInstanceStates )=='running':
            # disableStopButton    =   ""
            # serverReady                 =   "Ready"
            startRestart                =   "Restart"
            disablestartRestartButton    =   ""
            disableRDPButton            =   ""  

        elif str(windowInstanceStatus) != 'ok' and str(windowSystemStatus) != 'ok' and str(windowInstanceStates )=='running':
            disablestartRestartButton    =   "disabled"            
            startRestart                 =   "Restart"
            disableRDPButton             =   "disabled"
        
        elif str(windowInstanceStatus) != 'ok' and str(windowSystemStatus) != 'ok' and str(windowInstanceStates )=='stopped':
            startRestart                 =   "Start"
            disablestartRestartButton    =   ""
            disableRDPButton             =   "disabled"

        
    
        # else:
        #     # disableStopButton    =   "disabled"
        #     serverReady          =   "Not Ready"
        #     startReboot          =   "Start"       

        
        if str(windowInstanceStates )=='running':
            
            disableStopButton    =   ""
        else:
            
            disableStopButton    =   "disabled"


        awsWindowsInfo[awsWindow.id] = { 
                                'database'                      : awsWindow.database,
                                'instanceName'                  : awsWindow.instanceName,
                                'rdpPass'                       : awsWindow.rdpPass,
                                'windowInstanceStatus'          : windowInstanceStatus, 
                                'windowSystemStatus'            : windowSystemStatus,
                                'disableStopButton'             : disableStopButton,
                                'disablestartRestartButton'     : disablestartRestartButton,
                                # 'serverReady'           : serverReady,
                                'startRestart'                  : startRestart,
                                'windowInstanceStates'          : windowInstanceStates,
                                'disableRDPButton'              : disableRDPButton   
                                  
                                }
        windowsSession      =   None
        windows_client      =   None
        windowResponse      =   None
    
    # End for AWS Windows Servers

    context     =   {
        # 'awsUbuntus' : awsUbuntus,
        # 'awsWindows': awsWindows,
        # 'awsURL': awsURL,
        'awsUbuntuInfo' :awsUbuntuInfo,
        'awsWindowsInfo': awsWindowsInfo
        }


    return render (request, 'aws/index.html', context)


@login_required(login_url= '/users/login')
def addaccount(request):
    user                    =         request.user
    awsaccounts             =         Awsaccounts.objects.all()

    return render (request, 'aws/addaccount.html', {'awsaccounts' : awsaccounts})


@login_required(login_url= '/users/login')
def processaddaccount(request):
    user                    = request.user

    getAccountName          = request.POST.get('accountName')
    awsaccount              = Awsaccounts.objects.get(accountName=getAccountName)
    accountName             = awsaccount.accountName
    accountID               = awsaccount.accountID
    accountUser             = awsaccount.accountUser
    accessKeyID             = awsaccount.accessKeyID
    secretAccessKey         = awsaccount.secretAccessKey
    region                  = awsaccount.region
    instanceName            = request.POST.get('instanceName')
    instanceID              = request.POST.get('instanceID')
    serverIP                = request.POST.get('serverIP')
    database                = request.POST.get('database')
    serverType              = request.POST.get('serverType')
    setupDate               = datetime.now().date()
    # return render ('')

    newAWSAccount = Aws.objects.create(accountName=accountName, 
        accountID=accountID,
        accountUser=accountUser,
        accessKeyID=accessKeyID,
        secretAccessKey=secretAccessKey,
        region=region,
        instanceName=instanceName,
        instanceID=instanceID,
        serverIP=serverIP,
        database=database,
        serverType=serverType,
        setupDate=setupDate)

    newAWSAccount.save()

    # return render (request, 'aws/awsservers.html', {})
    return HttpResponseRedirect('/aws', {})


@login_required(login_url= '/users/login')
def awsaccounts(request):
    user                =         request.user
    awsaccounts         =         Awsaccounts.objects.all()
    return render (request, 'aws/awsaccounts.html',  {'awsaccounts': awsaccounts})

    
@login_required(login_url= '/users/login')
def startreserver(request,serverid):
    user                =         request.user
    currentserver   =   Aws.objects.get(pk=serverid)

    ec2_client = boto3.client('ec2', 
                      aws_access_key_id=currentserver.accessKeyID, 
                      aws_secret_access_key=currentserver.secretAccessKey, 
                      region_name=currentserver.region
                      )

    ec2describe_instances   =   ec2_client.describe_instances(InstanceIds=[currentserver.instanceID])

    ec2State            =   ec2describe_instances['Reservations'][0]['Instances'][0]['State']['Name']

    if str(ec2State)=='running':
        ec2_client.reboot_instances(InstanceIds=[currentserver.instanceID])
    
    elif str(ec2State)=='stopped':
        ec2_client.start_instances(InstanceIds=[currentserver.instanceID])


    

    # ec2_session = boto3.Session(aws_access_key_id =currentserver.accessKeyID, 
    #                     aws_secret_access_key=currentserver.secretAccessKey, 
    #                     region_name=currentserver.region
    #                   )
    # ec2_client = ec2_session.client('ec2')

    # respon  =   ec2_client.describe_instance_status(
    #     InstanceIds=[currentserver.instanceID],
    #     IncludeAllInstances=True
    # )

    # instanceStatus          =   respon['InstanceStatuses'][0]['InstanceStatus']['Status']
    # systemStatus            =   respon['InstanceStatuses'][0]['SystemStatus']['Status']
    # instanceStates          =   respon['InstanceStatuses'][0]['InstanceState']['Name']

    # ec2_session = None
    # ec2_client  = None
    # respon      = None


    # ec2_client.start_instances(InstanceIds=[currentserver.instanceID])

    # if str(instanceStatus) == 'ok' and str(systemStatus) == 'ok':
    #     # ec2_instance = boto3.client('ec2', 
    #     #               aws_access_key_id=currentserver.accessKeyID, 
    #     #               aws_secret_access_key=currentserver.secretAccessKey, 
    #     #               region_name=currentserver.region
    #     #               )
    #     ec2_client.reboot_instances(InstanceIds=[currentserver.instanceID])

    
    # if str(instanceStates )=='Stopped':
    #     # ec2_instance = boto3.client('ec2', 
    #     #               aws_access_key_id=currentserver.accessKeyID, 
    #     #               aws_secret_access_key=currentserver.secretAccessKey, 
    #     #               region_name=currentserver.region
    #     #               )
    #     ec2_client.start_instances(InstanceIds=[currentserver.instanceID])



    return HttpResponseRedirect('/aws', {})
 

@login_required(login_url= '/users/login')
def stopserver(request,serverid):

    currentserver   =   Aws.objects.get(pk=serverid)

    ec2_client = boto3.client('ec2', 
                      aws_access_key_id=currentserver.accessKeyID, 
                      aws_secret_access_key=currentserver.secretAccessKey, 
                      region_name=currentserver.region
                      )

    #Get instance State - START

    ec2_session = boto3.Session(aws_access_key_id =currentserver.accessKeyID, 
                        aws_secret_access_key=currentserver.secretAccessKey, 
                        region_name=currentserver.region
                      )
    ec2_sessionClient = ec2_session.client('ec2')

    getInstanceState  =   ec2_sessionClient.describe_instance_status(
    InstanceIds=[currentserver.instanceID],
    IncludeAllInstances=True)
    instanceState    =   getInstanceState['InstanceStatuses'][0]['InstanceState']['Name']
    #Get instance State - END
    
    if instanceState=='running':
        ec2_client.stop_instances(InstanceIds=[currentserver.instanceID])

    return HttpResponseRedirect('/aws', {})


@login_required(login_url= '/users/login')
def instancerdp(request, instanceid):
    
    # rdpStringLeft = "auto connect:i:1full address:s:"
    # rdpStringRight= "username:s:Administrator"

    autoCon = "auto connect:i:1\n"
    

    currentserver   =   Aws.objects.get(pk=instanceid)

    ec2_client = boto3.client('ec2', 
                      aws_access_key_id=currentserver.accessKeyID, 
                      aws_secret_access_key=currentserver.secretAccessKey, 
                      region_name=currentserver.region
                      )

    ec2describe_instances   =   ec2_client.describe_instances(InstanceIds=[currentserver.instanceID])

    instancePublicDNSName = ec2describe_instances['Reservations'][0]['Instances'][0]['NetworkInterfaces'][0]['Association']['PublicDnsName']


    createRDP = HttpResponse(content_type="text/plain")
    createRDP['Content-Disposition'] = 'attachment; filename=FCCT-ec2-windows-' + currentserver.instanceName + "-" + str(datetime.now())+'.rdp'  

    # fullAddress = "full address:s:ec2-3-1-217-100.ap-southeast-1.compute.amazonaws.com"
    fullAddress = "full address:s:"+ str(instancePublicDNSName)+"\n"
    userName = 'username:s:Administrator'
    

    # createRDP.writelines(rdpStringLeft + str(instancePublicDNSName) + rdpStringRight)

    createRDP.writelines(autoCon + fullAddress + userName)
    #pyperclip.copy(currentserver.rdpPass)

    return createRDP


# Ubuntu Servers Here -> Start
@login_required(login_url= '/users/login')
def ubuntuservers(request):
    UbuntuServersCebu   = {}
    UbuntuServersNegros = {}    
    user                =       request.user   
    awsUbuntus          =       Aws.objects.filter(serverType='Ubuntu')

    
    # UbuntuServersCebu - START
    awsUbuntusCebu      =   awsUbuntus.filter(area='Cebu')
    for awsUbuntuCebu  in awsUbuntusCebu:
        ubuntuSession = boto3.Session( 
                      aws_access_key_id=awsUbuntuCebu.accessKeyID, 
                      aws_secret_access_key=awsUbuntuCebu.secretAccessKey, 
                      region_name=awsUbuntuCebu.region
                      )
        ubuntu_client  =  ubuntuSession.client('ec2') 
        
        ubuntuResponse      =   ubuntu_client.describe_instance_status(
            InstanceIds     =   [awsUbuntuCebu.instanceID],
            IncludeAllInstances =   True
        )

       
        ubuntuInstanceStatus          = ubuntuResponse['InstanceStatuses'][0]['InstanceStatus']['Status']
        ubuntuSystemStatus            = ubuntuResponse['InstanceStatuses'][0]['SystemStatus']['Status']
        ubuntuInstanceStates          = ubuntuResponse['InstanceStatuses'][0]['InstanceState']['Name']

       
        disablestartRestartButton   =   "disabled"   
        startRestart                =   "Start"  
        if str(ubuntuInstanceStatus) == 'ok' and str(ubuntuSystemStatus) == 'ok' and str(ubuntuInstanceStates )=='running':
            startRestart                =   "Restart"
            disablestartRestartButton   =   ""
           

        elif str(ubuntuInstanceStatus) != 'ok' and str(ubuntuSystemStatus) != 'ok' and str(ubuntuInstanceStates )=='running':
            disablestartRestartButton   =   "disabled"   
                
            startRestart                 =   "Restart"

        
        elif str(ubuntuInstanceStatus) != 'ok' and str(ubuntuSystemStatus) != 'ok' and str(ubuntuInstanceStates )=='stopped':
            startRestart                 =   "Start"
            disablestartRestartButton    =   ""
               

        
        if str(ubuntuInstanceStates )=='running':
            disableStopButton    =   ""
        else:
            disableStopButton    =   "disabled"       

        UbuntuServersCebu[awsUbuntuCebu.id] = { 
                                'database'                  : awsUbuntuCebu.database,
                                'instanceName'              : awsUbuntuCebu.instanceName,
                                'ubuntuInstanceStatus'      : ubuntuInstanceStatus, 
                                'ubuntuSystemStatus'        : ubuntuSystemStatus,
                                'disableStopButton'         : disableStopButton,
                                'disablestartRestartButton' : disablestartRestartButton,
                                'startRestart'              : startRestart,
                                'ubuntuInstanceStates'      : ubuntuInstanceStates,   
                                         
                                }
        ubuntuSession          =   None
        ubuntu_client          =   None
        ubuntuResponse         =   None

    # UbuntuServersCebu - End

    # awsUbuntusNegros - START
    awsUbuntusNegros    =   awsUbuntus.filter(area='Negros')
    for awsUbuntuNegros  in awsUbuntusNegros:
            ubuntuSession = boto3.Session( 
                        aws_access_key_id=awsUbuntuNegros.accessKeyID, 
                        aws_secret_access_key=awsUbuntuNegros.secretAccessKey, 
                        region_name=awsUbuntuNegros.region
                        )
            ubuntu_client  =  ubuntuSession.client('ec2') 
            
            ubuntuResponse      =   ubuntu_client.describe_instance_status(
                InstanceIds     =   [awsUbuntuNegros.instanceID],
                IncludeAllInstances =   True
            )

        
            ubuntuInstanceStatus          = ubuntuResponse['InstanceStatuses'][0]['InstanceStatus']['Status']
            ubuntuSystemStatus            = ubuntuResponse['InstanceStatuses'][0]['SystemStatus']['Status']
            ubuntuInstanceStates          = ubuntuResponse['InstanceStatuses'][0]['InstanceState']['Name']

        

            if str(ubuntuInstanceStatus) == 'ok' and str(ubuntuSystemStatus) == 'ok' and str(ubuntuInstanceStates )=='running':
                startRestart                =   "Restart"
                disablestartRestartButton   =   ""
            

            elif str(ubuntuInstanceStatus) != 'ok' and str(ubuntuSystemStatus) != 'ok' and str(ubuntuInstanceStates )=='running':
                disablestartRestartButton   =   "disabled"   
                startRestart                 =   "Restart"

            
            elif str(ubuntuInstanceStatus) != 'ok' and str(ubuntuSystemStatus) != 'ok' and str(ubuntuInstanceStates )=='stopped':
                startRestart                 =   "Start"
                disablestartRestartButton    =   ""
                

            
            if str(ubuntuInstanceStates )=='running':
                disableStopButton    =   ""
            else:
                disableStopButton    =   "disabled"       

            UbuntuServersNegros[awsUbuntuNegros.id] = { 
                                    'database'                  : awsUbuntuNegros.database,
                                    'instanceName'              : awsUbuntuNegros.instanceName,
                                    'ubuntuInstanceStatus'      : ubuntuInstanceStatus, 
                                    'ubuntuSystemStatus'        : ubuntuSystemStatus,
                                    'disableStopButton'         : disableStopButton,
                                    'disablestartRestartButton' : disablestartRestartButton,
                                    'startRestart'              : startRestart,
                                    'ubuntuInstanceStates'      : ubuntuInstanceStates,   
                                            
                                    }
            ubuntuSession          =   None
            ubuntu_client          =   None
            ubuntuResponse         =   None
    
    # awsUbuntusNegros - START




    context     =   {        
        'UbuntuServersCebu'     :   UbuntuServersCebu,  
        'UbuntuServersNegros'   :   UbuntuServersNegros   
    }


    return render (request, 'aws/ubuntuservers.html', context)

@login_required(login_url= '/users/login')
def startreubuntuservers(request,serverid):
    user                =         request.user
    currentserver   =   Aws.objects.get(pk=serverid)

    ec2_client = boto3.client('ec2', 
                      aws_access_key_id=currentserver.accessKeyID, 
                      aws_secret_access_key=currentserver.secretAccessKey, 
                      region_name=currentserver.region
                      )

    ec2describe_instances   =   ec2_client.describe_instances(InstanceIds=[currentserver.instanceID])

    ec2State            =   ec2describe_instances['Reservations'][0]['Instances'][0]['State']['Name']

    if str(ec2State)=='running':
        ec2_client.reboot_instances(InstanceIds=[currentserver.instanceID])
    
    elif str(ec2State)=='stopped':
        ec2_client.start_instances(InstanceIds=[currentserver.instanceID]) 



    return HttpResponseRedirect('/aws/ubuntuservers/', {})


@login_required(login_url= '/users/login')
def stopubuntuservers(request,serverid):
    currentserver   =   Aws.objects.get(pk=serverid)

    ec2_client = boto3.client('ec2', 
                      aws_access_key_id=currentserver.accessKeyID, 
                      aws_secret_access_key=currentserver.secretAccessKey, 
                      region_name=currentserver.region
                      )

    #Get instance State - START

    ec2_session = boto3.Session(aws_access_key_id =currentserver.accessKeyID, 
                        aws_secret_access_key=currentserver.secretAccessKey, 
                        region_name=currentserver.region
                      )
    ec2_sessionClient = ec2_session.client('ec2')

    getInstanceState  =   ec2_sessionClient.describe_instance_status(
    InstanceIds=[currentserver.instanceID],
    IncludeAllInstances=True)
    instanceState    =   getInstanceState['InstanceStatuses'][0]['InstanceState']['Name']
    #Get instance State - END
    
    if instanceState=='running':
        ec2_client.stop_instances(InstanceIds=[currentserver.instanceID])

    return HttpResponseRedirect('/aws/ubuntuservers/', {})

# Ubuntu Servers Here -> End


# Windows Servers Here -> START
@login_required(login_url= '/users/login')
def windowsservers(request):
    windowsServers   = {}  
    
    user                =       request.user    

    awsWindows          =       Aws.objects.filter(serverType='Windows')

    
    
    

    disablestartRestartButton   =   "disabled"       
    
    for awsWindow  in awsWindows:
        windowsSession = boto3.Session( 
                      aws_access_key_id=awsWindow.accessKeyID, 
                      aws_secret_access_key=awsWindow.secretAccessKey, 
                      region_name=awsWindow.region
                      )
        windows_client  =  windowsSession.client('ec2') 
        
        ubuntuResponse      =   windows_client.describe_instance_status(
            InstanceIds     =   [awsWindow.instanceID],
            IncludeAllInstances =   True
        )

       
        windowsInstanceStatus          = ubuntuResponse['InstanceStatuses'][0]['InstanceStatus']['Status']
        windowsSystemStatus            = ubuntuResponse['InstanceStatuses'][0]['SystemStatus']['Status']
        windowsInstanceStates          = ubuntuResponse['InstanceStatuses'][0]['InstanceState']['Name']

       
        disablestartRestartButton    =   "disabled"
        disableRDPButton             =   "disabled"
        startRestart                 =   "disabled"
        if str(windowsInstanceStatus) == 'ok' and str(windowsSystemStatus) == 'ok' and str(windowsInstanceStates )=='running':
            startRestart                =   "Restart"
            disablestartRestartButton   =   ""
            disableRDPButton             =   ""
           

        elif str(windowsInstanceStatus) != 'ok' and str(windowsSystemStatus) != 'ok' and str(windowsInstanceStates )=='running':
            disablestartRestartButton   =   "disabled"                   
            startRestart                 =   "Restart"
            disableRDPButton             =   "disabled"

        
        elif str(windowsInstanceStatus) != 'ok' and str(windowsSystemStatus) != 'ok' and str(windowsInstanceStates )=='stopped':
            startRestart                 =   "Start"
            disablestartRestartButton    =   ""
            disableRDPButton             =   "disabled"
               

        
        if str(windowsInstanceStates )=='running':
            disableStopButton    =   ""
        else:
            disableStopButton    =   "disabled"       

        windowsServers[awsWindow.id] = { 
                                'database'                  : awsWindow.database,
                                'instanceName'              : awsWindow.instanceName,
                                'rdpPass'                   : awsWindow.rdpPass,
                                'windowsInstanceStatus'     : windowsInstanceStatus, 
                                'windowsSystemStatus'       : windowsSystemStatus,
                                'disableStopButton'         : disableStopButton,
                                'disablestartRestartButton' : disablestartRestartButton,
                                'startRestart'              : startRestart,
                                'windowsInstanceStates'     : windowsInstanceStates,
                                'disableRDPButton'          : disableRDPButton  
                                         
                                }
        windowsSession          =   None
        windows_client          =   None
        ubuntuResponse          =   None

    



    context     =   {        
        'windowsServers'     :   windowsServers,  
    }


    return render (request, 'aws/windowsservers.html', context)


@login_required(login_url= '/users/login')
def startrewindowsservers(request,serverid):
    user                =         request.user
    currentserver   =   Aws.objects.get(pk=serverid)

    ec2_client = boto3.client('ec2', 
                      aws_access_key_id=currentserver.accessKeyID, 
                      aws_secret_access_key=currentserver.secretAccessKey, 
                      region_name=currentserver.region
                      )

    ec2describe_instances   =   ec2_client.describe_instances(InstanceIds=[currentserver.instanceID])

    ec2State            =   ec2describe_instances['Reservations'][0]['Instances'][0]['State']['Name']

    if str(ec2State)=='running':
        ec2_client.reboot_instances(InstanceIds=[currentserver.instanceID])
    
    elif str(ec2State)=='stopped':
        ec2_client.start_instances(InstanceIds=[currentserver.instanceID]) 


    return HttpResponseRedirect('/aws/windowsservers/', {})


@login_required(login_url= '/users/login')
def stopwindowsservers(request,serverid):
    
    currentserver   =   Aws.objects.get(pk=serverid)

    ec2_client = boto3.client('ec2', 
                      aws_access_key_id=currentserver.accessKeyID, 
                      aws_secret_access_key=currentserver.secretAccessKey, 
                      region_name=currentserver.region
                      )

    #Get instance State - START

    ec2_session = boto3.Session(aws_access_key_id =currentserver.accessKeyID, 
                        aws_secret_access_key=currentserver.secretAccessKey, 
                        region_name=currentserver.region
                      )
    ec2_sessionClient = ec2_session.client('ec2')

    getInstanceState  =   ec2_sessionClient.describe_instance_status(
    InstanceIds=[currentserver.instanceID],
    IncludeAllInstances=True)
    instanceState    =   getInstanceState['InstanceStatuses'][0]['InstanceState']['Name']
    #Get instance State - END
    
    if instanceState=='running':
        ec2_client.stop_instances(InstanceIds=[currentserver.instanceID])

    return HttpResponseRedirect('/aws/windowsservers/', {})

# Windows Servers Here -> END


@login_required(login_url= '/users/login')
def startareaservers(request,area,action):
    urlLink =   '/aws/ubuntuservers/'
    areaSelected = area
    actionSelected = action

    if areaSelected == "Cebu":
        ubuntus  =   Aws.objects.filter(area=areaSelected)
        if actionSelected=="Start":
            for ubuntu in ubuntus:
                ec2_client = boto3.client('ec2', 
                      aws_access_key_id=ubuntu.accessKeyID, 
                      aws_secret_access_key=ubuntu.secretAccessKey, 
                      region_name=ubuntu.region
                      )
                
                ec2describe_instances   =   ec2_client.describe_instances(InstanceIds=[ubuntu.instanceID])
                ec2State                =   ec2describe_instances['Reservations'][0]['Instances'][0]['State']['Name']
                if str(ec2State)=='stopped':
                    ec2_client.start_instances(InstanceIds=[ubuntu.instanceID])

        if actionSelected=="Stop":
            for ubuntu in ubuntus:
                ec2_client = boto3.client('ec2', 
                      aws_access_key_id=ubuntu.accessKeyID, 
                      aws_secret_access_key=ubuntu.secretAccessKey, 
                      region_name=ubuntu.region
                      )
                
                ec2describe_instances   =   ec2_client.describe_instances(InstanceIds=[ubuntu.instanceID])
                ec2State                =   ec2describe_instances['Reservations'][0]['Instances'][0]['State']['Name']                
                if str(ec2State)=='running':
                    ec2_client.stop_instances(InstanceIds=[ubuntu.instanceID])
    
    elif areaSelected == "Negros":
        ubuntus  =   Aws.objects.filter(area=areaSelected)
        if actionSelected=="Start":
            for ubuntu in ubuntus:
                ec2_client = boto3.client('ec2', 
                      aws_access_key_id=ubuntu.accessKeyID, 
                      aws_secret_access_key=ubuntu.secretAccessKey, 
                      region_name=ubuntu.region
                      )
                
                ec2describe_instances   =   ec2_client.describe_instances(InstanceIds=[ubuntu.instanceID])
                ec2State                =   ec2describe_instances['Reservations'][0]['Instances'][0]['State']['Name']
                if str(ec2State)=='stopped':
                    ec2_client.start_instances(InstanceIds=[ubuntu.instanceID])

        if actionSelected=="Stop":
            for ubuntu in ubuntus:
                ec2_client = boto3.client('ec2', 
                      aws_access_key_id=ubuntu.accessKeyID, 
                      aws_secret_access_key=ubuntu.secretAccessKey, 
                      region_name=ubuntu.region
                      )
                
                ec2describe_instances   =   ec2_client.describe_instances(InstanceIds=[ubuntu.instanceID])
                ec2State                =   ec2describe_instances['Reservations'][0]['Instances'][0]['State']['Name']
                if str(ec2State)=='running':
                    ec2_client.stop_instances(InstanceIds=[ubuntu.instanceID])

    elif areaSelected == "AllUbuntu":
        urlLink = "/aws/"
        ubuntus  =   Aws.objects.filter(serverType='Ubuntu')
        if actionSelected=="Start":
            for ubuntu in ubuntus:
                ec2_client = boto3.client('ec2', 
                      aws_access_key_id=ubuntu.accessKeyID, 
                      aws_secret_access_key=ubuntu.secretAccessKey, 
                      region_name=ubuntu.region
                      )
                
                ec2describe_instances   =   ec2_client.describe_instances(InstanceIds=[ubuntu.instanceID])
                ec2State                =   ec2describe_instances['Reservations'][0]['Instances'][0]['State']['Name']
                if str(ec2State)=='stopped':
                    ec2_client.start_instances(InstanceIds=[ubuntu.instanceID])

        elif actionSelected=="Stop":
            for ubuntu in ubuntus:
                ec2_client = boto3.client('ec2', 
                      aws_access_key_id=ubuntu.accessKeyID, 
                      aws_secret_access_key=ubuntu.secretAccessKey, 
                      region_name=ubuntu.region
                      )
                
                ec2describe_instances   =   ec2_client.describe_instances(InstanceIds=[ubuntu.instanceID])
                ec2State                =   ec2describe_instances['Reservations'][0]['Instances'][0]['State']['Name']
                if str(ec2State)=='running':
                    ec2_client.stop_instances(InstanceIds=[ubuntu.instanceID])  

    elif areaSelected == "AllWindows":
        urlLink = "/aws/"
        windows  =   Aws.objects.filter(serverType='Windows')
        if actionSelected=="Stop":
            for window in windows:
                ec2_client = boto3.client('ec2', 
                      aws_access_key_id=window.accessKeyID, 
                      aws_secret_access_key=window.secretAccessKey, 
                      region_name=window.region
                      )
                
                ec2describe_instances   =   ec2_client.describe_instances(InstanceIds=[window.instanceID])
                ec2State                =   ec2describe_instances['Reservations'][0]['Instances'][0]['State']['Name']
                if str(ec2State)=='running':
                    ec2_client.stop_instances(InstanceIds=[window.instanceID])  

    return HttpResponseRedirect(urlLink, {})


# @login_required(login_url= '/users/login')
# def winrdpaccess(request, serverid):
#     currentserver   =   Aws.objects.get(pk=serverid)
#     clipRDPpass     =   pyperclip.copy(currentserver.rdpPass)
#     # pyperclip.copy(currentserver.rdpPass)

#     return response (clipRDPpass)

#Stop Start All Windows Servers - > START
@login_required(login_url= '/users/login')
def ssallwindowsservers(request,stopstart):  

    windowsServers = Aws.objects.filter(serverType="Windows")
    
    if stopstart == 1: # if 1 start all
        for windowsServer in windowsServers:
                ec2_client = boto3.client('ec2', 
                      aws_access_key_id=windowsServer.accessKeyID, 
                      aws_secret_access_key=windowsServer.secretAccessKey, 
                      region_name=windowsServer.region
                      )
                
                ec2describe_instances   =   ec2_client.describe_instances(InstanceIds=[windowsServer.instanceID])
                ec2State                =   ec2describe_instances['Reservations'][0]['Instances'][0]['State']['Name']
                if str(ec2State)=='stopped':
                    ec2_client.start_instances(InstanceIds=[windowsServer.instanceID])


        
    elif stopstart == 0: # if 0 stop all
        for windowsServer in windowsServers:
                ec2_client = boto3.client('ec2', 
                      aws_access_key_id=windowsServer.accessKeyID, 
                      aws_secret_access_key=windowsServer.secretAccessKey, 
                      region_name=windowsServer.region
                      )
                
                ec2describe_instances   =   ec2_client.describe_instances(InstanceIds=[windowsServer.instanceID])
                ec2State                =   ec2describe_instances['Reservations'][0]['Instances'][0]['State']['Name']
                if str(ec2State)=='running':
                    ec2_client.stop_instances(InstanceIds=[windowsServer.instanceID])

    return HttpResponseRedirect('/aws/windowsservers/', {})

#Stop Start All Windows Servers - > END