from django import forms
from App1.models import ChooseTask
#import App1.models
from App1.models import LoginAuthentication,Partners,RunCommands,NewServer,Document,ScriptDetails,CreateFolderPlaybook,CreateVPC,CreateSecurityGroup
from App1.models import LB_CreateNode,LB_CreatePool,LB_DeletePool,Linux_CreateLogicalVolume,Linux_CreateVolumeGroup,Linux_DeleteLogicalVolume,Linux_DeleteVolumeGroup,LB_ManagePool
from App1.models import  Windows_installFeature,Windows_uninstallFeature,Windows_ManageService,LB_DeleteNode,manage_Fortigate
# class HomeForm(forms.Form):
#     IPAddress = forms.CharField(label="ipAddress",max_length=100)
#     portNumber = forms.CharField(label="portNumber",max_length=100)
#     userName = forms.CharField(label="userName",max_length=100)
#     password = forms.CharField(label="password",max_length=100)
#     File= forms.FileField(label="csv_file")
#     
class  HomeForm(forms.ModelForm):  
    class Meta:  
        model = NewServer
        fields = "__all__" 
        
class Partners(forms.ModelForm):
    class Meta:
        model=Partners
        fields="__all__"
        
class RunCommands(forms.ModelForm):
    class Meta:
        model=RunCommands
        fields ="__all__"
class LoginAuthentication(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model=LoginAuthentication
        widgets = {
          'userName': forms.Textarea(attrs={'rows':7, 'cols':50}),
          'password': forms.Textarea(attrs={'rows':7, 'cols':50}),
        }
        fields="__all__"
        
        
class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ('description', 'document', )
        
class ScriptDetails(forms.ModelForm):
    RootPassword = forms.CharField(widget=forms.PasswordInput)
    NewUserName = forms.CharField(required=False)
    NewPassword = forms.CharField(required=False,widget=forms.PasswordInput)
    ConformPassWord = forms.CharField(required=False,widget=forms.PasswordInput)
    class Meta:
        model=ScriptDetails
        fields="__all__"
class ChooseTaskForm(forms.ModelForm):
    class Meta:
        model=ChooseTask
        fields="__all__"
class CreateFolderPlaybook(forms.ModelForm):
    ipAddress = forms.CharField(required=False)
    port=forms.CharField(required=False)
    username = forms.CharField(required=False)
    password=forms.CharField(required=False,widget=forms.PasswordInput)
    class Meta:
        model=CreateFolderPlaybook
        fields="__all__"
class CreateVPC(forms.ModelForm):
    class Meta:
        model=CreateVPC
        fields="__all__"
class CreateSecurityGroup(forms.ModelForm):
    class Meta:
        model=CreateSecurityGroup
        fields="__all__"
class LB_CreatePool(forms.ModelForm):
    class Meta:
        model=LB_CreatePool
        fields="__all__"
class LB_DeletePool(forms.ModelForm):
    class Meta:
        model=LB_DeletePool
        fields="__all__"
class LB_ManagePool(forms.ModelForm):
    class Meta:
        model=LB_ManagePool
        fields="__all__"
class LB_CreateNode(forms.ModelForm):
    class Meta:
        model=LB_CreateNode
        fields="__all__"
class LB_DeleteNode(forms.ModelForm):
    class Meta:
        model=LB_DeleteNode
        fields="__all__"
class Linux_CreateLogicalVolume(forms.ModelForm):
    class Meta:
        model=Linux_CreateLogicalVolume
        fields="__all__"
class Linux_DeleteLogicalVolume(forms.ModelForm):
    class Meta:
        model=Linux_DeleteLogicalVolume
        fields="__all__"
class Linux_CreateVolumeGroup(forms.ModelForm):
    class Meta:
        model=Linux_CreateVolumeGroup
        fields="__all__"
class Linux_DeleteVolumeGroup(forms.ModelForm):
    class Meta:
        model=Linux_DeleteVolumeGroup
        fields="__all__"
class Windows_installFeature(forms.ModelForm):
    class Meta:
        model=Windows_installFeature
        fields="__all__"
class Windows_uninstallFeature(forms.ModelForm):
    class Meta:
        model=Windows_uninstallFeature
        fields="__all__"
class Windows_ManageService(forms.ModelForm):
    class Meta:
        model=Windows_ManageService
        fields="__all__"
class Manage_Fortigate(forms.ModelForm):
    class Meta:
        model=manage_Fortigate
        fields="__all__"
