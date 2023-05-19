from ast import Return

import datetime
from statistics import median
from tokenize import Double

from statistics import median
from tokenize import Double
from django.shortcuts import render, redirect

from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib import messages
from .models import *
import numpy as np
import pandas as pd
import re
import nltk
# nltk.download('stopwords')
# from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from sklearn.feature_extraction.text import CountVectorizer

from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score


dataset = pd.read_csv('F:\\Employe evaluation\\PerformanceEvaluation up\\Reviews.tsv', delimiter = '\t', quoting = 3)


corpus = []
for i in range(0, 1000):
    review = re.sub('[^a-zA-Z]', ' ', dataset['Review'][i])
    review = review.lower()
    review = review.split()
    ps = PorterStemmer()
    review = [ps.stem(word) for word in review if not word in set(('english'))]
    review = ' '.join(review)
    corpus.append(review)

cv = CountVectorizer(max_features = 1500)
X = cv.fit_transform(corpus).toarray()
y = dataset.iloc[:, 1].values
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.3, random_state = 42)

#MultinomialNB model
print("MultinomialNB")
classifier = MultinomialNB(alpha=0.1)
classifier.fit(X_train, y_train)



def index(request):
    return render(request,"index.html")


def login(request):
    if request.POST:
        uname=request.POST["username"]
        psw=request.POST["password"]
        user=authenticate(username=uname,password=psw)
        if user:
            if user.is_superuser == 1:
                    return redirect("/adminhome")
            elif user.userType == 'Employee':
                
                    request.session["email"]=uname
                    r = Employee.objects.get(email=uname)
                    request.session["id"]=r.id
                    request.session["name"]=r.name
                    return redirect("/employeehome")
            else:
                    request.session["email"]=uname
                    r = Manager.objects.get(email=uname)
                    request.session["id"]=r.id
                    request.session["name"]=r.name
                    return redirect("/managerhome")
            
                
        else:
            messages.info(request,"User dosent exist")
    return render(request,"login.html")



def adminhome(request):
    return render(request,"adminhome.html")

def employeeregistration(request):
    msg=""
    m=""
    data=""
    manid=request.session["id"]
    man=Manager.objects.get(id=manid)
    
    if(request.POST):
        name=request.POST.get("name")
        address=request.POST.get("address")
        place=request.POST.get("place")
        desig=request.POST.get("desig")
        contact=request.POST.get("contact")
        email=request.POST.get("email")
        pic=request.FILES['pic']
        password=request.POST.get("password")
         
        user=Employee.objects.filter(email=email,psw=password).exists()
        if not user:
            try:
                    u=CustomUser.objects.create_user(username=email,password=password,email=email,userType="Employee")
                    u.save()
            except Exception as e:
                    messages.info(request,e)
            else:
                    try:
                        s=Employee.objects.create(name=name,address=address,man=man,place=place,contact=contact,email=email,pic=pic,desig=desig,psw=password,user=u)
                        s.save()
                    except  Exception as e:
                        messages.info(request,e)
                    else:
                        print("hi")
                        messages.info(request,"registered succesfully")
        else:
            messages.info(request,"Something Went wrong") 
            return redirect("/employeeregistration")           
    
   
    data=Employee.objects.filter(man__id=manid)
  
    return render(request,"empreg.html",{"msg":msg  ,"data":data})




def deletemp(request):
    msg=""
    id=request.GET.get("id")
    # s="update tbl_employee set status='0' where id='"+str(id)+"'"
    # c.execute(s)
    Employee.objects.filter(id=id).update(user__is_active=1)
    messages.info(request,'Deleted')
    # db.commit()
    return redirect('employeeregistration')

