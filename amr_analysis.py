import yt
import numpy as np
import matplotlib.pyplot as plt
import sys

start_timestep = 1000
end_timestep = 51000
#end_timestep  = 20000
vel = np.zeros((int((end_timestep - start_timestep) / 1000),2))
vel_1 = np.zeros((int((end_timestep - start_timestep) / 1000),2))
vel_2 = np.zeros((int((end_timestep - start_timestep) / 1000),2))
# vel_3 = np.zeros((int((end_timestep - start_timestep) / 1000),2))
while (start_timestep < end_timestep):
    file_name = '../../../../../../../projects/MUELLER/ltt/Output/h2_cont0/plt/plt_h' 
    f_1 = yt.load(file_name +"{:05d}".format(start_timestep))
    f_2= yt.load(file_name + "{:05d}".format(start_timestep+1000))

    file_name_1 = '../../../../../../../projects/MUELLER/ltt/Output/h2_cont1/plt/plt_h'
    file_name_2 = '../../../../../../../projects/MUELLER/ltt/Output/h2_cont2/amr_2cont/plt_h'
    file_name_3 = ''

    f_amr1 = yt.load(file_name_1 + "{:05d}".format(start_timestep))
    f_amr1n= yt.load(file_name_1 + "{:05d}".format(start_timestep+1000))

    f_amr2 = yt.load(file_name_2 + "{:05d}".format(start_timestep))
    f_amr2n= yt.load(file_name_2 + "{:05d}".format(start_timestep+1000))
    # f_amr3 = yt.load(file_name_3 + str(start_timestep))
    # f_amr3n= yt.load(file_name_3 + str(start_timestep + 1000))


    # Get the information needed for the grid
    max_level = f_1.index.max_level 
    max_level_1 = f_amr1.index.max_level 
    max_level_2 = f_amr2.index.max_level 
    # max_level_3 = f_amr3.index.max_level 

    lo =  np.array([0.0, 0.0,0.])
    hi = np.array([15.0, 5.0,0.025])
    lo1 =  np.array([0.0, 0.0,0.])
    hi1 = np.array([15.0, 5.0,0.0125])
    lo2 =  np.array([0.0, 0.0,0.])
    hi2 = np.array([15.0, 5.0,0.00625])
    # lo3 =  np.array([0.0, 0.0,0.])
    # hi3 = np.array([15.0, 5.0,0.003125])

    dxmin = f_1.index.get_smallest_dx()
    dxmin1 = f_amr1.index.get_smallest_dx()
    dxmin2 = f_amr2.index.get_smallest_dx()
    # dxmin3 = f_amr3.index.get_smallest_dx()
    # dxmax3 = dxmin*2.0*2.0*2.0 # if amr level 3
    dxmax2 = dxmin*2.0*2.0 # if amr level 2
    dxmax1 = dxmin*2.0 # if amr level 1
    npts=np.floor((hi-lo)/dxmin)
    npts_np = np.array(npts)
    npts1=np.floor((hi-lo)/dxmin1)
    npts_np1 = np.array(npts1)
    npts2=np.floor((hi-lo)/dxmin2)
    npts_np2 = np.array(npts2)
    # npts3=np.floor((hi-lo)/dxmin3)
    # npts_np3 = np.array(npts3)
    fields_load=["density","pressure", "Temp", "x_velocity", "y_velocity", "z_velocity","Y(H2O)"]

    # Get the values on the grid at level 0 (finest level)
    first = f_1.covering_grid(level=max_level, left_edge=lo, dims=npts, fields=fields_load)
    second = f_2.covering_grid(level=max_level, left_edge=lo, dims=npts, fields=fields_load)

    amr1 = f_amr1.covering_grid(level=max_level_1, left_edge=lo1, dims=npts1, fields=fields_load)
    amr1_n = f_amr1n.covering_grid(level=max_level_1, left_edge=lo1, dims=npts1, fields=fields_load)
    amr2 = f_amr2.covering_grid(level=max_level_2, left_edge=lo2, dims=npts2, fields=fields_load)
    amr2_n = f_amr2n.covering_grid(level=max_level_2, left_edge=lo2, dims=npts2, fields=fields_load)
    # amr3 = f_amr3.covering_grid(level=max_level_3, left_edge=lo3, dims=npts3, fields=fields_load)
    # amr3_n = f_amr3n.covering_grid(level=max_level_3, left_edge=lo3, dims=npts3, fields=fields_load)

    pres_1    = np.array(first["pressure"])
    pres_2    = np.array(second["pressure"])

    pres_amr1    = np.array(amr1["pressure"])
    pres_amr1n    = np.array(amr1_n["pressure"])
    pres_amr2    = np.array(amr2["pressure"])
    pres_amr2n    = np.array(amr2_n["pressure"])
    # pres_amr3    = np.array(amr3["pressure"])
    # pres_amr3n    = np.array(amr3_n["pressure"])


    x_arr = np.linspace(lo[0], hi[0], int(npts_np[0]))
    y_arr = np.linspace(lo[1], hi[1], int(npts_np[1]))
    x_arr1 = np.linspace(lo[0], hi[0], int(npts_np1[0]))
    y_arr1 = np.linspace(lo[1], hi[1], int(npts_np1[1]))
    x_arr2 = np.linspace(lo[0], hi[0], int(npts_np2[0]))
    y_arr2 = np.linspace(lo[1], hi[1], int(npts_np2[1]))
    # x_arr3 = np.linspace(lo[0], hi[0], int(npts_np3[0]))
    # y_arr3 = np.linspace(lo[1], hi[1], int(npts_np3[1]))
    # if (start_timestep == 60000):
    #     ax = plt.figure()
    #     plt.plot(x_arr,pres_1[:,2]**10^(-1), label="No AMR")
    #     plt.plot(x_arr1,pres_amr1[:,4]**10^(-1), label="AMR 1")
    #     plt.plot(x_arr2,pres_amr1[:,6]**10^(-1), label="AMR 2")
    #     # plt.plot(x_arr3,pres_amr1[:,8]**10^(-1), label="AMR 3")
    #     ax.legend()
    #     plt.xlabel("X (cm)")
    #     plt.ylabel("Pressure (Pa)")
    #     plt.savefig(f"pres_amr.png")
    #     plt.close()

    dt = f_2.current_time - f_1.current_time
    dt_1 = f_amr1n.current_time - f_amr1.current_time
    dt_2 = f_amr2n.current_time - f_amr2.current_time
    # dt_3 = f_amr3n.current_time - f_amr3.current_time


    check = pres_1[:,0,0]
    check2 = pres_2[:,0,0]
    max_index1 = np.unravel_index(np.argmax(check), check.shape)[0]
    max_index2 = np.unravel_index(np.argmax(check2), check2.shape)[0]
    if max_index2 < max_index1:
        max_index2 = 600 + max_index2

    check_1 = pres_amr1[:,0,0]
    check2_1 = pres_amr1n[:,0,0]
    max_index1_1 = np.unravel_index(np.argmax(check_1), check_1.shape)[0]
    max_index2_1 = np.unravel_index(np.argmax(check2_1), check2_1.shape)[0]
    check_2 = pres_amr2[:,0,0]
    check2_2 = pres_amr2n[:,0,0]
    max_index1_2 = np.unravel_index(np.argmax(check_2), check_2.shape)[0]
    max_index2_2 = np.unravel_index(np.argmax(check2_2), check2_2.shape)[0]
    # check_3 = pres_amr1[:,0,0]
    # check2_3 = pres_amr1n[:,0,0]
    # max_index1_3 = np.unravel_index(np.argmax(check_3), check_3.shape)[0]
    # max_index2_3 = np.unravel_index(np.argmax(check2_3), check2_3.shape)[0]

    if max_index2_1 < max_index1_1:
        max_index2_1 = 1200 + max_index2_1
    if max_index2_2 < max_index1_2:
        max_index2_2 = 2400 + max_index2_2
    # if max_index2_3 < max_index1_3:
    #     max_index2_3 = 600 + max_index2_3

    speed = ((max_index2 - max_index1) * dxmin) / (dt) *(10**-2)
    speed_1= ((max_index2_1 - max_index1_1) * dxmin1) / (dt_1) *(10**-2)
    speed_2= ((max_index2_2 - max_index1_2) * dxmin2) / (dt_2) *(10**-2)
    # speed_3= ((max_index2_3 - max_index1_3) * dxmin3) / (dt_3) *(10**-2)
    vel[int((end_timestep - start_timestep) / 1000) - 1,:] = [f_1.current_time, speed]
    vel_1[int((end_timestep - start_timestep) / 1000) -1,:] = [f_amr1.current_time, speed_1]
    vel_2[int((end_timestep - start_timestep) / 1000) -1,:] = [f_amr2.current_time, speed_2]
    #vel_3[int((end_timestep - start_timestep) / 1000) -1,:] = [f_amr3.current_time, speed_1]
    if start_timestep == 1000:
        ax = plt.figure(figsize=(5,3))
        plt.plot(x_arr,pres_1[:,2,0]*10**(-1), label="No AMR", color="#ea5545")
        plt.plot(x_arr1,pres_amr1[:,4,0]*10**(-1), label="AMR 1", color="#27aeef")
        plt.plot(x_arr2,pres_amr2[:,6,0]*10**(-1), label="AMR 2", color="#b33dc6")
        ax.legend()
        plt.xlabel("X (cm)")
        plt.ylabel("Pressure (Pa)")
        plt.savefig(f"pres_amr.png")
        plt.close()
    start_timestep = start_timestep + 1000

