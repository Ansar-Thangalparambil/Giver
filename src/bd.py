from flask import *
import functools
from src.dbconnectionnew import *
from src.prediction import accuracy_c

app=Flask(__name__)
app.secret_key="sdfgha"

def login_required(func):
    @functools.wraps(func)
    def secure_function():
        if "lid" not in session:
            return render_template('loginindex.html')
        return func()

    return secure_function
@app.route('/')
def login():
    return render_template("loginindex.html")
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

@app.route('/login code',methods=['post'])
def login_code():
    Username=request.form["textfield"]
    Password=request.form["textfield2"]
    qry="select * from login where Username = %s and Password=%s"
    val=(Username,Password)
    res= selectone(qry,val)
    if res is None:
        return''' <script> alert ("invalid");
        window.location="/"</script>'''
    elif res['UserType']=="admin":
        session['lid']=res['Login_id']
        return''' <script> alert ("Welcome"); 
    window.location="/homeadmin"</script>'''
    elif res['UserType']== "blood_bank":
        session['lid'] = res['Login_id']
        return'''<script> alert ("Welcome");
        window.location="/homebloodbank"</script>'''
    else:
        return'''<script> alert ("Invalid");window.location="/"</script>'''
@app.route('/awareness')
@login_required
def awareness():

    qry = "SELECT * FROM `awareness program`"
    res = selectall(qry)
    print(res)

    return render_template("ABGP/add&manage awareness.html",val=res)
@app.route('/manage')
@login_required
def manage():
    qry="SELECT * FROM `tips`"
    res=selectall(qry)
    print(res)
    return render_template("ABGP/add and manage tips.html",val=res)




@app.route('/approve')
@login_required
def approve():
    qry="SELECT `blood bank`.*,`login`.UserType FROM `login` JOIN `blood bank` ON `login`.`Login_id`=`blood bank`.Login_id WHERE login.UserType='pending' or login.UserType='blood_bank' or login.UserType='reject'"
    res = selectall(qry)
    print(res)
    return render_template("ABGP/approve blodd bank.html",val=res)


@app.route('/accept_bloodbank')
@login_required
def accept_bloodbank():
    id = request.args.get('id')
    qry = "UPDATE `login` SET `UserType`='blood_bank' WHERE `Login_id`=%s"
    iud(qry,id)
    return '''<script>alert("Accepted");window.location="approve"</script>'''


@app.route('/reject_bloodbank')
@login_required
def reject_bloodbank():
    id = request.args.get('id')
    qry = "UPDATE `login` SET `UserType`='reject' WHERE `Login_id`=%s"
    iud(qry,id)
    return '''<script>alert("rejected");window.location="approve"</script>'''





@app.route('/edit')
@login_required
def edit():
    return render_template("ABGP/edit.html")

@app.route('/feedback')
@login_required
def feedback():
    return render_template("ABGP/feedback.html")

@app.route('/history')
@login_required
def history():
    return render_template("ABGP/history.html")

@app.route('/managebloodbank')
@login_required
def managebloodbank():
    qry="SELECT `blood bank`.*,`login`.`UserType` FROM `blood bank` JOIN `login` ON `blood bank`.Login_id=`login`.Login_id WHERE `login`.`UserType`='blood_bank' or `login`.`UserType`='blocked' "
    res=selectall(qry)
    return render_template("ABGP/manage blood bank.html",val=res)

@app.route('/block_bloodbank')
@login_required
def block_bloodbank():
    id = request.args.get('id')
    qry = "UPDATE `login` SET `UserType`='blocked' WHERE `Login_id`=%s"
    iud(qry,id)
    return '''<script>alert("Block");window.location="managebloodbank"</script>'''

@app.route('/unblock_bloodbank')
@login_required
def unblock_bloodbank():
    id = request.args.get('id')
    qry = "UPDATE `login` SET `UserType`='blood_bank' WHERE `Login_id`=%s"
    iud(qry,id)
    return '''<script>alert("Unblock");window.location="managebloodbank"</script>'''


@app.route('/register')
def register():
    return render_template("registerindex.html")

@app.route('/register_code',methods=['Post'])
def register_code():
    Name=request.form["textfield"]

    Place=request.form["textfield2"]
    Phone=request.form["textfield3"]
    Email = request.form["textfield4"]
    Pin=request.form["textfield5"]

    session['name'] = Name
    session['place'] = Place
    session['phone'] = Phone
    session['email'] = Email
    session['pin'] = Pin

    # Post=request.form["textfield5"]
    # Latitude = request.form["textfield8"]
    # Longitude = request.form["textfield9"]
    # Username=request.form["textfield6"]
    # Password=request.form["textfield7"]
    # qry1="INSERT INTO `login`VALUES(null,%s,%s,'pending')"
    # val1=(Username,Password)
    # id=iud(qry1,val1)
    # qry="INSERT INTO`blood bank` VALUES(NULL,%s,%s,%s,%s,%s,%s,%s,CURDATE(),%s,%s)"
    # val=(str(id),Name,Place,Post,Pin,Phone,Email,Latitude,Longitude)
    # iud(qry,val)
    return render_template("registerindex2.html")