def managerregistration(request):
    msg=""
    m=""
    data=""
    
    if(request.POST):
        name=request.POST.get("name")
        age=request.POST.get("age") 
        address=request.POST.get("address")
        place=request.POST.get("place")
        desig=request.POST.get("desig")
        pic=request.FILES["pic"]
        contact=request.POST.get("contact")
        email=request.POST.get("email")
        password=request.POST.get("password")
        print(email[-4:]+'---------------')
        print
        if int(age)<18:
            messages.info(request,'Age must be greater than 18')
            return redirect('managerregistration')
        if email[-4:]!=".com":
            messages.info(request,'Enter valid Email')
            return redirect('managerregistration') 
        user=Manager.objects.filter(email=email,psw=password).exists()
        if not user:
            try:
                    u=CustomUser.objects.create_user(username=email,password=password,email=email,userType="Manager")
                    u.save()
            except Exception as e:
                    messages.info(request,e)
            else:
                    try:
                        s=Manager.objects.create(name=name,age=age,address=address,place=place,contact=contact,email=email,pic=pic,psw=password,user=u)
                        s.save()
                    except  Exception as e:
                        messages.info(request,e)
                    else:
                        print("hi")
                        messages.info(request,"registered succesfully")
        else:
            messages.info(request,"Something Went wrong") 
            return redirect("/managerregistration")
    
   
    name=selectmanager()
  
    return render(request,"managerregistration.html",{"msg":msg,"name":name,"data":data})
def selectmanager():
    data=Manager.objects.filter(user__is_active=1)
    # c.execute("select * from tbl_manager where status='1'")
    # data=c.fetchall()
    return data
def deletemanager(request):
    msg=""
    id=request.GET.get("id")
    # s="update tbl_manager set status='0' where id='"+str(id)+"'"
    # c.execute(s)
    Manager.objects.filter(id=id).update(user__is_active=1)
    messages.info(request,'Deleted')
    db.commit()
    return redirect("managerregistration")
def managerhome(request):
    msg=""
    managerid=request.session["id"]
    if(request.POST):
        name=request.POST["name"]
        age=request.POST["age"]
        address=request.POST["address"]
        place=request.POST["place"]
        # desig=request.POST["desig"]
        contact=request.POST["contact"]
        email=request.POST["email"]
        
        # s="update tbl_manager set name='"+str(name)+"',age='"+str(age)+"',address='"+str(address)+"',place='"+str(place)+"',desig='"+str(desig)+"',contact='"+str(contact)+"' where id='"+str(managerid)+"'"
        try:
            
            Manager.objects.filter(id=managerid).update(name=name,age=age,address=address,place=place,contact=contact,email=email)

        except:
            msg="Sorry some error occured"
        else:
            msg="Data Updated"
    # s="select * from tbl_manager where id='"+str(managerid)+"'"
    # c.execute(s)
    data=Manager.objects.get(id=managerid)
    return render(request,"managerhome.html",{"d":data,"msg":msg})
def employeehome(request):
    msg=""
    empid=request.session["id"]
    if(request.POST):
        name=request.POST["name"]
        age=request.POST["age"]
        address=request.POST["address"]
        place=request.POST["place"]
        
        contact=request.POST["contact"]
        email=request.POST["email"]
        
        
        # s="update tbl_employee set name='"+str(name)+"',age='"+str(age)+"',address='"+str(address)+"',place='"+str(place)+"',contact='"+str(contact)+"' where id='"+str(empid)+"'"
        try:
            # c.execute(s)
            # db. commit()
            Employee.objects.filter(id=empid).update(name=name,age=age,address=address,place=place,contact=contact,email=email)
        except:
            msg="Sorry some error occured"
        else:
            msg="Data Updated"
    # s="select * from tbl_employee where id='"+str(empid)+"'"
    # c.execute(s)
    data=Employee.objects.get(id=empid)
    return render(request,"employeehome.html",{"d":data,"msg":msg})
def addproject(request):
    m=""
    data=""
    msg=""
    # s="Select * from tbl_manager where status='1'"
    # c.execute(s)
    manager=Manager.objects.filter(user__is_active=1)
    if(request.POST):
        title=request.POST.get("title")
        description=request.POST.get("description") 
        manager=request.POST['manager']
        doc=request.FILES['doc']
        musr=Manager.objects.get(id=manager)
        # m="insert into tbl_project(title,description,doc,status,managerid) values('"+str(title)+"','"+str(description)+"','"+uploaded_file_url+"','1','"+manager+"')"
        # c.execute(m)
        # msg="Data added Successfull"
        # db.commit()
        m=Project.objects.create(title=title,desc=description,doc=doc,mid=musr,status="Created")
        m.save()
    name=selectproject()

    return render(request,"addproject.html",{"msg":msg,"name":name,"manager":manager})

def selectproject():
    data=Project.objects.filter(status="Created")
    # c.execute("select tbl_project.*,tbl_manager.name from tbl_project,tbl_manager where tbl_project.status='1' and tbl_manager.id=tbl_project.managerid")
    # data=c.fetchall()
    return data
