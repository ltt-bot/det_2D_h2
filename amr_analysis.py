import yt
import numpy as np
import matplotlib.pyplot as plt
import sys

#plt.rcParams['text.usetex'] = True

colors = ["#1D4DED", "#EC8321","#14B114","#8D3FBE","#FACF0C","#6B7C8A"]
start_timestep = 1000
start = 1000
diff = 1000
end_timestep = 51000
stab = 0
len_ar = int((end_timestep - start_timestep) / diff)
vel = np.array([np.zeros((len_ar,2)),np.zeros((len_ar,2)),np.zeros((len_ar,2))])
mdots = np.array([np.zeros((len_ar,2)),np.zeros((len_ar,2)),np.zeros((len_ar,2))])
pthrusts = np.array([np.zeros((len_ar,2)),np.zeros((len_ar,2)),np.zeros((len_ar,2))])
mthrusts = np.array([np.zeros((len_ar,2)),np.zeros((len_ar,2)),np.zeros((len_ar,2))])
thrusts = np.array([np.zeros((len_ar,2)),np.zeros((len_ar,2)),np.zeros((len_ar,2))])
isps = np.array([np.zeros((len_ar,2)),np.zeros((len_ar,2)),np.zeros((len_ar,2))])
fisps = np.array([np.zeros((len_ar,2)),np.zeros((len_ar,2)),np.zeros((len_ar,2))])
# vel_3 = np.zeros((int((end_timestep - start_timestep) / 1000),2))
file_names = ['../../../../../../../projects/MUELLER/ltt/Output/h2_cont0/plt/plt_h' ,
             '../../../../../../../projects/MUELLER/ltt/Output/h2_cont1/plt/plt_h',
             '../../../../../../../projects/MUELLER/ltt/Output/h2_cont2/amr_2cont/plt_h']
while (start_timestep < end_timestep):
    for i in range(3):
        file_name = file_names[i]
        f_1 = yt.load(file_name +"{:05d}".format(start_timestep))
        f_2= yt.load(file_name + "{:05d}".format(start_timestep+diff))

        # Get the information needed for the grid
        max_level = f_1.index.max_level 
        # max_level_3 = f_amr3.index.max_level 

        lo =  np.array([0.0, 0.0,0.])
        if i >0:
            dx_ = 0.025/(2*i)
        else:
            dx_ = 0.025
        hi = np.array([15.0, 5.0,dx_])

        dxmin = f_1.index.get_smallest_dx()

        npts=np.floor((hi-lo)/dxmin)
        npts_np = np.array(npts)
        fields_load=["density","pressure", "Temp", "x_velocity", "y_velocity", "z_velocity","Y(H2O)","Y(H2)","Y(N2)", "Y(O2)"]

        # Get the values on the grid at level 0 (finest level)
        first = f_1.covering_grid(level=max_level, left_edge=lo, dims=npts, fields=fields_load)
        second = f_2.covering_grid(level=max_level, left_edge=lo, dims=npts, fields=fields_load)

        pres_1    = np.array(first["pressure"])
        pres_2    = np.array(second["pressure"])

        dens = np.array(first["density"])
        y_vel = np.array(first["y_velocity"])
        h20 = np.array(first["Y(H2O)"])
        h2 = np.array(first["Y(H2)"])
        n2 = np.array(first["Y(N2)"])
        o2 = np.array(first["Y(O2)"])
        if i == 0:
            mdot = np.trapezoid((dens[:,199,0] * y_vel[:,199,0]), dx=dx_) * 10**(-1)
            mthrust = np.trapezoid(dens[:,199,0] * (y_vel[:,199,0]**2), dx=dx_)
            pthrust = np.trapezoid(pres_1[:,199,0] - 1013250, dx=dx_)
        else:
            mdot = np.trapezoid((dens[:,200*(2*i) - 1,0] * y_vel[:,200*(2*i) - 1,0]), dx=dx_) * 10**(-1)
            mthrust = np.trapezoid(dens[:,200*(2*i) - 1,0] * (y_vel[:,200*(2*i) - 1,0]**2), dx=dx_)
            pthrust = np.trapezoid(pres_1[:,200*(2*i) - 1,0] - 1013250, dx=dx_)
        thrust = pthrust + mthrust
        mdot_h2 = np.trapezoid((dens[:,0,0] * h2[:,0,0] * y_vel[:,0,0]), dx=dx_)
        mdot_air = np.trapezoid((dens[:,0,0] * (n2[:,0,0] + o2[:,0,0]) * y_vel[:,0,0]), dx=dx_)
        isp = thrust/(mdot_h2 * 980.665)
        fisp = thrust/(mdot_air)


        x_arr = np.linspace(lo[0], hi[0], int(npts_np[0]))
        y_arr = np.linspace(lo[1], hi[1], int(npts_np[1]))

        dt = f_2.current_time - f_1.current_time


        check = pres_1[:,0,0]
        check2 = pres_2[:,0,0]
        max_index1 = np.unravel_index(np.argmax(check), check.shape)[0]
        max_index2 = np.unravel_index(np.argmax(check2), check2.shape)[0]
        if max_index2 < max_index1 and i == 0:
            max_index2 = 600 + max_index2
        elif  max_index2 < max_index1:
            max_index2 = 600 * (i*2) + max_index2
        
        if f_1.current_time > 0.4 * 10**(-3) and stab == 0:
            stab = int((start_timestep - start) / diff)

        speed = ((max_index2 - max_index1) * dxmin) / (dt) *(10**-2)
        vel[i,int((start_timestep - start) / diff),:] = [f_1.current_time, speed]
        mdots[i,int((start_timestep - start) / diff),:] = [f_1.current_time, mdot]
        thrusts[i,int((start_timestep - start) / diff),:] = [f_1.current_time, thrust* 10**(-6)]
        pthrusts[i,int((start_timestep - start) / diff),:] = [f_1.current_time, pthrust* 10**(-6)]
        mthrusts[i,int((start_timestep - start) / diff),:] = [f_1.current_time, mthrust* 10**(-6)]
        isps[i,int((start_timestep - start) / diff),:] = [f_1.current_time, isp]
        fisps[i,int((start_timestep - start) / diff),:] = [f_1.current_time, fisp* 10**(-6)]


    start_timestep = start_timestep + diff
