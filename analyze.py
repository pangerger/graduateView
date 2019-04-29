# coding=utf8
"""
Migrate pyecharts and Flask with custom template functions.
"""
from __future__ import unicode_literals

import random
import datetime
import pymysql as MYSQLdb # 起个别名

from flask import Flask, render_template,request,send_from_directory
from flask.templating import Environment
import os.path

from pyecharts import HeatMap, Map,Bar,Pie,WordCloud,Line,EffectScatter,configure,Geo,Page,Timeline,Style,Funnel
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
    bar=Bar("top 旅游城市")#柱形 竖
    barH=Bar()# 柱形 横
    line=Line('top 旅游城市')# 折线
    es=Pie('top 旅游城市')# rose
    pie=Pie("top 旅游城市")# 饼
    #wordCloud=WordCloud(width=800,height=500)# 云词图
    #wordCloud.show_config()
    att=list()
    value=list()
    while count>0:
        one=cur.fetchone()
        att.append(one[1])
        value.append(one[3])
        #bar.add(one[1],int(one[3]))
        #bar.add_yaxis(one[1],int(one[3]))
        count=count-1

    bar.add('旅游人数',att,value,is_label_show = True,is_random=True)
    line.add('旅游人数',att,value,is_label_show=True)
    barH.add('旅游人数',att,value,is_label_show = True,label_pos = 'inside',is_convert = True,is_random=True)
    es.add('旅游人数',att,value,is_label_show=True,center = [25,50],radius=[30, 75],rosetype='radius')
    pie.add("旅游人数",att,value,is_label_show=True)

    #wordCloud.add('',att,value,word_size_range=[30,100])
    #wordCloud.add('',("Sam S Club", 10000),("Macys", 6181),word_size_range=[30,100])
    #wordCloud.show_config()
    cur.close()
    #conn.close()
    return render_template('city.html',micheal=bar,second=barH,third=pie,ford=line,fifth=es,topCityStart=start,topCityEnd=end,cityName=att)

@app.route("/geo",methods=['post','get'])
def geo():
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
    page=Page(page_title="旅游城市地理分析")
    #Geo.add_coordinate('丽江',100.22775, 26.855047)
    geo=Geo("全国主要旅游城市", "分布图",title_color="#fff", title_pos="center", width=1200, height=600, background_color='#404a59')
    geore=Geo("全国主要旅游城市", "热力图",title_color="#fff", title_pos="center", width=1200, height=600)

    att=list()
    value=list()
    while count>0:
        one=cur.fetchone()
        att.append(one[1])
        value.append(one[3])
        #bar.add(one[1],int(one[3]))
        #bar.add_yaxis(one[1],int(one[3]))
        count=count-1