def deleteproject(request):
    msg=""
    id=request.GET.get("id")
    data=Project.objects.get(id=id).delete()
    return render(request,"addproject.html",{"msg":msg})

def assignproject(request):
    data="" 
    managerid=request.session['id']
    # s="select * from tbl_project where status='1' and managerid='"+str(managerid)+"'"
    # c.execute(s)
    # data=c.fetchall()
    data=Project.objects.filter(status="Created",mid=managerid)
    return render(request,"allocation.html",{"data":data})
def allocatemanager(request):
    msg=""
    manid=request.session["id"]
    
    if(request.POST):
        managerid=request.session['id']
        projectid=request.GET.get("id")
        empid=request.POST.get("empid")
        fstage=request.POST.get("fstage")
        prj=Project.objects.get(id=projectid)
        empusr=Employee.objects.get(id=empid)
        # m="select count(*) count from tbl_taskallocation where empid='"+str(empid)+"' and fstage='"+str(fstage)+"' and projectid='"+str(projectid)+"'"
        # c.execute(m)
        # msg="Already Allocated This Task"
        # i=c.fetchone()
        t=Taskallocation.objects.filter(empid=empid,fstage=fstage,prid=projectid).exists()
        if not t:
            # m="insert into tbl_taskallocation(projectid,empid,fstage,status) values('"+str(projectid)+"','"+str(empid)+"','"+str(fstage)+"','Allocated')"
            # c.execute(m)
            # msg="Allocated"
            # db.commit()
            tt=Taskallocation.objects.create(prid=prj,empid=empusr,fstage=fstage,stat='Allocated')
            tt.save()
            prj.status = "Assigned"
            prj.save()
            return redirect("assignproject")
        else:
            return redirect("assignproject")
    ename=Employee.objects.filter(man__id=manid)
    return render(request,"allocatemanager.html",{"ename":ename,"msg":msg})

def viewtasksemployee(request):
    data=""
    employeeid=request.session['id']
    # s="select tbl_project.id,tbl_project.title,tbl_project.description,tbl_project.doc,tbl_manager.name,tbl_taskallocation.fstage,tbl_manager.id,tbl_taskallocation.id from tbl_project,tbl_manager,tbl_taskallocation where tbl_project.id=tbl_taskallocation.projectid and tbl_manager.id=tbl_project.managerid and tbl_taskallocation.empid='"+str(employeeid)+"'"
    # c.execute(s)
    data=Taskallocation.objects.filter(empid=employeeid)
    return render(request,"viewtaskemployee.html",{"data":data})


def empworkupdate(request):
    data=""
    employeeid=request.session['id']
    # s="select tbl_taskupdation.id,tbl_project.title,tbl_project.description,tbl_project.doc,tbl_manager.name,tbl_taskallocation.fstage,tbl_taskupdation.exp,tblworkfeedback.feedback,tblworkfeedback.points from tbl_project,tbl_manager,tbl_taskallocation,tblworkfeedback,tbl_taskupdation where tbl_project.id=tbl_taskallocation.projectid and tbl_manager.id=tbl_project.managerid and tbl_taskallocation.empid='"+str(employeeid)+"' and tblworkfeedback.updateid=tbl_taskupdation.id and tbl_taskupdation.empid='"+str(employeeid)+"' and tbl_taskupdation.projetctid=tbl_project.id and tbl_taskupdation.taskid=tbl_taskallocation.id"
    # c.execute(s)
    data=Workfeedback.objects.filter(updid__empid__id=employeeid)
    return render(request,"empworkupdate.html",{"data":data})
def taskupdation(request):
    msg=""
    if(request.POST):
        empid=request.session['id']
        projectid=request.GET.get("id")
        taskid=request.GET.get("taskid")
        mid=request.GET.get("mid")
        cdate=request.POST.get("cdate")
        description=request.POST.get("exp")
        empusr=Employee.objects.get(id=empid)
        prj=Project.objects.get(id=projectid)
        tsk=Taskallocation.objects.get(id=taskid)
        tu=Taskupdation.objects.filter(empid=empid,taskid=taskid).exists()
        if not tu:
        # m="select count(*) count from tbl_taskupdation where empid='"+str(empid)+"' and taskid='"+str(taskid)+"'"
        # c.execute(m)
        # msg="Already Allocated This Task"
        # i=c.fetchone()
        # if(i[0]==0):
        # m="insert into tbl_taskupdation(empid,projetctid,taskid,cdate,exp) values('"+str(empid)+"','"+str(projectid)+"','"+str(taskid)+"','"+str(cdate)+"','"+str(description)+"')"
        # print(m)
        # c.execute(m)
            msg="Updated"
        # db.commit()
            m=Taskupdation.objects.create(empid=empusr,prid=prj,taskid=tsk,cdate=cdate,exp=description)
            return redirect("viewtasksemployee")
        else:
            return redirect("viewtasksemployee")
    return render(request,"taskupdation.html",{"msg":msg })