@app.route('/register_code2', methods=['post'])
def register_code2():
    Post=request.form["textfield"]
    Latitude = request.form["textfield2"]
    Longitude = request.form["textfield3"]
    Username=request.form["textfield4"]
    Password=request.form["textfield5"]

    qry1 = "INSERT INTO `login`VALUES(null,%s,%s,'pending')"
    val1 = (Username, Password)
    id = iud(qry1, val1)
    qry = "INSERT INTO`blood bank` VALUES(NULL,%s,%s,%s,%s,%s,%s,%s,CURDATE(),%s,%s)"
    val = (str(id), session['name'], session['place'], Post, session['pin'], session['phone'], session['email'], Latitude, Longitude)
    iud(qry,val)

    return '''<script>alert("Successfully registered");window.location="/"</script>'''


@app.route('/reply')
@login_required
def reply():
    id=request.args.get('id')
    session['comp_id']=id
    return render_template("ABGP/reply.html")

@app.route('/sendreply',methods=['post'])
@login_required
def sendreply():
    reply=request.form['textfield']
    qry="UPDATE `complaint` SET reply=%s WHERE `C_id`=%s"
    val=(reply,session['comp_id'])
    iud(qry,val)
    return '''<script>alert("You have succesfully replied");window.location="/viewcomplaintreply#about"</script>'''

@app.route('/request1')
@login_required
def request1():
    return render_template("ABGP/request.html")

@app.route('/updateblooddonationstatus')
@login_required
def updateblooddonationstatus():
    return render_template("ABGP/update blood donation status.html")

@app.route('/viewcomplaintreply')
@login_required
def viewcomplaintreply():
    qry="SELECT `complaint`.*,`registration`.`Name`,Phone FROM  `registration` JOIN `complaint` ON `registration`.`Login_id`=`complaint`.`Login_id` WHERE complaint.reply='pending'"
    res=selectall(qry)
    return render_template("ABGP/view complaint reply.html",val=res)

@app.route('/viewrequestforblood')
@login_required
def viewrequestforblood():
    qry="SELECT  `registration`.*,`request`.* ,`request`.`R_id` AS reqid FROM `registration`JOIN `request`ON `registration`.`Login_id`=`request`.`Login_id` "
    res=selectall(qry)
    return render_template("ABGP/view request for blood.html",val=res)

@app.route('/viewuserhistory')
@login_required
def viewuserhistory():
    qry="SELECT * FROM `response` JOIN `registration` ON `response`.`lid`=`registration`.`Login_id` WHERE `response`.`status`='accepted'"
    res=selectall(qry)
    return render_template("ABGP/view user history.html",val=res)

@app.route('/viewfeedback')
@login_required
def viewfeedback():
    qry = "SELECT `feedback`.*,`registration`.`Name` FROM  `registration` JOIN `feedback` ON `registration`.`Login_id`=`feedback`.`Login_id`"
    res = selectall(qry)

    return render_template("ABGP/viewfeedback.html",val=res)


@app.route('/add',methods=['post'])
def add():
    return render_template("ABGP/add.html")#add tips

@app.route('/tipsinsert',methods=['post'])
@login_required
def tipsinsert():
    tip=request.form['textfield']
    details=request.form['textfield2']
    qry="INSERT INTO `tips` VALUES(NULL,%s,CURDATE(),%s)"
    val=(tip,details)
    iud(qry,val)
    return '''<script>alert("Tips added suucesfully");window.location="/manage#about"</script>'''

@app.route('/deletetips',methods=['get','post'])
@login_required
def deletetips():
    id = request.args.get('id')
    qry="DELETE FROM `tips` WHERE T_id=%s"
    iud(qry, id)
    return '''<script>alert("Succesfully deletd");window.location="/manage#about"</script>'''

@app.route('/edittips',methods=['get','post'])
@login_required
def edittips():
    id = request.args.get('id')
    session['tipid'] = id
    qry = "SELECT * FROM `tips` WHERE`T_id`=%s"
    res = selectone(qry, id)
    return render_template("ABGP/edittips.html",val=res)

@app.route('/editedtips',methods=['post'])
@login_required
def editedtips():
    tip=request.form['textfield']
    details=request.form['textfield2']
    qry="UPDATE `tips` SET `Tip`=%s,`Details`=%s WHERE T_id=%s"
    val=(tip,details,  session['tipid'])
    iud(qry,val)
    return '''<script>alert("You have Edited");window.location="/manage#about"</script>'''


@app.route('/complaint')
@login_required
def complaint():
    return render_template("ABGP/complaint.html")

@app.route('/homeadmin')
@login_required
def homeadmin():
    return render_template("ABGP/home admin.html")

@app.route('/homebloodbank')
def homebloodbank():
    return render_template("ABGP/home bloodbank.html")


@app.route('/response')
@login_required
def response():
    id=request.args.get('id')
    qry="SELECT `registration`.`Name`,`Gender`,`Phone`,`response`.* FROM `registration` JOIN `response` ON `registration`.`Login_id`=`response`.`lid` WHERE `response`.`reqid`=%s"
    res=selectall2(qry,id)
    print(res)
    return render_template("ABGP/response.html",val=res)

