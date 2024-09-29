from flask import *
from werkzeug.utils import secure_filename

from src.dbconnectionnew import *
app=Flask(__name__)
import smtplib
from src.prediction import accuracy_c
from email.mime.text import MIMEText
from flask_mail import Mail
import time, datetime
from encodings.base64_codec import base64_decode
import base64
mail=Mail(app)
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'giverblooddonation@gmail.com'
app.config['MAIL_PASSWORD'] = 'ebhbaefzjplccnjd'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
@app.route('/login',methods=['post'])
def login():
    Username=request.form["uname"]
    Password=request.form["passwd"]
    qry="select * from login where Username = %s and Password=%s and UserType='user' "
    val=(Username,Password)
    res= selectone(qry,val)
    print(res)
    if res is None:
        return jsonify(status="no")
    else:
        return jsonify(status="yes",lid=res['Login_id'])

@app.route('/register',methods=["post"])
def register():
    print(request.form)
    Name=request.form["Name"]
    Gender=request.form["Gender"]
    Bloodgroup=request.form["bg"]
    Email=request.form["E-mail"]
    Contact=request.form["Contact"]
    Place=request.form["Place"]
    Post=request.form["Post"]
    Pin=request.form["Pin"]
    profile=request.files['pic']

    fname=secure_filename(profile.filename)
    profile.save('static/uploads/' + fname)

    Username=request.form["Username"]
    Password=request.form["Password"]
    DOB=request.form["DOB"]

    qr= "INSERT INTO `login` VALUES(null,%s,%s,'user')"
    va=(Username,Password)
    id=iud(qr,va)

    qry="INSERT INTO `registration` VALUES(null,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,'0','0',%s)"
    val=(str(id),Name,Gender,DOB,Bloodgroup,Pin,Email,Contact,Place,Post,fname)
    iud(qry,val)
    return jsonify(status="ok")


@app.route('/viewothersrequest', methods=["post"])
def viewothersrequest():
    lid = request.form['lid']
    qry = "SELECT `registration`.`Name`,`blood bank`.`Name` AS bname,`request`.* FROM `request` JOIN `registration` ON `request`.`Login_id`=`registration`.`Login_id` JOIN `blood bank` ON `request`.`bbid`=`blood bank`.`Login_id` WHERE `request`.`status`='accepted' AND `request`.Login_id!=%s AND `request`.`Blood_Group`= (SELECT `registration`.`Bloodgroup` FROM `registration` WHERE `registration`.`Login_id`=%s)"
    res = selectall2(qry,(lid,lid))
    print("====",res)
    return jsonify(res)


@app.route('/sendrequest',methods=["post"])
def sendrequest():

    print(request.form)

    L_id=request.form["lid"]
    Bloodgroup=request.form["bld_grp"]

    Bloodbankid=request.form["bbid"]
    Units=request.form["Units"]

    date = request.form['Date']


    qry="INSERT INTO `request` VALUES(null,%s,%s,%s,%s,%s,%s)"
    val=(L_id,Bloodgroup,date,Bloodbankid,Units,"pending")
    iud(qry,val)
    return jsonify(status="success")

@app.route('/viewrequest',methods=["post"])
def viewrequest():
    L_id = request.form["lid"]
    qry="SELECT `request`.*,`blood bank`.Name FROM `request` JOIN `blood bank` ON `request`.bbid=`blood bank`.Login_id WHERE `request`.`Login_id`=%s "
    val = (L_id)
    res=selectall2(qry,val)
    print(res)
    return jsonify(res)

@app.route('/donateblood',methods=['post'])
def donateblood():
    Requestid=request.form["reqid"]
    Loginid=request.form["lid"]
    qry="INSERT INTO `response` VALUES(%s,%s,curdate(),%s)"
    val=(Requestid,Loginid,"pending")
    iud(qry,val)
    return jsonify(status="success")

@app.route('/history',methods=['post'])
def history():
    Loginid=request.form["lid"]
    qry="SELECT `blood bank`.`Name`,`request`.*,`response`.* FROM `blood bank` JOIN `response` ON `response`.`bbid`=`blood bank`.`Login_id` JOIN `request` ON `request`.`R_id`=`response`.`reqid` WHERE `response`.`lid`=%s"
    val=(Loginid)
    res=selectall2(qry,val)

    return jsonify(res)

@app.route('/viewresponses', methods=['post'])
def viewresponses():
    Rid =request.form["reqid"]
    qry = "SELECT  `registration`.`Name`,`Email`,`Phone` FROM `response` JOIN `registration` ON `response`.`lid`=`registration`.`Login_id` WHERE `response`.`reqid`=%s"
    res=selectall2(qry,Rid)
    return jsonify(res)






#
# @app.route('/viewdonors',methods=['post'])
# def viewdonors():
#     Requestid = request.form["reqid"]
#     Loginid = request.form["lid"]
#     Date = request.form["date"]
#     Status = request.form["status"]
#
#     qry="SELECT * FROM `response`"
#     val = (Requestid, Loginid, Date, Status)
#     iud(qry,val)
#     return jsonify(status="success")