def managerupdates(request):
    data=""
    employeeid=request.session['id']
    # s="select tbl_taskupdation.id,tbl_project.title,tbl_project.description,tbl_employee.name,tbl_taskallocation.fstage,tbl_taskupdation.exp from tbl_project,tbl_employee,tbl_taskallocation,tbl_taskupdation where tbl_project.id=tbl_taskallocation.projectid and tbl_employee.id=tbl_taskallocation.empid and tbl_project.managerid='"+str(employeeid)+"' and tbl_taskupdation.empid=tbl_employee.id and tbl_taskupdation.projetctid=tbl_project.id and tbl_taskupdation.taskid=tbl_taskallocation.id"
    # print(s)
    # c.execute(s)
    # data=c.fetchall()
    data=Taskupdation.objects.filter(prid__mid__id=employeeid)
    return render(request,"managerupdates.html",{"data":data})
def manageraddfeedback(request):
    msg=""
    uid=request.GET.get("id")
    rate=request.GET.get("rate")
    s="Select count(*) from tblworkfeedback where updateid='"+uid+"'"
    c.execute(s)
    d=c.fetchone()
    if d[0]>0:
        msg="Already added your rating"
    if request.POST:
        feedback=request.POST['txtfeedback']
        s="insert into tblworkfeedback (updateid,feedback,points) values('"+uid+"','"+feedback+"','"+rate+"')"
        try:
            c.execute(s)
            db.commit()
        except:
            msg="Sorry some error occured"
        else:
            msg="Feedback added"
    return render(request,"manageraddfeedback.html",{"msg":msg,"id":uid,"rate":rate})

def adminallocation(request):
    # s="select tbl_taskupdation.id,tbl_project.title,tbl_project.description,tbl_project.doc,tbl_manager.name,tbl_taskallocation.fstage,tbl_taskupdation.exp,tblworkfeedback.feedback,tblworkfeedback.points,tbl_employee.name from tbl_project,tbl_manager,tbl_taskallocation,tblworkfeedback,tbl_taskupdation,tbl_employee where tbl_project.id=tbl_taskallocation.projectid and tbl_manager.id=tbl_project.managerid and tbl_taskallocation.empid=tbl_employee.id and tblworkfeedback.updateid=tbl_taskupdation.id and tbl_taskupdation.empid=tbl_employee.id and tbl_taskupdation.projetctid=tbl_project.id and tbl_taskupdation.taskid=tbl_taskallocation.id"
    # c.execute(s)
    # data=c.fetchall()
    data=Workfeedback.objects.all()
    return render(request,"adminallocation.html",{"data":data})

def empappraisalrequest(request):
    msg=""

    employeeid=request.session['id']
    me=Employee.objects.get(id=employeeid)
    employee=Employee.objects.exclude(id=employeeid)
   
    s=Employee.objects.get(id=employeeid)
    if request.POST:
        emp=request.POST['emp']
        e=Employee.objects.get(id=emp)
        rev=request.POST['rev']
        new_review = rev
        new_review = re.sub('[^a-zA-Z]', ' ', new_review)
        new_review = new_review.lower()
        new_review = new_review.split()
        ps = PorterStemmer()
        print("REVIWS """"""")
        print(new_review)
        all_stopwords = ["not","in","a"]
        # all_stopwords.remove('not')
        new_review = [ps.stem(word) for word in new_review if not word in set(all_stopwords)]
        new_review = ' '.join(new_review)
        new_corpus = [new_review]
        new_X_test = cv.transform(new_corpus).toarray()
        new_y_pred = classifier.predict(new_X_test)
     
        rat=e.coR
        
        newRat = int(rat)+int(new_y_pred)
        e.coR = newRat
        e.save()
        try:
            c=CoWorkEval.objects.create(review=rev,emp=e,coworker=me.name)            
            c.save
        except:
            msg="Sorry some error"
        else:
            msg="Review "
            hotel2=Employee.objects.get(id=emp)
            rat1=hotel2.coR
            total=CoWorkEval.objects.filter(emp__id=emp).count()
            print(total)
            star=float(rat1) / int(total)
            star=round(star,2)
            # star1="{:.2f}".format(star)
            star=star * 5
            hotel2.coRat=round(star,2)
            hotel2.save()
    
    return render(request,"empappraisalrequest.html",{"msg":msg,"s":s,"employee":employee})
