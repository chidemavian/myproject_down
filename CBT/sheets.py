
def currentnumer(student,session,term,subject,exam):
    qc=cbtcurrentquestion.objects.get(student=student,
	    term =term,
	    subject=subject,
	    session=currse,
	    exam_type=ex.exam_type)

	number=int(qc.number)



def next(request):
    if "userid" in request.session:            
        if request.method=='POST':
            varuser=request.session['userid']
            c='where u go'

            student=Student.objects.get(admitted_session=currse,fullname=varuser,gone=False)

            sub=tblcbtsubject.objects.get(klass=student.admitted_class,session=currse,status='ACTIVE')
            subject=sub.subject

            qwe=tblquestion.objects.filter(session=currse,
                term=term, klass=student.admitted_class,subject=subject,
                exam_type=ex.exam_type,section='A').count()

            qc=cbtcurrentquestion.objects.get(student=student,
                term =term,
                subject=subject,
                session=currse,
                exam_type=ex.exam_type)

            number=int(qc.number)

            if 'gender' in request.POST:
                a= request.POST['gender']

                if a == str(d) or a == str(e) or a == str(g) or a == str(w):

                try:
                    dt = cbttrans.objects.get(student=student,session=currse,term=term,
                        exam_type=ex.exam_type,no=number,subject=subject)

                    ty='update'
                except:
                 
                    dt=cbtold.objects.get(student=student,session=currse,
                        term=term,exam_type=ex.exam_type,
                        klass=student.admitted_class,subject=subject)

                    ty='save'

                selq= tblquestion.objects.get(session=currse,term=term,
                    exam_type=ex.exam_type,klass=student.admitted_class,
                    subject= subject,id=dt.qstcode)

                sek=selq.qstn                 
                ans=tblans.objects.get(qstn=selq)
                ans=ans.ans
                b=str(ans)


                opti = tbloptions.objects.get(qstn=selq)
                d=opti.a
                e=opti.b
                g=opti.c
                w=opti.d

                if a == b: # if my answer is correct
                    if ty=='update':
                        k=cbttrans.objects.filter(student=student,session=currse,term=term,
                            exam_type=ex.exam_type,qstcode=selq.id,
                            subject=subject,).update(score =1,stu_ans=a)

                    elif ty=='save':
                        
                        k=cbttrans(student=student,session=currse,term=term,
                            exam_type=ex.exam_type,question=selq,stu_ans=a, score = 1, 
                            no=number,qstcode=selq.id,subject=subject).save()
                else:#if my ans is wrong
                   
                    if a == str(d) or a == str(e) or a == str(g) or a == str(w):
                        if ty=='update':    
                            cbttrans.objects.filter(student=student,session=currse,term=term,exam_type=ex.exam_type,
                                qstcode=selq.id,subject=subject).update(score=0,stu_ans=a)
        
                        elif ty=='save':
                            cbttrans(student=student,term=term, exam_type=ex.exam_type,question=selq,
                                stu_ans=a, score = 0,no=number,status=0,qstcode=selq.id,subject=subject,
                                session=currse).save()
                    else:
                        pass


                        # return HttpResponseRedirect('/welcome/')
     
