from django.db import models
from user.models import Userprofile
from django.urls import reverse
import uuid

# Create your models here.
STATUS_CHOICES = (
    ("ACTIVE", "Active"),
    ("DEACTIVE", "Deactive"),
)

class Client(models.Model):
    user = models.OneToOneField(Userprofile, on_delete=models.CASCADE,null=True,blank=True)
    phone_number=models.CharField(max_length=10,null=True,blank=True)
    image=models.ImageField(upload_to='images/',null=True,blank=True)
    email=models.EmailField(null=True,blank=True)
    dob =  models.CharField(max_length=50, default=None, null=True, blank=True)
    gender=models.CharField(max_length=50,default=True,null=True)
    place=models.CharField(max_length=50,null=True,blank=True)
    country=models.CharField(max_length=50,default=True,null=True,blank=True)
    is_active=models.BooleanField(default=True,null=True,blank=True)
    created_at=models.DateTimeField(auto_now_add=True,null=True,blank=True)
    updated_at=models.DateTimeField(auto_now_add=True,null=True,blank=True)
class placevisited(models.Model):
    user=models.ForeignKey(Userprofile,on_delete=models.CASCADE)
    placename=models.CharField(max_length=50,default=True,null=True,blank=True)

    is_active=models.BooleanField(default=True,null=True,blank=True)
    created_at=models.DateTimeField(auto_now_add=True,null=True,blank=True)
    updated_at=models.DateTimeField(auto_now_add=True,null=True,blank=True)



class Wandergroup(models.Model):
    user=models.ForeignKey(Userprofile,on_delete=models.CASCADE,null=True,blank=True)
    groupname=models.CharField(max_length=100,null=True,blank=True)
    groupimage=models.FileField(upload_to='groupimage/',null=True,blank=True)
    groupdescription=models.CharField(max_length=100,null=True,blank=True)
    grouppermission=models.BooleanField(null=True,blank=True,default=False)
    grouplink=models.CharField(max_length=100,null=True,blank=True,unique=True)
    grouphashtag=models.CharField(max_length=100,null=True,blank=True)
    status=models.BooleanField(null=True,blank=True)
    is_active=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True,null=True,blank=True)
    updated_at=models.DateTimeField(auto_now_add=True,null=True,blank=True)

    def save(self, *args, **kwargs):
        if not self.grouplink:
            self.grouplink = str(uuid.uuid4())  # Generate unique grouplink if not provided
        super().save(*args, **kwargs)


    def get_grouplink(self):
        print('defgetgrouplink')
        return reverse('join_group', kwargs={'grouplink': self.grouplink})
class grouphashtag(models.Model):
    user=models.ForeignKey(Userprofile,on_delete=models.CASCADE)
    group=models.ForeignKey(Wandergroup,on_delete=models.CASCADE,null=True,related_name='creategrouptag')
    hashtag=models.CharField(max_length=200,default=True,null=True,blank=True)
    is_active=models.BooleanField(default=True,null=True,blank=True)
    created_at=models.DateTimeField(auto_now_add=True,null=True,blank=True)
    updated_at=models.DateTimeField(auto_now_add=True,null=True,blank=True)
class posts(models.Model):
    user=models.ForeignKey(Userprofile,on_delete=models.CASCADE)
    groupid=models.ForeignKey(Wandergroup,on_delete=models.CASCADE,null=True,blank=True)
    postcontent=models.CharField(max_length=200,default=True,null=True,blank=True)
    postfile=models.ImageField(upload_to='images/',null=True,blank=True)
    is_active=models.BooleanField(default=True,null=True,blank=True)
    created_at=models.DateTimeField(auto_now_add=True,null=True,blank=True)
    updated_at=models.DateTimeField(auto_now_add=True,null=True,blank=True)
class hashtag(models.Model):
    user=models.ForeignKey(Userprofile,on_delete=models.CASCADE)
    post=models.ForeignKey(posts,on_delete=models.CASCADE,null=True)
    hashtag=models.CharField(max_length=200,default=True,null=True,blank=True)
    is_active=models.BooleanField(default=True,null=True,blank=True)
    created_at=models.DateTimeField(auto_now_add=True,null=True,blank=True)
    updated_at=models.DateTimeField(auto_now_add=True,null=True,blank=True)
class Connections(models.Model):
    user=models.ForeignKey(Userprofile,on_delete=models.CASCADE,null=True,blank=True)
    client=models.ForeignKey(Client,on_delete=models.CASCADE,null=True,blank=True)
    clientuserid=models.ForeignKey(Userprofile,on_delete=models.CASCADE,null=True,blank=True,related_name='connectionid')
    status = models.BooleanField(null=True, blank=True)
    is_active = models.BooleanField(default=True, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)



INVITATION_CHOICES=[('sharelink','sharelink'),('invitation','invitation')]
class Groupinvitation(models.Model):
    user=models.ForeignKey(Userprofile,on_delete=models.CASCADE,null=True,blank=True)
    toid=models.ForeignKey(Userprofile,on_delete=models.CASCADE,null=True,blank=True,related_name='toid')
    i_type=models.CharField(max_length=100,null=True,blank=True,choices=INVITATION_CHOICES)
    group=models.ForeignKey(Wandergroup,on_delete=models.CASCADE,null=True,blank=True)
    grouplink=models.CharField(max_length=100,null=True,blank=True)
    status = models.BooleanField(null=True, blank=True,default=False)
    is_active = models.BooleanField(default=True, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

class Assignedgroups(models.Model):
    user=models.ForeignKey(Userprofile,on_delete=models.CASCADE,null=True,blank=True)
    groupid=models.ForeignKey(Wandergroup,on_delete=models.CASCADE,null=True,blank=True)
    status = models.BooleanField(null=True, blank=True,default=False)
    groupaddmode=models.CharField(max_length=100,null=True,blank=True)
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now_add=True, null=True,blank=True)
    is_invited = models.BooleanField(null=True, blank=True,default=False)
class Chat(models.Model):
    message = models.CharField(max_length=100)
    from_id = models.ForeignKey(Userprofile,on_delete=models.CASCADE,related_name="fuser",null=True,blank=True)
    group_id=models.ForeignKey(Wandergroup,on_delete=models.CASCADE,null=True,blank=True)
    to_id = models.ForeignKey(Userprofile,on_delete=models.CASCADE,related_name="tuser",null=True,blank=True)
    # status = models.CharField(max_length=20, null=True, choices=STATUS_CHOICES, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
class Likepost(models.Model):
    user=models.ForeignKey(Userprofile,on_delete=models.CASCADE,null=True,blank=True)
    postid=models.ForeignKey(posts,on_delete=models.CASCADE,null=True,blank=True)
    groupid=models.ForeignKey(Wandergroup,on_delete=models.CASCADE,null=True,blank=True)
    likestatus=models.BooleanField(default=False,null=True,blank=True)
    status = models.CharField(max_length=20, null=True, choices=STATUS_CHOICES, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
class Commentpost(models.Model):
    user=models.ForeignKey(Userprofile,on_delete=models.CASCADE,null=True,blank=True)
    postid=models.ForeignKey(posts,on_delete=models.CASCADE,null=True,blank=True)
    groupid=models.ForeignKey(Wandergroup,on_delete=models.CASCADE,null=True,blank=True)
    comment=models.CharField(max_length=200,null=True,blank=True)
    status = models.CharField(max_length=20, null=True, choices=STATUS_CHOICES, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
