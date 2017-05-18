# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import numpy as np
import xlsxwriter
import cv2
import os
from pyautocad import Autocad,APoint

class obj:
    #不确定值 static always change just one
    dongtai = 0
    out_num_node = 0
    book = 0
    name_form = book.add_format()
    name_form.bold()
    val_form = book.add_format()
    danwei_form = book.add_format()
    danwei_form.italic()    
    def init(self,init,in_num):
        self.dongtai = init
        self.in_num = in_num
        self.my_num = self.jisuan()
        self.out_num = self.out_num()        
    def __init__(self,in_num):
        if in_num != 0:
            self.in_num = in_num
            self.my_num = self.jisuan()
            self.out_num = self.out_num()
            self.book = xlsxwriter.Workbook("./bishe/jisuan.xlsx")
    def jisuan(self):
        return 0
    def out_num(self):
        return 0
    def __add__(self,other):
        other.set_innum(self.out_num)
        return other.out_num
        
class geshan(obj):
    '''
    格栅设计要点及动态参数包含
        dongtai:进水流量、总变化系数、栅前水深、栅前流速、过栅流速、格栅倾角、栅条间隙、栅条宽度、系数、断面系数、超高、进水渠宽、栅前渠道长度、栅后渠道长度、栅渣量/m3
        my_num:间隙数、栅槽宽度、阻力系数、计算水头损失、过栅水头损失、栅后槽总高度、渐展长度、渐缩长度、总长度
    '''
    def jisuan(self):
        self.Q = obj.dongtai["Q"]
        self.kz = obj.dongtai["geshan_kz"]
        self.h0 = obj.dongtai["geshan_h_0"]
        self.v0 = obj.dongtai["geshan_v_0"]
        self.v1 = obj.dongtai["geshan_v_1"]
        self.theta = obj.dongtai["geshan_theta"]
        self.jianxi = obj.dongtai["geshan_jianxi"]
        self.shantiao = obj.dongtai["geshan_shantiao"]
        self.k = obj.dongtai["geshan_k"]
        self.betha = obj.dongtai["geshan_betha"]
        self.chagao = obj.dongtai["geshan_chaogao"]
        self.B0 = obj.dongtai["geshan_B0"]
        self.zhan_theta = obj.dongtai["geshan_jianzhan"]
        self.L0 = obj.dongtai["geshan_L0"]
        self.L01 = obj.dongtai["geshan_L1"]
        self.w0 = obj.dongtai["geshan_shanzha"]
        #计算相关数据        
        self.n = (self.Q*np.sqrt(np.sin(self.theta)))/(self.jianxi*self.h0*self.v1)
        self.B = self.shantiao*(self.n-1)+self.jianxi*self.n
        self.zulixishu = self.betha*np.power(self.shantiao/self.jianxi,4/3)
        self.jisuan_h = self.zulixishu*np.power(self.v1,2)*np.sin(self.theta)/(2*9.8)
        self.shiji_h = self.jisuan_h*self.k
        self.houcao_h = self.h0 + self.shiji_h + self.chaogao
        self.L1 = (self.B - self.B0)/(2 * np.tan(self.zhan_theta))
        self.L2 = self.L1 / 2 
        self.L = self.L1 + self.L2 + self.L0 + self.L01 + (self.h0 + self.chaogao)/np.tan(self.theta)
        self.shanzha = self.w0 * self.Q * 86400 / 1000
    def jilu(self):
        book = obj.book
        sheet = book.add_worksheet("geshan")
        data = {"geshan":[
            {"name":"项目",
             "val":"数值",
             "danwei":"单位"},
            {"name":"每日流量",
             "val":self.Q,
             "danwei":"m3/d"},
            {"name":"总变化系数",
             "val":self.kz,
             "danwei":""},
            {"name":"栅槽前渠长",
             "val":self.L0,
             "danwei":"m"},
            {"name":"栅槽后渠长",
             "val":self.L01,
             "danwei":"m"},
            {"name":"栅槽渐展角",
             "val":self.zhan_theta,
             "danwei":"弧度"},
            {"name":"栅前长度",
             "val":self.L1,
             "danwei":"m"},             
            {"name":"栅槽长度",
             "val":(self.h0 + self.chaogao)/np.tan(self.theta),
             "danwei":"m"},
            {"name":"栅后长度",
             "val":self.L2,
             "danwei":"m"},             
            {"name":"总长度",
             "val":self.L,
             "danwei":"m"},             
            {"name":"栅前水深",
             "val":self.h0,
             "danwei":"m"},                          
            {"name":"设计超高",
             "val":self.chagao,
             "danwei":"m"},             
            {"name":"总高度",
             "val":self.chagao+self.h0,
             "danwei":"m"},             
            {"name":"栅前流速",
             "val":self.v0,
             "danwei":"m/s"},             
            {"name":"过栅流速",
             "val":self.v1,
             "danwei":"m/s"},             
            {"name":"格栅倾角",
             "val":self.theta,
             "danwei":"弧度"},             
            {"name":"格栅间隙宽度",
             "val":self.jianxi,
             "danwei":"m"},             
            {"name":"格栅条数",
             "val":self.n,
             "danwei":""},             
            {"name":"栅条宽度",
             "val":self.shantiao,
             "danwei":"m"},             
            {"name":"栅槽宽度",
             "val":self.B,
             "danwei":"m"},             
            {"name":"进水渠宽",
             "val":self.B0,
             "danwei":"m"},             
            {"name":"断面Beta",
             "val":self.betha,
             "danwei":""},             
            {"name":"阻力系数",
             "val":self.zulixishu,
             "danwei":""},             
            {"name":"理论水头损失",
             "val":self.jisuan_h,
             "danwei":"m"},             
            {"name":"系数k",
             "val":self.k,
             "danwei":""},             
            {"name":"实际水头损失",
             "val":self.shiji_h,
             "danwei":"m"},             
            {"name":"栅后槽高",
             "val":self.houcao_h,
             "danwei":"m"},             
            {"name":"每日栅渣量",
             "val":self.shanzha,
             "danwei":"m3/d"},
        ]}
        col = 0
        row = 0
        for i in data["geshan"]:
            sheet.write(row,col,i["name"],obj.name_form)
            sheet.write(row,col+1,str(i["val"]),obj.val_form)
            sheet.write(row,col+2,i["danwei"],obj.danwei_form)
            row = row+1
            
    def huitu(self):
        bili = 500/self.L
        kuan = self.B*bili
        img = np.ones((int(kuan),500,3),dtype=np.float32)*255
        p = {"p0":(0,(self.B - self.B0)/2),
             "p1":(self.L0,(self.B - self.B0)/2),
             "p2":(self.L0+self.L1,0),
             "p3":(self.L0+self.L1+(self.h0 + self.chaogao)/np.tan(self.theta),0),
             "p4":(self.L-self.L01,(self.B - self.B0)/2),
             "p5":(self.L,(self.B - self.B0)/2)}
        all_p = p.values()
        
        for i in range(0,len(all_p)-1):
            cv2.line(img,(all_p[i][0]*bili,all_p[i][1]*bili),(all_p[i+1][0]*bili,all_p[i+1][1]*bili),(0,0,255),1)
        img = img[::-1]
        for i in range(0,len(all_p)-1):
            cv2.line(img,(all_p[i][0]*bili,all_p[i][1]*bili),(all_p[i+1][0]*bili,all_p[i+1][1]*bili),(0,0,255),1)
        for i in range(0,int(self.n)):
            pt0 = ( bili*p["p2"][0], bili * self.jianxi * (i+1))
            pt1 = ( bili*p["p3"][0], bili * self.shantiao * i)
            cv2.rectangle(img,pt0,pt1,(255,0,0))
        cv2.putText(img,"--->",(0,kuan),0,1,(0,255,0))
        cv2.imwrite("./bishe/geshan/shiyitu.png",img)    
    

def plotCAD(points,lines,circles,path):
    acad = Autocad(create_if_not_exists=True)
    for p,color in points:
        point = acad.model.addPoint(p)
        point.color = color
        
    for p0,p1,color,bz in lines:
        line = acad.model.addLine(p0,p1)
        line.color = color
        if bz:
            acad.model.AddDimAligned(p0,p1,APoint(0,0))

    for center,radius,color in circles:
        circle = acad.model.addCircle(center,radius)
        circle.color = color
        
    acad.doc.saveas(path)
    acad.close()
    
        
os.mkdir("./bishe")
os.mkdir("./bishe/geshan")