def managerappraisal(request):
    
  
    data=Appraisalreq.objects.all()
    return render(request,"managerappraisal.html",{"data":data})

def manageraddevaluation(request):
    msg=""
    reqid=request.GET.get('id')
    employeeid=request.session['id']
    apreq=Taskupdation.objects.get(id=reqid)
    empid=apreq.empid.id
    hotel2=Employee.objects.get(id=empid)


    musr=Manager.objects.get(id=employeeid)
   
    
    if request.POST:
            jk=request.POST['jk']
            qual=request.POST['qual']
            prod=request.POST['prod']
            dep=request.POST['dep']
            sup=request.POST['sup']
            over=request.POST['over']

            new_review1 = jk
            new_review2 = qual
            new_review3 = prod
            new_review4 = dep
            new_review5 = sup
            new_review6 = over
            new_review1 = re.sub('[^a-zA-Z]', ' ', new_review1)
            new_review2 = re.sub('[^a-zA-Z]', ' ', new_review2)
            new_review3 = re.sub('[^a-zA-Z]', ' ', new_review3)
            new_review4 = re.sub('[^a-zA-Z]', ' ', new_review4)
            new_review5 = re.sub('[^a-zA-Z]', ' ', new_review5)
            new_review6 = re.sub('[^a-zA-Z]', ' ', new_review6)
            new_review1 = new_review1.lower()
            new_review2 = new_review2.lower()
            new_review3 = new_review3.lower()
            new_review4 = new_review4.lower()
            new_review5 = new_review5.lower()
            new_review6 = new_review6.lower()
            new_review1 = new_review1.split()
            new_review2 = new_review2.split()
            new_review3 = new_review3.split()
            new_review4 = new_review4.split()
            new_review5 = new_review5.split()
            new_review6 = new_review6.split()
            ps = PorterStemmer()
            all_stopwords = ["not","in","a"]
            # all_stopwords.remove('not')
            new_review1 = [ps.stem(word) for word in new_review1 if not word in set(all_stopwords)]
            new_review2 = [ps.stem(word) for word in new_review2 if not word in set(all_stopwords)]
            new_review3 = [ps.stem(word) for word in new_review3 if not word in set(all_stopwords)]
            new_review4 = [ps.stem(word) for word in new_review4 if not word in set(all_stopwords)]
            new_review5 = [ps.stem(word) for word in new_review5 if not word in set(all_stopwords)]
            new_review6 = [ps.stem(word) for word in new_review6 if not word in set(all_stopwords)]
            new_review1 = ' '.join(new_review1)
            new_review2 = ' '.join(new_review2)
            new_review3 = ' '.join(new_review3)
            new_review4 = ' '.join(new_review4)
            new_review5 = ' '.join(new_review5)
            new_review6 = ' '.join(new_review6)
            new_corpus1 = [new_review1]
            new_corpus2 = [new_review2]
            new_corpus3 = [new_review3]
            new_corpus4 = [new_review4]
            new_corpus5 = [new_review5]
            new_corpus6 = [new_review6]
            new_X_test1 = cv.transform(new_corpus1).toarray()
            new_X_test2 = cv.transform(new_corpus2).toarray()
            new_X_test3 = cv.transform(new_corpus3).toarray()
            new_X_test4 = cv.transform(new_corpus4).toarray()
            new_X_test5 = cv.transform(new_corpus5).toarray()
            new_X_test6 = cv.transform(new_corpus6).toarray()
            new_y_pred1 = classifier.predict(new_X_test1)
            print("predicted result(1/0)")
            print(new_y_pred1)
            new_y_pred2 = classifier.predict(new_X_test2)
            new_y_pred3 = classifier.predict(new_X_test3)
            new_y_pred4 = classifier.predict(new_X_test4)
            new_y_pred5 = classifier.predict(new_X_test5)
            new_y_pred6 = classifier.predict(new_X_test6)
            
            rat1=hotel2.r1
            rat2=hotel2.r2
            rat3=hotel2.r3
            rat4=hotel2.r4
            rat5=hotel2.r5
            rat6=hotel2.r6
            print("count of positive reviews")
            print(rat1)

            newRat1 = int(rat1)+int(new_y_pred1)
            print("newest count of positive rating")
            print(newRat1)
            hotel2.r1 = newRat1
            apreq.save()

            print("updated")
            print(hotel2.r1)

            newRat2 = int(rat2)+int(new_y_pred2)
            hotel2.r2 = newRat2
            apreq.save()
            newRat3 = int(rat3)+int(new_y_pred3)
            hotel2.r3 = newRat3
            apreq.save()
            newRat4 = int(rat4)+int(new_y_pred4)
            hotel2.r4 = newRat4
            apreq.save()
            newRat5 = int(rat5)+int(new_y_pred5)
            hotel2.r5 = newRat5
            apreq.save()
            newRat6 = int(rat6)+int(new_y_pred6)
            hotel2.r6 = newRat6
            apreq.save()

            try:
                
                mane=ManEval.objects.create(r1=jk,r2=qual,r3=prod,r4=dep,r5=sup,r6=over,man=musr,emp=hotel2)
                mane.save()
                msg="Success"






            except Exception as e:
                msg=e
            else:

                rt1=hotel2.r1

                rt2=hotel2.r2
                rt3=hotel2.r3
                rt4=hotel2.r4
                rt5=hotel2.r5
                rt6=hotel2.r6
                total=ManEval.objects.filter(emp__id=empid).count()
                print(total )
                star=float(rt1) / int(total)
                star=round(star,2)
                star=star * 5
                hotel2.rat1=round(star,2)

                star=float(rt2) / int(total)
                star=round(star,2)
                star=star * 5
                hotel2.rat2=round(star,2)

                star=float(rt3) / int(total)
                star=round(star,2)
                star=star * 5
                hotel2.rat3=round(star,2)

                star=float(rt4) / int(total)
                star=round(star,2)
                star=star * 5
                hotel2.rat4=round(star,2)

                star=float(rt5) / int(total)
                star=round(star,2)
                star=star * 5
                hotel2.rat5=round(star,2)

                star=float(rt6) / int(total)
                star=round(star,2)
                star=star * 5
                hotel2.rat6=round(star,2)

                hotel2.save()
                return redirect("/managerupdates")
                
    return render(request,"manageraddevaluation.html",{"msg":msg})

