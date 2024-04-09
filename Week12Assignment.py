# -*- coding: utf-8 -*-
"""
Created on Tue Apr  9 13:40:56 2024

@author: bentn
"""
import numpy as np
import matplotlib.pyplot as plt

dt = 1/100
time_sec = 60
time = np.arange(0, time_sec, dt)

e_a = 2
e_al = 1
e_vl = 1
e_v = .5

v_a = np.zeros(len(time))
v_al = np.zeros(len(time))
v_vl = np.zeros(len(time))
v_v = np.zeros(len(time))
v_h = np.zeros(len(time))
v_h[0] = 16
v_a[0] = 15
v_al[0] = 5
v_vl[0] = 5
v_v[0] = 59
r_ao = 1
r_a = 1
r_c = 1
r_v = 1
r_ve = 1

heart_rate_sec = 1
const = time_sec * heart_rate_sec
elast_h = np.array(([4] * int(50/heart_rate_sec) + [0] * int(50/heart_rate_sec)) * const)
alpha = np.array(([0] * int(50/heart_rate_sec) + [1] * int(50/heart_rate_sec)) * const)
beta = np.array(([1] * int(50/heart_rate_sec) + [0] * int(50/heart_rate_sec)) * const)

dvh_dt = np.zeros(len(time))
dva_dt = np.zeros(len(time))
dval_dt = np.zeros(len(time))
dvvl_dt = np.zeros(len(time))
dvv_dt = np.zeros(len(time))

for i in range(len(time) - 1):
    dvh_dt[i] = ((v_v[i] * e_v - v_h[i] * elast_h[i])/ r_ve) * alpha[i] - ((v_h[i] * elast_h[i] - v_a[i] * e_a)/ r_ao) * beta[i]
    v_h[i+1] = v_h[i] + dvh_dt[i] * dt
    
    dva_dt[i] = (v_h[i] * elast_h[i] - v_a[i] * e_a)/ r_ao * beta[i] - (v_a[i] * e_a - v_al[i] * e_al)/ r_a
    v_a[i+1] = v_a[i] + dva_dt[i] * dt 
    
    dval_dt[i] = (v_a[i] * e_a - v_al[i] * e_al)/ r_a - (v_al[i] * e_al - v_vl[i] * e_vl)/ r_c
    v_al[i+1] = v_al[i] + dval_dt[i] * dt
    
    dvvl_dt[i] = (v_al[i] * e_al - v_vl[i] * e_vl)/ r_c - (v_vl[i] * e_vl - v_v[i] * e_v)/ r_v
    v_vl[i+1] = v_vl[i] + dvvl_dt[i] * dt

    dvv_dt[i] = (v_vl[i] * e_vl - v_v[i] * e_v)/ r_v - (v_v[i] * e_v - v_h[i] * elast_h[i])/ r_ve *alpha[i]
    v_v[i+1] = v_v[i] + dvv_dt[i] * dt
    


# %%
plt.figure()
plt.plot(time[:-1], dvh_dt[:-1], label="Flow Heart")
plt.plot(time[:-1], dva_dt[:-1], label="Flow Arteries")
#plt.plot(time[:-1], dval_dt[:-1], label="Flow Arterioles")
#plt.plot(time[:-1], dvvl_dt[:-1], label="Flow Venules")
plt.plot(time[:-1], dvv_dt[:-1], label="Flow Veins")
plt.plot(time, alpha)
plt.plot(time, beta)
plt.legend()

# %%
all_volumes = np.zeros((len(time), 5))
all_volumes[:, 0] = v_h
all_volumes[:, 1] = v_a
all_volumes[:, 2] = v_al
all_volumes[:, 3] = v_vl
all_volumes[:, 4] = v_v

volume_totals = np.sum(all_volumes, axis=1)

# %%
plt.figure()
plt.plot(time[:-1], v_h[:-1], label="Volume Heart")
plt.plot(time[:-1], v_a[:-1], label="Volume Arteries")
#plt.plot(time[:-1], dval_dt[:-1], label="Flow Arterioles")
#plt.plot(time[:-1], dvvl_dt[:-1], label="Flow Venules")
plt.plot(time[:-1], v_v[:-1], label="Volume Veins")
plt.legend()


def compute_stroke_volume(v_h):
    stroke_volume = np.max(v_h[int(len(v_h)/5):]) - np.min(v_h[int(len(v_h)/5):])
    return stroke_volume

stroke_volume = compute_stroke_volume(v_h)
cardiac_output = stroke_volume * heart_rate_sec * 60



























