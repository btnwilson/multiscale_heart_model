
# -*- coding: utf-8 -*-
"""
Created on Tue Apr  9 13:40:56 2024

@author: bentn
"""
import numpy as np
import matplotlib.pyplot as plt

def compute_stroke_volume(v_h):
    stroke_volume = np.max(v_h[int(len(v_h)/3):]) - np.min(v_h[int(len(v_h)/3):])
    return stroke_volume

dt = 1/100
time_sec = 60
time = np.arange(0, time_sec, dt)

v_a = np.zeros(len(time))
v_al = np.zeros(len(time))
v_vl = np.zeros(len(time))
v_v = np.zeros(len(time))
v_h = np.zeros(len(time))
v_h[0] = 25
v_a[0] = 15
v_al[0] = 5
v_vl[0] = 5
v_v[0] = 40

e_a = lambda x: 2*x - 2*v_a[0]
e_al = lambda x: x - v_al[0]
e_vl = lambda x: x - v_vl[0]
e_v = lambda x: .5 * x - .5*v_v[0]

r_ao = 1
r_a = 1
r_c = .6
r_v = .6
r_ve = .4

stroke_volume_list = []
cardiac_output_list = []
heart_rate_list = [10,20,30,40,60,100,120,150, 200]

#percent_contract = lambda x: -0.00075 * x + .55
percent_contract = lambda x: 0.5
for j in heart_rate_list:
    
    v_a = np.zeros(len(time))
    v_al = np.zeros(len(time))
    v_vl = np.zeros(len(time))
    v_v = np.zeros(len(time))
    v_h = np.zeros(len(time))
    v_h[0] = 20
    v_a[0] = 15
    v_al[0] = 5
    v_vl[0] = 5
    v_v[0] = 40
    
    heart_rate = j
    inds_per_beat = int(100/(heart_rate/60))
    multiplier = int((time_sec * 100)/inds_per_beat)
    
    elast_h = np.array(([4] * int(inds_per_beat*percent_contract(j)) + [0] * int(inds_per_beat*(1-percent_contract(j))))*multiplier)
    alpha = np.array(([0] * int(inds_per_beat*percent_contract(j)) + [1] * int(inds_per_beat*(1-percent_contract(j))))*multiplier)
    beta = np.array(([1] * int(inds_per_beat*percent_contract(j)) + [0] * int(inds_per_beat*(1-percent_contract(j))))*multiplier)
    
    
    dvh_dt = np.zeros(len(elast_h))
    dva_dt = np.zeros(len(elast_h))
    dval_dt = np.zeros(len(elast_h))
    dvvl_dt = np.zeros(len(elast_h))
    dvv_dt = np.zeros(len(elast_h))
    
    
    for i in range(len(elast_h)-1):
        dvh_dt[i] = ((v_v[i] * e_v(v_v[i]) - v_h[i] * elast_h[i])/ r_ve) * alpha[i] - ((v_h[i] * elast_h[i] - v_a[i] * e_a(v_a[i]))/ r_ao) * beta[i]
        v_h[i+1] = v_h[i] + dvh_dt[i] * dt
        
        dva_dt[i] = (v_h[i] * elast_h[i] - v_a[i] * e_a(v_a[i]))/ r_ao * beta[i] - (v_a[i] * e_a(v_a[i]) - v_al[i] * e_al(v_al[i]))/ r_a
        v_a[i+1] = v_a[i] + dva_dt[i] * dt 
        
        dval_dt[i] = (v_a[i] * e_a(v_a[i]) - v_al[i] * e_al(v_al[i]))/ r_a - (v_al[i] * e_al(v_al[i]) - v_vl[i] * e_vl(v_vl[i]))/ r_c
        v_al[i+1] = v_al[i] + dval_dt[i] * dt
        
        dvvl_dt[i] = (v_al[i] * e_al(v_al[i]) - v_vl[i] * e_vl(v_vl[i]))/ r_c - (v_vl[i] * e_vl(v_vl[i]) - v_v[i] * e_v(v_v[i]))/ r_v
        v_vl[i+1] = v_vl[i] + dvvl_dt[i] * dt
    
        dvv_dt[i] = (v_vl[i] * e_vl(v_vl[i]) - v_v[i] * e_v(v_v[i]))/ r_v - (v_v[i] * e_v(v_v[i]) - v_h[i] * elast_h[i])/ r_ve *alpha[i]
        v_v[i+1] = v_v[i] + dvv_dt[i] * dt
        
    
    
    # %%
    
    plt.figure()
    plt.plot(time[:len(elast_h)], dvh_dt[:len(elast_h)], label="Flow Heart")
    plt.plot(time[:len(elast_h)], dva_dt[:len(elast_h)], label="Flow Arteries")
    #plt.plot(time[:-1], dval_dt[:-1], label="Flow Arterioles")
    #plt.plot(time[:-1], dvvl_dt[:-1], label="Flow Venules")
    plt.plot(time[:len(elast_h)], dvv_dt[:len(elast_h)], label="Flow Veins")
    plt.plot(time[:len(elast_h)], alpha)
    plt.plot(time[:len(elast_h)], beta)
    plt.legend()
    
    # %%
    all_volumes = np.zeros((len(elast_h), 5))
    all_volumes[:, 0] = v_h[:len(elast_h)]
    all_volumes[:, 1] = v_a[:len(elast_h)]
    all_volumes[:, 2] = v_al[:len(elast_h)]
    all_volumes[:, 3] = v_vl[:len(elast_h)]
    all_volumes[:, 4] = v_v[:len(elast_h)]
    
    volume_totals = np.sum(all_volumes, axis=1)
    
    # %%
    plt.figure()
    plt.plot(time[:len(elast_h)], v_h[:len(elast_h)], label="Volume Heart")
    plt.plot(time[:len(elast_h)], v_a[:len(elast_h)], label="Volume Arteries")
    #plt.plot(time[:-1], dval_dt[:-1], label="Flow Arterioles")
    #plt.plot(time[:-1], dvvl_dt[:-1], label="Flow Venules")
    plt.plot(time[:len(elast_h)], v_v[:len(elast_h)], label="Volume Veins")
    plt.legend()
    
    
    stroke_volume = compute_stroke_volume(v_h)
    stroke_volume_list.append(stroke_volume)

# %%
#stroke_volume_list[7] = (stroke_volume_list[8] + stroke_volume_list[6])/2
cardiac_output_list = np.array(stroke_volume_list) * np.array(heart_rate_list)
plt.figure()
plt.plot(heart_rate_list, stroke_volume_list)
plt.title("Stroke Volume vs Heart Rate")

plt.figure()
plt.plot(heart_rate_list, cardiac_output_list)
plt.title("Cardiac Output vs Heart Rate")





















