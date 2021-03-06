# -*- coding: utf-8 -*-
"""
Created on Sun Jun  4 17:51:16 2017

@author: lipo
"""

import numpy as np 
import tensorflow as tf
import matplotlib.pyplot as plt
from matplotlib import cm   
from mpl_toolkits.mplot3d import Axes3D

plt.rcParams['font.sans-serif'] = ['SimHei']

sess = tf.Session()

with tf.name_scope("init_data"):
    qmax = tf.placeholder(tf.float32,name="Qmax")
    kz = tf.placeholder(tf.float32,name="Kz")
    bod_in = tf.placeholder(tf.float32,name="BOD_IN")
    bod_out = tf.placeholder(tf.float32,name="BOD_OUT")
    
#水解酸化池
with tf.name_scope("HydrolysisAcidificationTank"):
    #水力停留时间 6~8h
    hy_t = tf.placeholder(tf.float32,name="HydraulicRetentionTime")
    #有效水深
    hy_h = tf.placeholder(tf.float32,name="EffectiveWaterDepth")
    with tf.name_scope("CalculateTheVolume"):   
        #水解池的容积
        hy_V = hy_t * qmax
    with tf.name_scope("DetermineTheSize"):
        #池体直径
        hy_D = tf.sqrt((4*hy_V)/(np.pi*hy_h))
    with tf.name_scope("IncreaseTheFlowRateCheck"):
        #上升流速
        hy_v = hy_h / hy_t

hy_data = [hy_t,hy_h,hy_V,hy_D,hy_v]
hy_dcn = ["水力停留时间","有效高度","容积","池体直径","上升流速"]
#接触氧化池
with tf.name_scope("ContactOxidationTank"):
    #填料容积负荷
    co_M = tf.placeholder(tf.float32,name="PackingVolumeLoad")
    #池体有效高度
    co_h = tf.placeholder(tf.float32,name="EffectiveWaterDepth")
    #池个数
    co_num = tf.placeholder(tf.float32,name="PoolNumber")
    #格子个数
    co_f_num = tf.placeholder(tf.float32,name="TheNumberOfLattice")
    #填料层数
    co_m = tf.placeholder(tf.float32,name="TheNumberOfLayers")
    #超高
    co_h1 = tf.placeholder(tf.float32,name="HighProtection")
    #水面至填料层
    co_h2 = tf.placeholder(tf.float32,name="WaterToThePackingLayer")
    #填料间距
    co_h3 = tf.placeholder(tf.float32,name="PackingSpacing")
    #池底至填料层
    co_h4 = tf.placeholder(tf.float32,name="BottomToPackingLayer")
    #气水比
    co_qqs = tf.placeholder(tf.float32,name="GasToWaterRatio")
    with tf.name_scope("CalculateTheVolume"):
        #计算池容
        co_V = qmax*(bod_in - bod_out) / co_M
    with tf.name_scope("CalculateTheTotalPlaneArea"):
        #总平面面积
        co_F = co_V / co_h
        #单座池体面积
        co_f = co_F / co_num
        #单格池体平面面积
        co_f1 = co_f / co_f_num
    with tf.name_scope("CalculateTheDwellTime"):
        #计算停留时间
        co_t_caclu = co_V * co_h / qmax    
    with tf.name_scope("PoolTotalHeight"):
        #计算池总高
        co_H = co_h + co_h1 + co_h2 + (co_m - 1) * co_h3 + co_h4
    with tf.name_scope("CalculateTheActualDwellTime"):
        #实际停留时间
        co_t_real = co_V * (co_H - co_h1) / qmax
    with tf.name_scope("CalculateThePackingVolume"):
        #计算填料容积
        co_V_pack = co_h * co_F
    with tf.name_scope("CalculateTheAmountOfAir"):
        #计算空气量
        co_qs = co_qqs * qmax
        #单池空气量
        co_f_qs = co_qs / co_num
        #单格空气量
        co_f_m_qs = co_qs / co_f_num
co_data = [ co_M, co_V, co_h, co_F, co_num, co_f, co_f_num, co_f1,
            co_t_caclu, co_h1, co_h2, co_h3, co_m, co_h4, co_H, co_t_real,
           co_V_pack,co_qqs,co_qs,co_f_qs,co_f_m_qs]
co_dcn = ["填料容积负荷","计算池容","池体有效高度","总平面面积","池个数","单座池体面积","格子个数","单格池体平面面积",
          "计算停留时间","超高","水面至填料层", "填料间距", "填料层数", "池底至填料层","池总高","实际停留时间",
          "填料容积","气水比","空气量","单池空气量","单格空气量"]
