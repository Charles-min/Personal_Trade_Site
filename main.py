from turtle import update
from flask import Flask, flash, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Trade.sqlite3'
app.config['SECRET_KEY'] = "abcdefg anything"

db = SQLAlchemy(app)


class USER(db.Model):
    idx = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)
    userID = db.Column(db.String(30), primary_key=True, unique=True)
    userPW = db.Column(db.String(50))
    userName = db.Column(db.String(100))
    userPhoneNum = db.Column(db.String(50))
    followPara1 = db.Column(db.String(30))
    followPara2 = db.Column(db.String(30))
    followPara3 = db.Column(db.String(30))
    followPara4 = db.Column(db.String(30))
    followPara5 = db.Column(db.String(30))

    def __init__(self, userID, userPW, userName, userPhoneNum):
        self.userID = userID
        self.userPW = userPW
        self.userName = userName
        self.userPhoneNum = userPhoneNum
        # self.followPara1 = followPara1
        # self.followPara2 = followPara2
        # self.followPara3 = followPara3
        # self.followPara4 = followPara4
        # self.followPara5 = followPara5


class PRODUCT(db.Model):
    productCode = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)
    productName = db.Column(db.String(200))
    productPicture = db.Column(db.String(200))
    productPrice = db.Column(db.Integer)
    productInfo = db.Column(db.Text)
    productState = db.Column(db.String)

    def __init__(self, productName, productPicture, productPrice, productInfo):
        self.productName = productName
        self.productPicture = productPicture
        self.productPrice = productPrice
        self.productInfo = productInfo


@app.route('/')
def index():
    # 회원 가입 시 입력 값 유지를 위한 변수들
    global signUp_userID
    global signUp_userPW
    global signUp_userName
    global signUp_userPhoneNum
    global signUp_IdDuplicate

    # index.html 처음 접속하면 회원가입 시 사용했던 변수들 초기화
    signUp_userID = ''
    signUp_userPW = ''
    signUp_userName = ''
    signUp_userPhoneNum = ''
    signUp_IdDuplicate = True

    return render_template('index.html')


# 다시 회원가입 시 입력 값 기억할 변수 등장
signUp_userID = ''
signUp_userPW = ''
signUp_userName = ''
signUp_userPhoneNum = ''
signUp_IdDuplicate = True

################################################
@app.route('/add_user/', methods=['GET', 'POST'])
def add_user():
    global signUp_userID
    global signUp_userPW
    global signUp_userName
    global signUp_userPhoneNum
    global signUp_IdDuplicate

    if request.method == 'POST':
        if not request.form['userID'] or not request.form['userPW'] or not request.form['userName'] or not request.form[
            'userPhoneNum']:
            signUp_userID = request.form['userID']
            signUp_userPW = request.form['userPW']
            signUp_userName = request.form['userName']
            signUp_userPhoneNum = request.form['userPhoneNum']
            flash('There are items that require your attention.')
        elif signUp_IdDuplicate:
            signUp_userID = request.form['userID']
            signUp_userPW = request.form['userPW']
            signUp_userName = request.form['userName']
            signUp_userPhoneNum = request.form['userPhoneNum']
            flash('Validate the ID duplication.')
        elif signUp_userID != request.form['userID']:
            flash('Please double check ID again.')
            signUp_userID = request.form['userID']
            signUp_userPW = request.form['userPW']
            signUp_userName = request.form['userName']
            signUp_userPhoneNum = request.form['userPhoneNum']
        else:
            user = USER(request.form['userID'], request.form['userPW'], request.form['userName'],
                        request.form['userPhoneNum'])
            db.session.add(user)
            db.session.commit
            flash('You have successfully sign up as a member')
            # 회원가입 성공했으므로 다시 입력값 초기화
            signUp_userID = ''
            signUp_userPW = ''
            signUp_userName = ''
            signUp_userPhoneNum = ''
            signUp_IdDuplicate = True

            return redirect(url_for('index'))


@app.route('/check_idform/', methods=['GET', 'POST'])
def idDuplicateCheck():
    global signUp_userID
    global signUp_userPW
    global signUp_IdDuplicate

    signUp_userPW = request.form['userPW']

    if not request.form['signUp_userID']:
        flash('Enter the ID and then Retry the ID duplication.')
        return redirect(url_for('add_user'))

    if request.method == 'POST':

        id = USER.query.filter_by(userID=request.form['userID']).first()
        if (id):
            flash('ID already exists. You have entered other ID')

            signUp_userID = ''
            signUp_IdDuplicate = True
            return redirect(url_for('add_user'))

        else:
            flash('Use the available ID.')
            signUp_userID = request.form['userID']
            signUp_IdDuplicate = False
            return redirect(url_for('add_user'))

################################################
@app.route('/add_product', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        if not request.form['productName'] or not request.form['productPrice']:
            flash('Please enter all the fields', 'error')
        else:
            product = PRODUCT(request.form['productName'], request.form['productPicture'], request.form['productPrice'],
                              request.form['productInfo'])
            db.session.add(product)
            db.session.commit()

            flash('Record was successfully added')
            return redirect(url_for('show_product'))
    return render_template('add_product.html')


@app.route('/show_product')
def show_product():
    return render_template('show_product.html', PRODUCT=PRODUCT.query.all())


################################

@app.route('/show_user')
def show_user():
    return render_template('show_user.html', USER=USER.query.all())



##############################################
## 상품상세페이지 ## by.윤선희
#############################################
@app.route('/product_detail/<productCode>', methods=['GET', 'POST'])
def product_detail(productCode):
    update_product = PRODUCT.query.filter_by(productCode=productCode).first()
    return render_template('product_detail.html', product=update_product)


##############################################
## 구매확인페이지 ## by.윤선희
#############################################
@app.route('/buy/<productCode>', methods=['GET', 'POST'])
def buy(productCode):
    buy_product = PRODUCT.query.filter_by(productCode=productCode).first()
    buy_product.productState = "SOLD"
    db.session.commit()

    # flash('Record state was successfully updated')
    # return redirect(url_for('buy', productCode = buy_product.productCode))
    # productCode = buy_product.productCode
    # return render_template('product_detail.html', product = buy_product)

    return render_template('buy.html', product=buy_product)


##############################################
## 상품검색페이지 ## by.윤선희
#############################################
@app.route('/search_keyword/<key_search>', methods=['GET'])
def search_keyword(key_search):
    if request.method == 'GET':
        # kw = request.form.get['key_search']
        search_product = PRODUCT.query.filter_by(productName=key_search).first()
    else:
        search_product = PRODUCT.query.all()

    return render_template('search_keyword.html', product=search_product)


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