@app.route('/sendcomplaintviewreply',methods=['post'])
def sendcomplaintviewreply():
    Loginid=request.form["lid"]
    Complaint=request.form["complaint"]

    qry = "INSERT INTO `complaint` VALUES(null,%s,%s,curdate(),'pending')"
    val = (Loginid,Complaint)

    iud(qry, val)
    return jsonify(status="success")


@app.route('/sendfeedback',methods=["post"])
def sendfeedback():
    Loginid=request.form["lid"]
    Feedback=request.form["Feedback"]
    qry="INSERT INTO `feedback`VALUES(null,%s,%s,curdate())"
    val=(Loginid,Feedback)
    iud(qry,val)
    return jsonify(status="success")


@app.route('/viewtips',methods=['post'])
def viewtips():

    qry="SELECT * FROM `tips`"
    res=selectall(qry)
    return jsonify(res)


@app.route('/view_blood_banks',methods=['post'])
def view_blood_banks():

    qry="SELECT * FROM `blood bank`"
    res=selectall(qry)
    return jsonify(res)


@app.route('/view_complaint_and_reply',methods=['post'])
def view_complaint_and_reply():
    id = request.form['lid']
    qry="SELECT * FROM complaint where Login_id=%s"
    res=selectall2(qry,id)
    return jsonify(res)


@app.route('/and_viewprofile', methods=['post'])
def and_viewprofile():
    id = request.form['lid']
    qry="SELECT * FROM `registration` WHERE `Login_id`=%s"
    res=selectone(qry,id)
    print(res)
    return jsonify(status="ok",data=res)




@app.route('/and_editprofile', methods=['post'])
def profile():
    print(request.form)
    print(request.files)
    lid = request.form['lid']
    Name = request.form["Name"]
    Email = request.form["Email"]
    Contact = request.form["Phone"]
    Place = request.form["Place"]
    Post = request.form["Post"]
    Pin = request.form["Pin"]

    try:
        im = request.form['pic']
        timestr = time.strftime("%Y%m%d-%H%M%S")
        print(timestr)
        a = base64.b64decode(im)
        fh = open("static/uploads/" + timestr + ".jpg", "wb")
        path = timestr + ".jpg"
        fh.write(a)
        fh.close()

        qry = "UPDATE `registration` SET `Name`=%s,`Pin`=%s,`Email`=%s,`Phone`=%s,`Place`=%s,`Post`=%s,Image=%s WHERE `Login_id`=%s"
        val = (Name,Pin,Email,Contact,Place,Post,path,lid)
        iud(qry,val)
        return jsonify({"status": "ok"})
    except:
        lid = request.form['lid']
        Name = request.form["Name"]
        Email = request.form["Email"]
        Contact = request.form["Phone"]
        Place = request.form["Place"]
        Post = request.form["Post"]
        Pin = request.form["Pin"]
        qry2= "UPDATE `registration` SET `Name`=%s,`Pin`=%s,`Email`=%s,`Phone`=%s,`Place`=%s,`Post`=%s WHERE `Login_id`=%s"
        val2 = (Name, Pin, Email, Contact, Place, Post, lid)
        iud(qry2, val2)
        return jsonify({"status": "ok"})




    # timestr = time.strftime("%Y%m%d-%H%M%S")
    # print(timestr)
    # a = base64.b64decode(image)
    # fh = open("static/Reg_photos/" + timestr + ".jpg", "wb")
    # path = "/static/Reg_photos/" + timestr + ".jpg"
    # fh.write(a)
    # fh.close()

    # try:
    #     lid = request.form['lid']
    #     Name = request.form["Name"]
    #
    #     Email = request.form["Email"]
    #     Contact = request.form["Phone"]
    #     Place = request.form["Place"]
    #     Post = request.form["Post"]
    #     Pin = request.form["Pin"]
    #     im = request.files['pic']
    #     fname=secure_filename(im.filename)
    #     im.save('static/uploads/' + fname)
    #
    #     qry = "UPDATE `registration` SET `Name`=%s,`Pin`=%s,`Email`=%s,`Phone`=%s,`Place`=%s,`Post`=%s,Image=%s WHERE `Login_id`=%s"
    #     val = (Name,Pin,Email,Contact,Place,Post,fname,lid)
    #     iud(qry,val)
    #     return jsonify({"status": "ok"})
    #
    # except Exception as e:
    #     lid = request.form['lid']
    #     Name = request.form["Name"]
    #     Email = request.form["Email"]
    #     Contact = request.form["Phone"]
    #     Place = request.form["Place"]
    #     Post = request.form["Post"]
    #     Pin = request.form["Pin"]
    #     qry2= "UPDATE `registration` SET `Name`=%s,`Pin`=%s,`Email`=%s,`Phone`=%s,`Place`=%s,`Post`=%s WHERE `Login_id`=%s"
    #     val2 = (Name, Pin, Email, Contact, Place, Post, lid)
    #     iud(qry2, val2)
    #     return jsonify({"status": "ok"})


