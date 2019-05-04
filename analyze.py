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

from pyecharts import Bar,Pie,WordCloud,Line,EffectScatter,configure,Geo,Page,Timeline,Style,Funnel
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
        host='104.168.234.94'
        passwd='pjc996770483'
        db='mfw2'
        conn = MYSQLdb.connect(host=host, user='root', passwd=passwd, db=db, port=3306, charset='utf8')
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


@app.route("/month/")
def month():
    query="SELECT month,count(*) FROM strategy where year=2018 group by month"
    query2="SELECT tianshu, count(*) FROM strategy where year=2018 group by tianshu;" 
    cur=getcur()
    count=cur.execute(query)
    
    bar=Bar("2018 出行时间分布")
    
    att=['一月','二月','三月','四月','五月','六月','七月','八月','九月','十月','十一月','十二月']
    value=list()
    while count>0:
        one=cur.fetchone()
        value.append(one[1])

        count-=1

    bar.add('2018年旅游人数随月份变化图',att,value,is_label_show = True,is_random=True)
    line=Line('2018年旅游人数随月份变化图')
    line.add('2018年旅游人数随月份变化情况',att,value,is_label_show = True,is_random=True)
    
    count=cur.execute(query2)
    att={'1天':0,'2天':0,'3天':0,'4天':0,'5天':0,'6~7天':0,'8~10天':0,'11~30天':0,'30天以上':0}
    while count>0:
        one=cur.fetchone()
        if(one[0]==1):
            att['1天']+=one[1]
        elif one[0]==2:
            att['2天']+=one[1]
        elif one[0]==3:
            att['3天']+=one[1]
        elif one[0]==4:
            att['4天']+=one[1]
        elif one[0]==5:
            att['5天']+=one[1]
        elif one[0]<=7:
            att['6~7天']+=one[1]
        elif one[0]<=10:
            att['8~10天']+=one[1]
        elif one[0]<=30:
            att['11~30天']+=one[1]
        else:
            att['30天以上']+=one[1]
        count-=1
    print(att)
    attr=list(att.keys())
    value=list(att.values())

    es=Pie('出行天数',width=1300)# rose
    es.add('出行天数',attr,value,is_label_show=True,center = [25,50],radius=[30, 75],rosetype='radius')

    line2=Line('出行天数')
    line2.add('出行天数',attr,value,is_label_show = True,is_random=True)

    f=Funnel('出行天数')
    f.add("出行天数",
        attr,value,
        is_label_show=True,
    label_pos="inside",
    label_text_color="#fff",
    funnel_sort="ascending")


    return render_template('map.html', m=bar,l=line,t=es,tl=line2,c=f)


@app.route("/pay/")
def pay():

    query="SELECT pay, count(*) FROM strategy where pay!=0 group by pay"
    cur=getcur()
    count=cur.execute(query)
    
    attr={'1~100':0,'100~200':0,'200~300':0,'300~400':0,'400~500':0,'500~600':0,'600~700':0,'700~800':0,'800~900':0,'900~1000':0,'1000~1300':0,'1300~1500':0,'1500~2500':0,'2500~3000':0,'3000~3500':0,'3500~4000':0,'4000~5000':0,'5000~6000':0,'6000~10000':0,'10000以上':0}
    value=list()
    while count>0:
        one=cur.fetchone()
        if one[0]<=100:
            attr['1~100']+=one[1]
        elif one[0]<=200:
            attr['100~200']+=one[1]
        elif one[0]<=300:
            attr['200~300']+=one[1]
        elif one[0]<=400:
            attr['300~400']+=one[1]
        elif one[0]<=500:
            attr['400~500']+=one[1]
        elif one[0]<=600:
            attr['500~600']+=one[1]
        elif one[0]<=700:
            attr['600~700']+=one[1]
        elif one[0]<=800:
            attr['700~800']+=one[1]
        elif one[0]<=900:
            attr['800~900']+=one[1]
        elif one[0]<=1000:
            attr['900~1000']+=one[1]
        elif one[0]<=1300:
            attr['1000~1300']+=one[1]
        elif one[0]<=1500:
            attr['1300~1500']+=one[1]
        elif one[0]<=2500:
            attr['1500~2500']+=one[1]
        elif one[0]<=3000:
            attr['2500~3000']+=one[1]
        elif one[0]<=3500:
            attr['3000~3500']+=one[1]
        elif one[0]<=4000:
            attr['3500~4000']+=one[1]
        elif one[0]<=5000:
            attr['4000~5000']+=one[1]
        elif one[0]<=6000:
            attr['5000~6000']+=one[1]
        elif one[0]<=10000:
            attr['6000~10000']+=one[1]
        else:
            attr['10000以上']+=one[1]
        count-=1

    att=list(attr.keys())[:10]
    value=list(attr.values())[:10]
    bar=Bar("旅游花费")
    bar.add('',att,value,is_label_show = True,is_datazoom_show=True,is_random=True, mark_point=["average"])
    line=Line('旅游花费信息')
    line.add('',att,value,is_label_show = True,is_random=True, mark_point=["average"])
    es=Pie('1000元之内',width=1300)# rose
    es.add('',att,value,is_label_show=True,center = [25,50],radius=[30, 75],rosetype='radius')

    att=list(attr.keys())
    value=list(attr.values())
    barAll=Bar("总体花费情况")
    barAll.add('',att,value,is_label_show = True,is_datazoom_show=True,is_random=True)
    
    pie=Pie('',width=1000,height=700)# rose
    pie.add('',att,value,is_label_show=True)

    att=list(attr.keys())[10:]
    value=list(attr.values())[10:]
    over=Pie('',width=1200)# rose
    over.add('',att,value,is_label_show=True)


    return render_template('pay.html', m=bar,line=line,es=es,all=barAll,all2=pie,over=over)


app.run(port=80,debug=True)
