# coding=utf8
"""
Migrate pyecharts and Flask with custom template functions.
"""
from __future__ import unicode_literals

import random
import datetime
import pymysql as MYSQLdb # 起个别名

from flask import Flask, render_template,request
from flask.templating import Environment

from pyecharts import HeatMap, Map,Bar,Page
from pyecharts.engine import ECHAERTS_TEMPLATE_FUNCTIONS
from pyecharts.conf import PyEchartsConfig


# ----- Adapter ---------
class FlaskEchartsEnvironment(Environment):
    def __init__(self, *args, **kwargs):
        super(FlaskEchartsEnvironment, self).__init__(*args, **kwargs)
        self.pyecharts_config = PyEchartsConfig(jshost='/static/js')
        self.globals.update(ECHAERTS_TEMPLATE_FUNCTIONS)


# ---User Code ----

class MyFlask(Flask):
    jinja_environment = FlaskEchartsEnvironment


# connect to mysql
def getcur():
    try:
        host='localhost'
        passwd='root'
        conn = MYSQLdb.connect(host=host, user='root', passwd=passwd, db='mfw', port=3306, charset='utf8')
        cur = conn.cursor()
        return cur
        #cur_update = conn.cursor() #这个游标用于更新
        #count = cur.execute(url_query)# 执行查询操作
    except MYSQLdb.Error as e:
        print(e.args)

# close to mysql
# def removecur(conn,cur):
#     conn.close()
#     cur.close()

app = MyFlask(__name__)

@app.route("/hi")
@app.route("/")
def index():
    return render_template('index.html')

# city in top!
@app.route("/top",methods=['post','get'])
def top():
    try:
        topCityStart=request.form['topCityStart']
        topCityEnd=request.form['topCityEnd']
    except Exception as e:
        print(e.args)
        topCityStart='1'
        topCityEnd='10'
    start=topCityStart
    end=topCityEnd
    x=int(topCityEnd)
    y=int(topCityStart)-1
    z=x-y
    topCityStart=str(y)
    topCityEnd=str(z)
    #topCityEnd=str(z)
    
    query="SELECT * FROM city order by nums desc limit "+topCityStart+","+topCityEnd
    
    cur=getcur()
    count=cur.execute(query)
    #count=int(count)
    #pan=Page()
    bar=Bar("top 旅游城市")
    barH=Bar()
    att=list()
    value=list()
    while count>0:
        one=cur.fetchone()
        att.append(one[1])
        value.append(one[3])
        #bar.add(one[1],int(one[3]))
        #bar.add_yaxis(one[1],int(one[3]))
        count=count-1

    bar.add('出行人数',att,value,is_label_show = True)
    
    barH.add('出行人数',att,value,is_label_show = True,label_pos = 'inside',is_convert = True)

    #cur.close()
    #conn.close()
    return render_template('city.html',micheal=bar,second=barH,topCityStart=start,topCityEnd=end,cityName=att)


@app.route("/heatmap/")
def heatmap():
    hm = create_heatmap()
    return render_template('heatmap.html', m=hm)


def create_heatmap():
    begin = datetime.date(2017, 1, 1)
    end = datetime.date(2017, 12, 31)
    data = [[str(begin + datetime.timedelta(days=i)),
             random.randint(1000, 25000)] for i in
            range((end - begin).days + 1)]
    heatmap = HeatMap("日历热力图示例", "某人 2017 年微信步数情况", width=1100)
    heatmap.add("", data, is_calendar_heatmap=True,
                visual_text_color='#000', visual_range_text=['', ''],
                visual_range=[1000, 25000], calendar_cell_size=['auto', 30],
                is_visualmap=True, calendar_date_range="2017",
                visual_orient="horizontal", visual_pos="center",
                visual_top="80%", is_piecewise=True)
    return heatmap







@app.route('/fujian/')
def fujian():
    value = [20, 190, 253, 77, 65]
    attr = ['福州市', '厦门市', '南平市', '泉州市', '三明市']
    map = Map("福建地图示例", width='100%', height=600)
    map.add("", attr, value, maptype='福建', is_visualmap=True,
            visual_text_color='#000')
    return render_template('fujian_map.html', m=map)

@app.route('/bar/')
def bar():
    bar = Bar()
    bar.add('格式化',["atf_tb1","shop"],[10,50])
    bar.add("范围", ["shop"], [120])
    return render_template('heatmap.html', m=bar)


app.run(port=5000,debug=True)