def adminappraisal(request):
    
   
    data=Employee.objects.all()
    return render(request,"adminappraisal.html",{"data":data})

def adminevaluation(request):
    aid=request.GET.get("id")
    # s="Select tbl_manager.name, tbl_evaluation.edate,tbl_evaluation.jobknowledge,tbl_evaluation.qualityofwork,tbl_evaluation.productivity,tbl_evaluation.dependability,tbl_evaluation.supervisorability,tbl_evaluation.overallrating from tbl_evaluation,tbl_manager where tbl_evaluation.managerid=tbl_manager.id and tbl_evaluation.aid='"+str(aid)+"' "
    # c.execute(s)
    data=Evaluation.objects.filter(aid=aid)
    # if request.POST:
    #     adminanalyse(aid)
    return render(request,"adminevaluation.html",{"data":data})
    
def adminanalyse(aid):
    s="select empid from tbl_appraisalrequest where apId='"+aid+"' "
    c.execute(s)
    d=c.fetchone()
    empid=d[0]

    import pymysql
    import csv
    import sys

    db_opts = {
        'user': 'root',
        'password': '',
        'host': 'localhost',
        'database': 'dbempevaluation'
    }

    db = pymysql.connect(**db_opts)
    cur = db.cursor()

    sql = "SELECT feedback from tblworkfeedback where updateid in(select id from tbl_taskupdation where empid='"+str(empid)+"')"
    csv_file_path = 'EvaluationApp/static/data/dataset.csv'

    try:
        cur.execute(sql)
        rows = cur.fetchall()
    finally:
        db.close()
