from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class CustomUser(AbstractUser):
    userType = models.CharField(max_length=20)

class Manager(models.Model):
    name=models.CharField(max_length=20)
    age=models.CharField(max_length=20)
    address=models.CharField(max_length=20)
    place=models.CharField(max_length=20)
    contact=models.CharField(max_length=20)
    email=models.CharField(max_length=20)
    pic=models.ImageField(max_length=20)
    psw=models.CharField(max_length=20)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)


class Employee(models.Model):
    name=models.CharField(max_length=20)
    man=models.ForeignKey(Manager,on_delete=models.CASCADE)
    address=models.CharField(max_length=20)
    place=models.CharField(max_length=20)
    contact=models.CharField(max_length=20)
    email=models.CharField(max_length=20)
    pic=models.ImageField(max_length=20)
    desig=models.CharField(max_length=20)
    r1=models.CharField(max_length=10,null=True,default=0)
    r2=models.CharField(max_length=10,null=True,default=0)
    r3=models.CharField(max_length=10,null=True,default=0)
    r4=models.CharField(max_length=10,null=True,default=0)
    r5=models.CharField(max_length=10,null=True,default=0)
    r6=models.CharField(max_length=10,null=True,default=0)
    rat1=models.CharField(max_length=10,null=True,default=0)
    rat2=models.CharField(max_length=10,null=True,default=0)
    rat3=models.CharField(max_length=10,null=True,default=0)
    rat4=models.CharField(max_length=10,null=True,default=0)
    rat5=models.CharField(max_length=10,null=True,default=0)
    rat6=models.CharField(max_length=10,null=True,default=0)
    coR=models.CharField(max_length=10,null=True,default=0)
    coRat=models.CharField(max_length=10,null=True,default=0)
    psw=models.CharField(max_length=20)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)







class Project(models.Model):
    title=models.CharField(max_length=20)
    desc=models.CharField(max_length=20)
    doc=models.ImageField(max_length=20)
    mid = models.ForeignKey(Manager,on_delete=models.CASCADE)
    status=models.CharField(max_length=20)


class Taskallocation(models.Model):
    prid = models.ForeignKey(Project,on_delete=models.CASCADE)
    empid = models.ForeignKey(Employee,on_delete=models.CASCADE)
    fstage=models.CharField(max_length=20)
    stat=models.CharField(max_length=20)


class Taskupdation(models.Model):
    prid = models.ForeignKey(Project,on_delete=models.CASCADE)
    empid = models.ForeignKey(Employee,on_delete=models.CASCADE)
    taskid = models.ForeignKey(Taskallocation,on_delete=models.CASCADE)
    cdate=models.DateField()
    exp=models.CharField(max_length=100)


class Workfeedback(models.Model):
    updid = models.ForeignKey(Taskupdation,on_delete=models.CASCADE)
    feedback=models.CharField(max_length=100)
    points=models.IntegerField()


class Appraisalreq(models.Model):
    empid = models.ForeignKey(Employee,on_delete=models.CASCADE)
    adate=models.DateField(auto_now=True)
    dfrom=models.DateField()
    dto=models.DateField()
    atype=models.CharField(max_length=100)
    status=models.CharField(max_length=100)


class Evaluation(models.Model):
    aid = models.ForeignKey(Appraisalreq,on_delete=models.CASCADE)
    mid = models.ForeignKey(Manager,on_delete=models.CASCADE)
    edate=models.DateField(auto_now=True)
    jobknowledge=models.CharField(max_length=100)
    qualityofwork=models.CharField(max_length=100)
    productivity=models.CharField(max_length=100)
    dependability=models.CharField(max_length=100)
    supervisorability=models.CharField(max_length=100)
    overallrating=models.CharField(max_length=100)


class ManEval(models.Model):
    r1=models.CharField(max_length=10)
    r2=models.CharField(max_length=10)
    r3=models.CharField(max_length=10)
    r4=models.CharField(max_length=10)
    r5=models.CharField(max_length=10,null=True)
    r6=models.CharField(max_length=10,null=True)
    man=models.ForeignKey(Manager,on_delete=models.CASCADE)
    emp=models.ForeignKey(Employee,on_delete=models.CASCADE)

class CoWorkEval(models.Model):
    review=models.CharField(max_length=20)
    emp=models.ForeignKey(Employee,on_delete=models.CASCADE)
    coworker=models.CharField(max_length=20)