#竖流式沉淀池
with tf.name_scope("VerticalFlowSedimentationTank"):
    #中心管流速
    vf_v_1 = tf.placeholder(tf.float32,name="CenterTubeFlowRate")
    #喇叭口管径
    vf_d_1 = tf.placeholder(tf.float32,name="BellMouthDiameter")
    #喇叭口流速
    vf_v_2 = tf.placeholder(tf.float32,name="BellMouthFlowRate")
    #表面负荷
    vf_q_1 = tf.placeholder(tf.float32,name="SurfaceLoad")
    #水力停留时间
    vf_t = tf.placeholder(tf.float32,name="HydraulicRetentionTime")
    #池体下部半径
    vf_r = tf.placeholder(tf.float32,name="TheLowerRadius")
    #池体下端倾角
    vf_alpha = tf.placeholder(tf.float32,name="VertebralAngle")
    #计算中心管面积
    with tf.name_scope("CalculateTheAreaOfTheCentralTube"):
        #中心管断面面积
        vf_f = qmax / vf_v_1
        #中心管管径
        vf_d = tf.sqrt(4 * vf_f / np.pi)
        #喇叭口至反射板得距离
        vf_h_1 = qmax / (vf_v_2 * np.pi * vf_d_1)
    #计算表面积
    with tf.name_scope("CalculateTheSurfaceArea"):
        #水体流速
        vf_v = vf_q_1 
        #池体断面面积
        vf_F = qmax / (kz * vf_v)
        #池体直径
        vf_D = tf.sqrt((vf_f + vf_F) * 4/np.pi)   
    #计算有效水深
    with tf.name_scope("CalculateEffectiveWaterDepth"):
        #池体有效高度
        vf_h = vf_v * vf_t 
        #池体锥形部分高度
        vf_h_xd = ((vf_D / 2) - vf_r)*tf.tan(vf_alpha)
    #计算出水负荷
    with tf.name_scope("CalculateTheWaterLoad"):
        #出水负荷
        vf_q1 = qmax / (np.pi * vf_D)
vf_data = [vf_v_1,vf_f,vf_d,vf_d_1,vf_v_1,vf_h_1,
           vf_q_1,vf_v,vf_F,vf_D,vf_t,vf_h,vf_r,
           vf_h_xd,vf_q1]
    
#污泥浓缩池
with tf.name_scope("SludgeThickeningTank"):
    #污泥总产量
    st_q = tf.placeholder(tf.float32,name="TotalSludgeProduction")
    #污泥固体浓度
    st_c = tf.placeholder(tf.float32,name="SludgeSolidConcentration")
    #污泥固体负荷
    st_m = tf.placeholder(tf.float32,name="SludgeSolidLoad")
    #超高
    st_h1 = tf.placeholder(tf.float32,name="HighProtection")
    #缓冲层高度
    st_h2 = tf.placeholder(tf.float32,name="BufferLayerHeight")
    #浓缩前污泥含水率
    st_p1 = tf.placeholder(tf.float32,name="ConcentrationOfSludgeBeforeConcentration")
    #浓缩后污泥含水率
    st_p2 = tf.placeholder(tf.float32,name="ConcentratedSludgeMoistureContent")   
    
    #污泥池的总面积
    with tf.name_scope("TheTotalAreaOfTheSludgePool"):
        #污泥池平面面积
        st_F = st_q * st_c / st_m
    #浓缩池直径
    with tf.name_scope("ConcentratePoolDiameter"):
        #浓缩池直径
        st_D = tf.sqrt(st_F * 4 / np.pi)
    #浓缩池工作部分的高度
    with tf.name_scope("ConcentrateTheHeightOfTheWorkingPartOfThePool"):
        #有效高度
        st_h = 7 * st_q / (24 * st_F)
    #浓缩池总高度 
    with tf.name_scope("ConcentrationPoolHeight"):
        #浓缩池总高度 
        st_H = st_h + st_h1 + st_h2
    #浓缩后污泥体积
    with tf.name_scope("ConcentratedSludgeVolume"):
        #泥浓缩后污泥的体积
        st_V2 = st_q * (1 - st_p1)/ (1 - st_p2)
st_data = [st_q,st_c,st_m,st_F,st_D,st_h,st_h1,st_h2,st_H,st_p1,st_p2,st_V2]

hy_t_o,hy_h_o = np.mgrid[6*3600:8*3600:360,1.0:5.0:0.1]
data_hy = sess.run(hy_data,{qmax:0.0289,hy_t:hy_t_o,hy_h:hy_h_o})
for j in data_hy:
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.plot_surface(hy_t_o,hy_h_o,j,cmap=cm.coolwarm)
    ax.set_xlabel('停留时间')
    ax.set_ylabel('有效高度')
    ax.set_zlabel(hy_dcn[np.where(data_hy==j)[0][0]])
    plt.savefig("C:/Users/Administrator/Desktop/Images/hy_"+hy_dcn[np.where(data_hy==j)[0][0]]+".png",dpi=500)

co_h_o,co_qqs_o  = np.mgrid[2.5:3.5:0.1,3:7:0.5]
data_co = sess.run(co_data,{qmax:0.0289,bod_in:400.0,
                            bod_out:20.0,co_M:3000.0,
                            co_h:co_h_o,co_num:2,
                            co_f_num:8,co_m:3,
                            co_h1:0.6,co_h2:0.5,
                            co_h3:0.3,co_h4:1.5,
                            co_qqs:co_qqs_o})
z = 0
for j in data_co:   
    if j.shape == co_h_o.shape:
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.plot_surface(co_h_o,co_qqs_o,j,cmap=cm.coolwarm)
        ax.set_xlabel('有效高度')
        ax.set_ylabel('气水比')
        ax.set_zlabel(co_dcn[z])
        plt.savefig("C:/Users/Administrator/Desktop/Images/co_"+co_dcn[z]+".png",dpi=500)
    z = z + 1
