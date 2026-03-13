from flask import Flask,render_template,request,redirect,session
import sqlite3
import datetime

app = Flask(__name__)
app.secret_key="secret123"


# ---------------------
# コース金额
# ---------------------

courses={
"コース1":1000,
"コース2":2000,
"コース3":3000,
"コース4":4000
}


# ---------------------
# 自动创建数据库
# ---------------------

def init_db():

    conn=sqlite3.connect("database.db")
    c=conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS records(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    course TEXT,
    base_value INTEGER,
    input_value INTEGER,
    result INTEGER,
    time TEXT
    )
    """)

    conn.commit()
    conn.close()


init_db()


# ---------------------
# 连接数据库
# ---------------------

def get_db():
    return sqlite3.connect("database.db")


# ---------------------
# 登录
# ---------------------

@app.route("/",methods=["GET","POST"])
def login():

    if request.method=="POST":

        username=request.form["username"]
        password=request.form["password"]

        if username=="123" and password=="123":
            session["user"]=username
            return redirect("/home")

    return render_template("login.html")


# ---------------------
# 主页
# ---------------------

@app.route("/home")
def home():

    if "user" not in session:
        return redirect("/")

    conn=get_db()
    c=conn.cursor()

    c.execute("SELECT * FROM records ORDER BY id DESC")
    records=c.fetchall()

    # 今日收入
    today=datetime.date.today().strftime("%Y-%m-%d")

    c.execute("SELECT SUM(result) FROM records WHERE time LIKE ?",(today+"%",))
    today_total=c.fetchone()[0]

    if today_total is None:
        today_total=0

    # 每个人统计
    c.execute("""
    SELECT name,SUM(result)
    FROM records
    GROUP BY name
    """)
    people=c.fetchall()

    conn.close()

    return render_template(
        "home.html",
        courses=courses,
        records=records,
        today_total=today_total,
        people=people
    )


# ---------------------
# 计算页面
# ---------------------

@app.route("/calc/<course>",methods=["GET","POST"])
def calc(course):

    base_value=courses[course]

    if request.method=="POST":

        name=request.form["name"]
        number=int(request.form["number"])

        result=abs(number-base_value)

        time=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        conn=get_db()
        c=conn.cursor()

        c.execute("""
        INSERT INTO records(name,course,base_value,input_value,result,time)
        VALUES(?,?,?,?,?,?)
        """,(name,course,base_value,number,result,time))

        conn.commit()
        conn.close()

        return redirect("/home")

    return render_template("calculator.html",course=course,value=base_value)


# ---------------------
# 删除记录
# ---------------------

@app.route("/delete/<int:id>")
def delete(id):

    conn=get_db()
    c=conn.cursor()

    c.execute("DELETE FROM records WHERE id=?",(id,))

    conn.commit()
    conn.close()

    return redirect("/home")


# ---------------------
# 修改课程金额
# ---------------------

@app.route("/update_course",methods=["POST"])
def update_course():

    course=request.form["course"]
    value=int(request.form["value"])

    courses[course]=value

    return redirect("/home")


# ---------------------
# 启动服务器
# ---------------------

if __name__=="__main__":
    app.run(debug=True)