# oh-----
    geo.add_coordinate('丽江',100.22775, 26.855047)
    geo.add_coordinate('乌镇',120.549822, 30.779863)
    geo.add_coordinate('西塘',120.892624, 30.944639)
    geo.add_coordinate('阳朔',110.496593, 24.778481)
    geo.add_coordinate('九寨沟',104.243841, 33.252056)
    geo.add_coordinate('凤凰古镇',114.892674, 30.40661)
    geo.add_coordinate('香格里拉',99.700836, 27.829743)
    geo.add_coordinate('泰山',117.135354, 36.192084)
    geo.add_coordinate('束河',100.225766, 26.87719)
    geo.add_coordinate('泸沽湖',101.50546, 27.431771)
    geo.add_coordinate('青海湖',100.99443, 36.896467)
    geo.add_coordinate('华山',110.089198, 34.52834)
    geo.add_coordinate('婺源',117.85,29.25)
    geo.add_coordinate('鼓浪屿',118.066102, 24.446214)

    geore.add_coordinate('丽江',100.22775, 26.855047)
    geore.add_coordinate('乌镇',120.549822, 30.779863)
    geore.add_coordinate('西塘',120.892624, 30.944639)
    geore.add_coordinate('阳朔',110.496593, 24.778481)
    geore.add_coordinate('九寨沟',104.243841, 33.252056)
    geore.add_coordinate('凤凰古镇',114.892674, 30.40661)
    geore.add_coordinate('香格里拉',99.700836, 27.829743)
    geore.add_coordinate('泰山',117.135354, 36.192084)
    geore.add_coordinate('束河',100.225766, 26.87719)
    geore.add_coordinate('泸沽湖',101.50546, 27.431771)
    geore.add_coordinate('青海湖',100.99443, 36.896467)
    geore.add_coordinate('华山',110.089198, 34.52834)
    geore.add_coordinate('婺源',117.85,29.25)
    geore.add_coordinate('鼓浪屿',118.066102, 24.446214)
    #effectScatter
    geo.add('one',att,value,maptype='china',type="effectScatter",is_random=True, effect_scale=5,
        visual_text_color= "#fff",
        is_visualmap= True)
    geore.add('',att,value,maptype='china',type="heatmap",is_random=True, effect_scale=5,
        visual_text_color= "#fff",
        is_visualmap= True)
    page.add(geo)
    page.add(geore)
    #data =[("海门", 9), ("鄂尔多斯", 12), ("招远", 12), ("舟山", 12), ("齐齐哈尔", 14), ("盐城", 15)]
    #geo =Geo("全国主要城市空气质量", "data from pm2.5",title_color="#fff", title_pos="center", width=1200, height=600, background_color='#404a59')
    #attr, value =geo.cast(data)
    #geo.add("", attr, value, type="effectScatter",maptype="china", is_random=True, effect_scale=5)

    page.render('geo.html')
    root = os.path.join(os.path.dirname(os.path.abspath(__file__)))#html是个文件夹
    cur.close()
    return send_from_directory(root,'geo.html')

@app.route("/cloud",methods=['post','get'])
def cloud():
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
    
    att=list()
    value=list()
    while count>0:
        one=cur.fetchone()
        att.append(one[1])
        value.append(one[3])
        #bar.add(one[1],int(one[3]))
        #bar.add_yaxis(one[1],int(one[3]))
        count=count-1
    wordCloud=WordCloud(width=1000,height=600,page_title="云词图分析")
    wordCloud.add("热门城市云词图分析",att,value,word_size_range=[20,100],shape='apple')
    wordCloud.render('cloud.html')
    root = os.path.join(os.path.dirname(os.path.abspath(__file__)))#html是个文件夹
    cur.close()
    return send_from_directory(root,'cloud.html')

@app.route("/top3",methods=['post','get'])
def top3():
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
    cnt=count
    t=Timeline("热门城市旅游top3景点",timeline_bottom=0)
    t2=Timeline("热门城市旅游top3景点",timeline_bottom=0)
    
    '''
    pieAll=Pie("top3景点")
    style = Style()
    pie_style = style.add(
    label_pos="center",
    is_label_show=True,
    label_text_color=None
    )
    '''
    page=Page(page_title="top3景点分析")
    pie=Pie("本市top3旅游景点")
    

    cityName=list()
    att=list()
    value=[39,33,28]
    while count>0:
        one=cur.fetchone()
        cityName.append(one[1])
        att.append(one[6])
        att.append(one[8])
        att.append(one[10])
        count=count-1
    i=0
    for j in range(cnt):
        pie=Pie("本市top3旅游景点")
        funnel=Funnel("top3景点")
        pie.add(cityName[j],[att[i],att[i+1],att[i+2]],value,center = [25,50],radius=[30, 75],rosetype='radius')
        t.add(pie,cityName[j])
        funnel.add("",[att[i],att[i+1],att[i+2]],value,is_label_show=True)
        t2.add(funnel,cityName[j])
        i+=3
    # label_pos="inside",
    # label_text_color="#fff",)
        #pieAll.add("",[att[i],att[i+1],att[i+2]],[39,33,28],center=[10, 30], radius=[18, 24], **pie_style)
    #pie.add('旅游人数',['a','b'],[3,5],center = [25,50],radius=[30, 75],rosetype='radius')

    #t.render('top3.html')
    root = os.path.join(os.path.dirname(os.path.abspath(__file__)))#html是个文件夹
    cur.close()
    page.add(t)
    page.add(t2)
    page.render('top3.html')
    #return render_template('map.html', m=page)
    return send_from_directory(root,'top3.html')

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