@app.route('/acceptrequest')
@login_required
def acceptrequest():
    id=request.args.get('id')
    print(id,"GGGGGGGGGGg")
    qry="UPDATE `response` SET `status`='accepted' WHERE `rid`=%s"
    iud(qry,(id))

    qry = "UPDATE `request` SET `units` = `units`-1 WHERE `R_id`=%s"
    iud(qry,id)

    return '''<script>alert("Succesful");window.location="/viewrequestforblood#about"</script>'''

@app.route('/rejectrequest')
@login_required
def rejectrequest():
    id=request.args.get('id')
    qry="UPDATE  `response` SET `status`='rejected' WHERE `rid`=%s"
    iud(qry,id)
    return '''<script>alert("Succesful");window.location="/viewrequestforblood"</script>'''


@app.route('/accept_blood_request')
@login_required
def accept_blood_request():
    id=request.args.get('id')
    print(id,"GGGGGGGGGGg")
    qry="UPDATE `request` SET `status`='accepted' WHERE `R_id`=%s"
    iud(qry,(id))

    return '''<script>alert("Succesful");window.location="/viewrequestforblood#about"</script>'''

@app.route('/reject_blood_request')
@login_required
def reject_blood_request():
    id=request.args.get('id')
    qry="UPDATE `request` SET `status`='rejected' WHERE `R_id`=%s"
    iud(qry,id)
    return '''<script>alert("Succesful");window.location="/viewrequestforblood"</script>'''





@app.route('/addawareness',methods=['get','post'])
@login_required
def addawareness():
    return render_template("ABGP/add awareness.html")

@app.route('/add_code',methods=['Post'])
@login_required
def add_code():
    Details=request.form["textfield1"]
    Venue=request.form["textfield2"]
    Time=request.form["textfield3"]
    Date=request.form["textfield4"]
    qry="INSERT INTO `awareness program` VALUES(NULL,%s,%s,%s,%s)"
    val=(Date,Time,Venue,Details)
    iud(qry,val)
    return '''<script>alert("You have successfully added");window.location="/awareness#about"</script>'''

@app.route('/editawareness',methods=['get','post'])
@login_required
def editawareness():
    id=request.args.get('id')
    session['awareid']=id
    qry="SELECT * FROM `awareness program` WHERE A_id=%s"
    res=selectone(qry,id)
    return render_template("ABGP/editawareness.html",val=res)


@app.route('/editawareness1',methods=['get','post'])
@login_required
def editawareness1():
    Details = request.form["textfield"]
    Venue = request.form["textfield2"]
    Time = request.form["textfield3"]
    Date = request.form["textfield4"]
    qry ="UPDATE `awareness program` SET `Date`=%s,`Time`=%s,`Venue`=%s,`Details`=%s WHERE `A_id`=%s"
    val=(Date,Time,Venue,Details,session['awareid'])
    iud(qry,val)
    return '''<script>alert("You have Edited");window.location="/awareness"</script>'''

@app.route('/deleteawareness',methods=['get','post'])
@login_required
def deleteawareness():
    id=request.args.get('id')
    qry="DELETE FROM `awareness program` WHERE A_id=%s"
    iud(qry,id)
    return '''<script>alert("Succesfully deletd");window.location="/awareness#about"</script>'''

@app.route('/predictuser')
@login_required
def predictuser():
    return render_template("ABGP/predict user.html")

@app.route('/DonationProb',methods=['post'])
@login_required
def DonationProb():
    bg=request.form['select']
    qry="SELECT * FROM `registration` WHERE `Bloodgroup`=%s"
    res=selectall2(qry,bg)

    res1=[]
    print(res,"=====================")
    for i in res:
        print(i,"===========================")
        qry="SELECT * FROM `response` WHERE `lid`=%s"
        rr=selectall2(qry,i["Login_id"])
        count=len(rr)
        print("++++",count)

        qry = "SELECT YEAR(CURDATE())-YEAR(DATE),MONTH(CURDATE())-MONTH(DATE) FROM `response` WHERE `lid`=%s ORDER BY `rid` DESC LIMIT 1"
        rrr = selectone(qry, i['Login_id'])
        print("rr+===+",rrr)
        fm=0
        try:
            fm=int(rrr[0])*12+int(rrr[1])
        except:
            pass

        qry = "SELECT YEAR(CURDATE())-YEAR(DATE),MONTH(CURDATE())-MONTH(DATE) FROM `response` WHERE `lid`=%s ORDER BY `rid` desc LIMIT 1"
        rrr = selectone(qry, i['Login_id'])
        lm=0
        try:
            lm = int(rrr[0]) * 12 + int(rrr[1])
        except:
            pass

        bc=count*400

        row=[lm,count,bc,fm]
        print(row)
        rr=accuracy_c(row)

        if str(rr)=="1":
            res1.append(i)
        print(rr,"===++===")
    return render_template("ABGP/predict user.html", val=res1)







app.run(debug=True)