### porting to reportsheet module****************
                add=cbttrans.objects.filter(student=student,session=currse,term=term,                        
                        exam_type=ex.exam_type,
                        subject=subject).aggregate(Sum('score'))

                add = add['score__sum']

                acaderec = StudentAcademicRecord.objects.get(student = student, term=term)

        #               remove this line when you are ready
                subject ='SCIENCE'

                if ex.exam_type=='Welcome back':
                    subsco = SubjectScore.objects.filter(academic_rec = acaderec,
                        subject=subject,term=term,session=currse).update(first_ca=add)

                 
                if ty == 'save': #if i added a new entry to cbttrans
                    subject='BASIC SCIENCE'
                    hu=cbtold.objects.get(session=currse,term=term,exam_type=ex.exam_type,klass=selq.klass,
                        subject=subject,student=student).delete()
    

                    trans=cbttrans.objects.filter(session=student.admitted_session,
                        exam_type=ex.exam_type,
                        student=student, #or student.id 
                        subject=subject,
                        term=term)

                    count=trans.count()+1



                    transid=[]

                    for k in trans:
                            fb= k.qstcode.split('-')[0]
                            fb=int(fb)   
                            transid.append(fb)


                    qstns=tblquestion.objects.filter(term=term, 
                            exam_type=ex.exam_type, 
                            session=student.admitted_session,
                            subject=subject,
                            klass=student.admitted_class)#student.admitted_class
                        

                    myq=[]
                       
                    for q in qstns:
                            myq.append(q.id)

                    qu=[]
            
                    qu= [item for item in myq  if item not in transid]


                    if qu == []:
                          cbtcurrentquestion.objects.filter(student=student,session=currse,term=term,
                                exam_type=ex.exam_type,
                                subject=subject).delete()
                          return render_to_response('CBT/done.html')

                    uid = 0


                    uid = random.choice(qu)
                    tk=0
                        
                    tk = tblquestion.objects.get(term=q.term, 
                            exam_type=q.exam_type, 
                            session=student.admitted_session,
                            subject=subject,
                            klass=student.admitted_class,
                            id=uid)

                    gh=cbtold.objects.filter(session=currse,
                            question=tk,
                            term=term,
                            exam_type=ex.exam_type,
                            klass=student.admitted_class,
                            subject=subject,
                            student=student,
                            qstcode=tk.id).count()

                    if gh==0:
                        cbtold(session=currse,
                                question=tk,
                                term=term,
                                exam_type=ex.exam_type,
                                klass=student.admitted_class,
                                subject=subject,
                                student=student,
                                qstcode=tk.id).save()

                        n2=number+1
                        hj= cbtcurrentquestion.objects.filter(student=student,
                            term = term,
                            session=currse,
                            subject=subject,
                            exam_type=ex.exam_type,
                            number=number).update(number=n2)


                elif ty=='update':     #if i updated

                    try:
                        c='i update'

                        n2=number+1
                        subject='BASIC SCIENCE'

                        hj= cbtcurrentquestion.objects.filter(student=student,
                            term = term,
                            session=currse,
                            subject=subject,
                            exam_type=ex.exam_type,
                            number=number).update(number=n2)                     

                        qs= cbttrans.objects.get(student=student,session=currse,
                            term=term,exam_type=ex.exam_type,no=n2,subject=subject)
                        ans=qs.stu_ans

                        tk = tblquestion.objects.get(term=term, 
                        exam_type=ex.exam_type, 
                        session=currse,
                        subject=subject,
                        klass=student.admitted_class,
                        id=qs.qstcode)
                        
                    except:
                        c= 'i do well'

                        n2=number+1
                        subject='BASIC SCIENCE'

                        hj= cbtcurrentquestion.objects.filter(student=student,
                            term = term,
                            session=currse,
                            subject=subject,
                            exam_type=ex.exam_type,
                            number=number).update(number=n2) 

                        qs=cbtold.objects.get(student=student,
                            session=currse,
                            term=term,                            
                            exam_type=ex.exam_type,
                            klass=student.admitted_class,
                            subject=subject)
                        ans=''

                        tk = tblquestion.objects.get(term=term, 
                        exam_type=ex.exam_type, 
                        session=currse,
                        subject=subject,
                        klass=student.admitted_class,
                        id=qs.qstcode)
                  
                number=number+1

            else: #if i didnt chose an option
                try:
                    qs = cbttrans.objects.get(student=student,session=currse,term=term,
                        exam_type=ex.exam_type,no=number,subject=subject)
                    ans=qs.stu_ans

                except:

                    qs=cbtold.objects.get(student=student,session=currse,term=term,
                        exam_type=ex.exam_type,klass=student.admitted_class,subject=subject)
                    ans=''


                tk = tblquestion.objects.get(term=term, 
                        exam_type=ex.exam_type, 
                        session=currse,
                        subject=subject,
                        klass=student.admitted_class,
                        id=qs.qstcode)

            tk1 =tk.qstn
            opt = tbloptions.objects.filter(qstn=tk)

        

            return render_to_response('CBT/pupiltest.html',{'question':tk1,
                'school':school,
                'count':number,
                'form':student,
                'ans':ans,
                'a':ty,
                'session':currse,
                'name':student.fullname,
                'klass':student.admitted_class,
                'adm':student.admissionno,
                'options':opt,
                'term':term,
                'uid':tk.id,
                'subject':subject})
       
        else:
            return HttpResponseRedirect('/cbt/take_test/start/')
    else:
        return HttpResponseRedirect('/login/')