# Continue only if there are rows returned.
    if rows:
    # New empty list called 'result'. This will be written to a file.
        result = list()

    # The row name is the first entry for each entity in the description tuple.
        column_names = list()
        for i in cur.description:
            column_names.append(i[0])

        result.append(column_names)
        for row in rows:
            result.append(row)

    # Write result to file.
        with open(csv_file_path, 'w', newline='') as csvfile:
            csvwriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            for row in result:
                csvwriter.writerow(row)
    else:
        sys.exit("No rows found for query: {}".format(sql))
    analyse()

def analyse():
    # from django.shortcuts import render
# from django.http import HttpResponse,HttpResponseRedirect
# import pymysql
    import csv
# #from django.shortcuts import render_to_response
# from django.core.files.storage import FileSystemStorage
# import simplejson as json
# from django.http import Http404
# from datetime import date
# from datetime import datetime
# import datetime
    from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
    import pandas as pd
    import re
    analyser = SentimentIntensityAnalyzer()
    # print(analyser)
    def print_sentiment_scores(name):
        lst=[]
        dataset = pd.read_csv('EvaluationApp/static/data/dataset.csv', delimiter = ',')
        f=open('EvaluationApp/static/data/dataset.csv')
        reader=csv.reader(f)
        lines=len(list(reader))
        print(lines)
        corpus = []
        corpusn = []
        print("dataset")
        
    # dataset1 = pd.read_csv('E:\PROJECTS\aluva\COVID\analysis.csv', delimiter = ',')
        # iteam=[]
    # for j in range(0, 20):
    #         pname = re.sub('[^a-zA-Z]', ' ', dataset['name'][j])
    #         iteam.append(pname)
    # for j in range(0, 20):
    #         k=0
        cnt=0
        cntn=0
        print("kkkkkkkkkkkkkkkkkkkkkkkkkkkk")
        print(name)
        pos=0
        neg=0
        neu=0
       
        for i in range(0,lines-1):  
            review = re.sub('[^a-zA-Z0-1]', ' ', dataset['feedback'][i])
            #review = re.sub(r'[\xe2\x80\x99s]', ' ', dataset['text'][i])
            cor=0
            # print(review)
            # for i in terms:
            #     # print(i)
            #     if i in review.lower():
            #         cor=cor+1
            
            # if cor>0:
            #     print("Accepted review: ", review)
            #pname = re.sub('[^a-zA-Z0-1]', ' ', dataset['text'][i])
            # name= re.sub('[^a-zA-Z0-1]', ' ', name)
            # print(name.replace(",", ""))
            # if(name.replace(",", "")==pname):
            #     print("ppppppppppppppppppppppppppppp")
            #     print(name)
            vadersenti = analyser.polarity_scores(review)
            if vadersenti["compound"] >= 0.5:
                    pos=pos+1
            elif vadersenti["compound"] <= -0.5:
                    neg=neg+1
            else:
                    neu=neu+1
            
            print(i)
            print("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
            print(vadersenti)
            cnt=cnt+vadersenti['pos']
            cntn=cntn+vadersenti['neg']
            corpus.append(cnt)
            corpusn.append(cntn)
            
        print("Scores")
        print("************************")
        print("Pos=",pos)
        print("Neg=",neg)
        print("Neu=",neu)
        print("************************")
        corpus.append(cnt)
        corpusn.append(cntn)
        lst.append(name)
        lst.append(corpus)
        lst.append(corpusn)
        print(lst)

        import matplotlib.pyplot as plt
        labels = ['negative', 'neutral', 'positive']
        sizes  = [neg, neu, pos]
        plt.pie(sizes, labels=labels, autopct='%1.1f%%') # autopct='%1.1f%%' gives you percentages printed in every slice.
        plt.axis('equal')  # Ensures that pie is drawn as a circle.
        plt.title("Sentiment analysis result")
        if neg>0 or neu>0 or pos>0:
            plt.show()
        return lst
    
    print_sentiment_scores("")
def adminapproveappraisal(request):
    aid=request.GET.get("id")
    status=request.GET.get("status")
    # s="update tbl_appraisalrequest set status='"+status+"' where apId='"+aid+"'"
    # c.execute(s)
    # db.commit()
    s=Appraisalreq.objects.filter(id=aid).update(status=status)
    return redirect("/adminappraisal")