# ax = plt.figure(dpi=1200)
# plt.plot(vel[:,0] * 10**3,vel[:,1], label="No AMR", color="#ea5545",lw=1.5)
# plt.plot(vel_1[:,0]* 10**3,vel_1[:,1], label="AMR 1", color="#27aeef",lw=1.5)
# plt.plot(vel_2[:,0]* 10**3,vel_2[:,1], label="AMR 2", color="#b33dc6",lw=1.5)
# # plt.plot(vel_3[:,0]* 10**3,vel_3[:,1], label="AMR 1")
# ax.legend()
# plt.grid()
# plt.xlabel("Time (ms)")
# plt.ylabel("Velocity (m/s)")
# plt.savefig(f"Velocity_h2_amr.png")
# plt.close()

# axs = plt.figure(dpi=1200)
# bplot = plt.boxplot(x=[vel[stab:,1],vel_1[stab:,1], vel_2[stab:,1]], label=["No AMR", "AMR 1", "AMR 2"],
#                  patch_artist=True, meanprops={"markeredgecolor": "black",  "markerfacecolor": "black"})
# plt.grid(True, axis='y')
# # fill with colors
# for patch, color in zip(bplot['boxes'], colors[0:2]):
#     patch.set_facecolor(color)
# for median in bplot['medians']:
#     median.set_color('black')
# plt.xticks([y + 1 for y in range(3)],labels=["No AMR", "AMR 1", "AMR 2"])
# plt.xlabel('AMR Level')
# plt.ylabel('Velocity (m/s)')
# plt.savefig(f"Velocity_box_amr.png")
# plt.close()

vars = [vel,mdots,thrusts,isps,fisps]
names = ["Velocity", "mdot","thrust","isp","fsp"]
y_title = ["Velocity (m/s)", "ṁ (kg/ms)", "Thrust (kN/m)", "I$_{sp}$ (sec)","F$_{sp} ($\frac{kN s}{kg m}$"]

for i,val in zip(range(len(vars)),vars):

    f, (ax,axs) = plt.subplots(1,2, figsize=(7,4), width_ratios=[1,0.75])

    ax.plot(val[0,:,0] * 10**3,val[0,:,1], label="No AMR", color=colors[0],lw=1.5)
    ax.plot(val[1,:,0]* 10**3,val[1,:,1], label="AMR 1", color=colors[1],lw=1.5)
    ax.plot(val[2,:,0]* 10**3,val[2,:,1], label="AMR 2", color=colors[2],lw=1.5)
    ax.grid()
    ax.legend()
    ax.set_xlabel("Time (ms)")
    ax.set_ylabel(y_title[i])
    # plt.savefig(f"Velocity_sing.png", dpi=1200)
    # plt.close()

    # axs = plt.figure()
    bplot = axs.boxplot(x=[val[0,stab:,1],val[1,stab:,1], val[2,stab:,1]], label=["No AMR", "AMR 1", "AMR 2"],
                    patch_artist=True, meanprops={"markeredgecolor": "black",  "markerfacecolor": "black"})
    axs.grid(True, axis='y')
    # fill with colors
    for patch, color in zip(bplot['boxes'], colors[0:3]):
        patch.set_facecolor(color)
    for median in bplot['medians']:
        median.set_color('black')
    axs.set_xticks([y + 1 for y in range(3)],labels=["No AMR", "AMR 1", "AMR 2"])
    plt.savefig(names[i] + "_amr.png", dpi=1200)
    plt.close()