@app.route('/forgotpassword',methods=['post'])
def forgotpassword():
    un=request.form['Username']
    email=request.form['Email']
    val=(un,email)
    qry="SELECT `login`.`Password`,`registration`.`Email` FROM `registration` JOIN `login` ON `login`.`Login_id`=`registration`.`Login_id` WHERE `login`.`Username`=%s AND `registration`.`Email`=%s";
    s=selectone(qry,val)
    print(s)
    if s is None:
        return jsonify({'task': 'invalid email'})
    else:
        try:
            gmail = smtplib.SMTP('smtp.gmail.com', 587)
            gmail.ehlo()
            gmail.starttls()
            gmail.login('giverblooddonation@gmail.com', 'ebhbaefzjplccnjd')
            print("ok 1")
        except Exception as e:
            print("Couldn't setup email!!" + str(e))
        msg = MIMEText("Your password is : " + str(s['Password']))
        print(msg)
        msg['Subject'] = 'Giver password'
        msg['To'] = email
        msg['From'] = 'giverblooddonation@gmail.com'
        print("ok 2")
        try:
            gmail.send_message(msg)
            print("ok 3")
        except Exception as e:
            print("COULDN'T SEND EMAIL", str(e))
        return jsonify({"status": "yes"})

@app.route('/awarenessnotification',methods=['post'])
def awarenessnotification():
    qry="SELECT * FROM `awareness program` "
    res=selectall(qry)
    print(res)
    return jsonify(res)

@app.route('/DonationProb',methods=['post'])
def DonationProb():
    bg=request.form['blood_group']
    print(bg)
    qry="SELECT * FROM `registration` WHERE `Bloodgroup`=%s"
    res=selectall2(qry,bg)
    res1=[]
    print(res,"=====================")
    for i in res:
        print(i,"===========================")
        qry="SELECT * FROM `response` WHERE `lid`=%s"
        rr=selectall2(qry,i['Login_id'])
        count=len(rr)
        qry = "SELECT YEAR(CURDATE())-YEAR(DATE),MONTH(CURDATE())-MONTH(DATE) FROM `response` WHERE `lid`=%s ORDER BY `rid` DESC LIMIT 1"
        rrr = selectone(qry, i['Login_id'])
        fm=0
        try:
            fm=int(rrr[0])*12+int(rrr[1])
        except:
            pass
        qry = "SELECT YEAR(CURDATE())-YEAR(DATE),MONTH(CURDATE())-MONTH(DATE) FROM `response` WHERE `lid`=%s ORDER BY `rid` LIMIT 1"
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
        print(rr)
    return jsonify(res1)

@app.route('/update_user_location', methods=['post'])
def update_user_location():
    print(request.form)
    lid = request.form['id']
    lati = request.form['lati']
    longi = request.form['logi']

    qry = "UPDATE `registration` SET `Latitude`=%s,`Longitude`=%s WHERE `Login_id`=%s"
    iud(qry,(lati,longi,lid))

    return jsonify({"task":"valid"})


@app.route('/accept_request', methods=['post'])
def accept_request():
    req_id = request.form['id']
    lid = request.form['lid']

    qry = "INSERT INTO `response` VALUES(NULL,%s,%s,CURDATE(),'pending')"
    iud(qry,(req_id,lid))

    return jsonify({"task":"success"})


@app.route('/complete_request', methods=['post'])
def complete_request():
    req_id = request.form['id']

    qry = "UPDATE `request` SET `status`='completed' WHERE `R_id`=%s"
    iud(qry,req_id)

    return jsonify({"task":"success"})
# @app.route('/DonationProb',methods=['post'])
# def DonationProb():DonationProb
#     bg=request.form['blood_group']
#     qry="SELECT * FROM `registration` WHERE `Bloodgroup`=%s"
#     res=selectall2(qry,bg)
#
#     res1=[]
#     print(res,"=====================")
#     for i in res:
#         print(i,"===========================")
#         qry="SELECT * FROM `response` WHERE `lid`=%s"
#         rr=selectall2(qry,i["Login_id"])
#         count=len(rr)
#         print("++++",count)
#
#         qry = "SELECT YEAR(CURDATE())-YEAR(DATE),MONTH(CURDATE())-MONTH(DATE) FROM `response` WHERE `lid`=%s ORDER BY `rid` DESC LIMIT 1"
#         rrr = selectone(qry, i['Login_id'])
#         print("rr+===+",rrr)
#         fm=0
#         try:
#             fm=int(rrr[0])*12+int(rrr[1])
#         except:
#             pass
#
#         qry = "SELECT YEAR(CURDATE())-YEAR(DATE),MONTH(CURDATE())-MONTH(DATE) FROM `response` WHERE `lid`=%s ORDER BY `rid` desc LIMIT 1"
#         rrr = selectone(qry, i['Login_id'])
#         lm=0
#         try:
#             lm = int(rrr[0]) * 12 + int(rrr[1])
#         except:
#             pass
#
#         bc=count*400
#
#         row=[lm,count,bc,fm]
#         print(row)
#         rr=accuracy_c(row)
#
#         if str(rr)=="1":
#             res1.append(i)
#         print(rr,"===++===")
#     return jsonify(res1)


app.run(host="0.0.0.0",port=5000)




















