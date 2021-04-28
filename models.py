from pymongo import MongoClient
from djongo import models
from pandas.core.algorithms import mode

# def conncetion():
#     client = MongoClient(port=27017)
#     print(client)
#     db=client.NE_Automations
#     data=db.ntsmsps.find({"mid": "2345"})
#     print("----------welcome to mongodb")
#     print(data)

ScriptActions=(
    ('default','--Select Action Here--'),
    ('pwdChange','CHANGE PASSWORD'),
    )

MSP_CHOICES =(
    ('select Partner','--Select Partner--'),
    ('KAR','KAR'),
    ('GREENPAGES','GREENPAGES'),
    ('CDI', 'CDI'),
    ('CAROUSAL','CAROUSAL'),
)

CLIENT_CHOICES = (
    ('select Partner','--Select Client--'),
    ('IAAI','IAAI'),
    ('AssuriCare','AssuriCare'),
    ('BlueWaveSolar', 'BlueWaveSolar'),
    ('DeadRiver','DeadRiver'),
)
OS_CHOICES = (
    ('select File','--Device Type--'),
    ('Windows','WINDOWS'),
    ('Linux', 'LINUX'),
    ('Network','NETWORK'),
    ('Azure','AZURE'),
    ('AWS','AWS'),
    ('LB','LB')
)
class Partners(models.Model):
    mid = models.CharField(max_length=100)
    msp = models.TextField()
    created_at = models.DateTimeField()
    Active=models.BooleanField()
    class Meta:
        db_table="partners"
        
class ScriptDetails(models.Model):
    RootUserName = models.CharField(max_length=50)
    RootPassword = models.CharField(max_length=50)
    document = models.FileField(upload_to='D:\\eclipse-workspace\\AutomationStuff\\Documents\\')
    Change_Password = models.CharField(max_length=50,choices=(('no','NO'),('yes',"YES")),default='--Select Action Here--')
    NewUserName = models.CharField(max_length=50)
    NewPassword = models.CharField(max_length=50)
    ConformPassWord = models.CharField(max_length=50)
   
class ChooseTask(models.Model):
    action = models.CharField(max_length=200,choices=ScriptActions,default='--Select Action Here--')
         
class LoginAuthentication(models.Model):
    userName=models.CharField(max_length=100)
    password=models.CharField(max_length=100)
    
class RunCommands(models.Model):
    partner=models.CharField(max_length=200,choices=MSP_CHOICES,default='--select Partner')
    clients=models.CharField(max_length=200,choices=CLIENT_CHOICES,default='--select Client')
    Domain=models.CharField(max_length=200,choices=OS_CHOICES,default='--Opearting System--')
    class Meta:
        db_table="RunCommands"
  
class NewServer(models.Model):  
    ipAddress = models.CharField(max_length=30)  
    portNumber  = models.IntegerField()  
    userName = models.CharField(max_length=50)
    password =models.CharField(max_length=50)
    class Meta:  
        db_table = "NewServer" 
