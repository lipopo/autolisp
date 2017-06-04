# -*- coding: utf-8 -*-
"""
Created on Sun Jun  4 17:51:16 2017

@author: Administrator
"""

import numpy as np 
import tensorflow as tf

with tf.name_scope("init_data"):
    qmax = tf.placeholder(tf.float32,name="Qmax")
    kz = tf.placeholder(tf.float32,name="Kz")
    bod_in = tf.placeholder(tf.float32,name="BOD_IN")
    bod_out = tf.placeholder(tf.float32,name="BOD_OUT")
    
#水解酸化池
with tf.name_scope("HydrolysisAcidificationTank"):
    #水力停留时间
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
        
#竖流式沉淀池
with tf.name_scope("VerticalFlowSedimentationTank"):
    #中心管流速
    vf_v = tf.placeholder(tf.float32,name="CenterTubeFlowRate")
    #喇叭口管径
    vf_d_1 = tf.placeholder(tf.float32,name="BellMouthDiameter")
    #喇叭口流速
    vf_v_1 = tf.placeholder(tf.float32,name="BellMouthFlowRate")
    #表面负荷
    vf_q_1 = tf.placeholder(tf.float32,name="SurfaceLoad")
    #计算中心管面积
    with tf.name_scope("CalculateTheAreaOfTheCentralTube"):
        #中心管断面面积
        vf_f = qmax / vf_v
        #中心管管径
        vf_d = tf.sqrt(4 * vf_f / np.pi)
        #喇叭口至反射板得距离
        vf_h_1 = qmax / (vf_v_1 * np.pi * vf_d_1)
    #计算表面积
    with tf.name_scope("CalculateTheSurfaceArea"):
        #水体流速
        