ax = plt.figure()
plt.plot(vel[:,0] * 10**3,vel[:,1], label="No AMR", color="#ea5545")
plt.plot(vel_1[:,0]* 10**3,vel_1[:,1], label="AMR 1", color="#27aeef")
plt.plot(vel_2[:,0]* 10**3,vel_2[:,1], label="AMR 2", color="#b33dc6")
#plt.plot(vel_3[:,0]* 10**3,vel_3[:,1], label="AMR 1")
ax.legend()
plt.xlabel("Time (ms)")
plt.ylabel("Velocity (m/s)")
plt.savefig(f"Velocity_h2_amr.png")
plt.close()

axs = plt.figure()
colors = ["#ea5545","#27aeef","#b33dc6"]
bplot = plt.boxplot(x=[vel[:,1],vel_1[:,1], vel_2[:,1]], label=["No AMR", "AMR 1", "AMR 2"],
                 patch_artist=True, meanprops={"markeredgecolor": "black",  "markerfacecolor": "black"})
plt.grid(True, axis='y')
# fill with colors
for patch, color in zip(bplot['boxes'], colors):
    patch.set_facecolor(color)
for median in bplot['medians']:
    median.set_color('black')
plt.xticks([y + 1 for y in range(3)],labels=["No AMR", "AMR 1", "AMR 2"])
plt.xlabel('AMR Level')
plt.ylabel('Velocity (m/s)')
plt.savefig(f"Velocity_box_amr.png")
plt.close()