class Document(models.Model):
    description = models.CharField(max_length=255, blank=True)
    document = models.FileField(upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
 
class CreateFolderPlaybook(models.Model):
    folderPath=models.CharField(max_length=255)
    Device=models.CharField(max_length=50,choices=(('manual','Manual'),('inventory','Infrastructue')))
    ipAddress=models.CharField(max_length=100)
    port=models.CharField(max_length=100)
    username=models.CharField(max_length=100)
    password=models.CharField(max_length=100)
    class Meta:
        db_table="CreateFolderPlaybook"

class CreateVPC(models.Model):
    vpc_name=models.CharField(max_length=255)
    vpc_cidr=models.CharField(max_length=255)
    vpc_state=models.CharField(max_length=255)
    dns_support=models.CharField(max_length=255)
    dns_hostnames=models.CharField(max_length=255)
    tenancy=models.CharField(max_length=255)
    Execution_method=models.CharField(max_length=50,choices=(('ssh','SSH'),('jenkins','Jenkins')),default='--Execution Type--')
    
    class Meta:
        db_table="CreateVPC"
        
class CreateSecurityGroup(models.Model):
    security_group_state = models.CharField(max_length=255)
    security_group_name = models.CharField(max_length=255)
    security_group_description= models.CharField(max_length=255)
    vpc_id = models.CharField(max_length=255)
    ingress_protocol= models.CharField(max_length=100)
    ingress_port_from =models.IntegerField()
    ingress_port_to = models.IntegerField()
    ingress_destination_cidr_block =models.CharField(max_length=255)
    egress_protocol = models.CharField(max_length=100)
    egress_port_from = models.IntegerField()
    egress_port_to = models.IntegerField()
    egress_destination_cidr_block = models.CharField(max_length=255)
    Execution_method= models.CharField(max_length=50,choices=(('ssh','SSH'),('jenkins','Jenkins')),default='--Execution Type--')
    
    class Meta:
        db_table="CreateSecurityGroup"
        
class LB_CreatePool(models.Model):
    lb_ip = models.CharField(max_length=255)
    #username = models.CharField(max_length=255)
    #password = models.CharField(max_length=255)
    pool_name = models.CharField(max_length=255)
    partition = models.CharField(max_length=255)
    lb_method = models.CharField(max_length=255)
    slow_ramp_time = models.IntegerField()
    Execution_method= models.CharField(max_length=50,choices=(('ssh','SSH'),('jenkins','Jenkins')),default='--Execution Type--')
        
    class Meta:
        db_table="CreatePool"

class LB_DeletePool(models.Model):
    lb_ip = models.CharField(max_length=255)
    #username = models.CharField(max_length=255)
    #password = models.CharField(max_length=255)
    pool_name = models.CharField(max_length=255)
    partition = models.CharField(max_length=255)
    Execution_method= models.CharField(max_length=50,choices=(('ssh','SSH'),('jenkins','Jenkins')),default='--Execution Type--')
        
    class Meta:
        db_table="DeletePool"

class LB_ManagePool(models.Model):
    lb_ip = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    #password = models.CharField(max_length=255)
    pool_name = models.CharField(max_length=255)
    partition = models.CharField(max_length=255)
    Execution_method= models.CharField(max_length=50,choices=(('ssh','SSH'),('jenkins','Jenkins')),default='--Execution Type--')

    class Meta:
        db_table="ManagePool"

        
class LB_CreateNode(models.Model):
    lb_ip = models.CharField(max_length=255)
    #username = models.CharField(max_length=255)
    #password = models.CharField(max_length=255)
    host = models.CharField(max_length=255)
    node_name=models.CharField(max_length=255)
    Execution_method= models.CharField(max_length=50,choices=(('ssh','SSH'),('jenkins','Jenkins')),default='--Execution Type--')
        
    class Meta:
        db_table="CreateNode"
        
class LB_DeleteNode(models.Model):
    lb_ip = models.CharField(max_length=255)
    #username = models.CharField(max_length=255)
    #password = models.CharField(max_length=255)
    node_name = models.CharField(max_length=255)
    Execution_method= models.CharField(max_length=50,choices=(('ssh','SSH'),('jenkins','Jenkins')),default='--Execution Type--')
        
    class Meta:
        db_table="DeleteNode"
        
class Linux_CreateLogicalVolume(models.Model):
    server = models.CharField(max_length=255)
    #username = models.CharField(max_length=255)
    #password = models.CharField(max_length=255)
    volume_group_name = models.CharField(max_length=255)
    logical_volume_name = models.CharField(max_length=255)
    physcal_extent_size = models.CharField(max_length=255)
    physical_volumes = models.CharField(max_length=255)
    Execution_method= models.CharField(max_length=50,choices=(('ssh','SSH'),('jenkins','Jenkins')),default='--Execution Type--')
    
    class Meta:
        db_table="CreateLogicalVolume"

class Linux_DeleteLogicalVolume(models.Model):
    server = models.CharField(max_length=255)
    #username = models.CharField(max_length=255)
    #password = models.CharField(max_length=255)
    volume_group_name = models.CharField(max_length=255)
    logical_volume_name = models.CharField(max_length=255)
    Execution_method= models.CharField(max_length=50,choices=(('ssh','SSH'),('jenkins','Jenkins')),default='--Execution Type--')
    
    class Meta:
        db_table="DeleteLogicalVolume"
        
class Linux_CreateVolumeGroup(models.Model):
    server = models.CharField(max_length=255)
    #username = models.CharField(max_length=255)
    #password = models.CharField(max_length=255)
    volume_group_name = models.CharField(max_length=255)
    physical_volumes = models.CharField(max_length=255)
    physcal_extent_size = models.IntegerField()
    Execution_method= models.CharField(max_length=50,choices=(('ssh','SSH'),('jenkins','Jenkins')),default='--Execution Type--')
    
    class Meta:
        db_table="CreateVolumeGroup"

class Linux_DeleteVolumeGroup(models.Model):
    server = models.CharField(max_length=255)
    #username = models.CharField(max_length=255)
    #password = models.CharField(max_length=255)
    volume_group_name = models.CharField(max_length=255)
    Execution_method= models.CharField(max_length=50,choices=(('ssh','SSH'),('jenkins','Jenkins')),default='--Execution Type--')
    
    class Meta:
        db_table="DeleteVolumeGroup"
        
#class LB_DeleteNode(models.Model):

class Windows_installFeature(models.Model):
    server = models.CharField(max_length=255)
    #username = models.CharField(max_length=255)
    #password = models.CharField(max_length=255)
    windows_feature_name = models.CharField(max_length=255)
    Execution_method= models.CharField(max_length=50,choices=(('ssh','SSH'),('jenkins','Jenkins')),default='--Execution Type--')
    class Meta:
        db_table="InstallFeature"
    
class Windows_uninstallFeature(models.Model):
    server = models.CharField(max_length=255)
    #username = models.CharField(max_length=255)
    #password = models.CharField(max_length=255)
    windows_feature_name = models.CharField(max_length=255)
    Execution_method= models.CharField(max_length=50,choices=(('ssh','SSH'),('jenkins','Jenkins')),default='--Execution Type--')
    class Meta:
        db_table="UninstallFeature"
        
class Windows_ManageService(models.Model):
    server = models.CharField(max_length=255)
    #username = models.CharField(max_length=255)
    #password = models.CharField(max_length=255)
    windows_service_name = models.CharField(max_length=255)
    windows_service_state = models.CharField(max_length=255)
    Execution_method= models.CharField(max_length=50,choices=(('ssh','SSH'),('jenkins','Jenkins')),default='--Execution Type--')
    class Meta:
        db_table="ManageService"
        
class manage_Fortigate(models.Model):
    firewall_ip = models.CharField(max_length=255)
    #username = models.CharField(max_length=255)
    #password = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    address_name = models.CharField(max_length=255)
    address_type = models.CharField(max_length=255)
    ip_and_cidr = models.CharField(max_length=255)
    Execution_method= models.CharField(max_length=50,choices=(('ssh','SSH'),('jenkins','Jenkins')),default='--Execution Type--')
    class Meta:
        db_table="manage_Fortigate"
        

