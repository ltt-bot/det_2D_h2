import yt
import numpy as np
import matplotlib.pyplot as plt
import sys

start_timestep = 1000
start = 1000
diff = 1000
stab = 0
end_timestep = 85000
colors = ["#1D4DED", "#EC8321","#14B114","#8D3FBE","#FACF0C","#6B7C8A"]
#end_timestep  = 22000
vel = np.zeros((int((end_timestep - start_timestep) / 1000),2))
vel_diff = np.zeros((int((end_timestep - start_timestep) / 1000),2))
while (start_timestep < end_timestep):
    file_name = '../../../../../../../projects/MUELLER/ltt/Output/no_diff/plt_h' 
    f_1 = yt.load(file_name +"{:05d}".format(start_timestep))
    f_2= yt.load(file_name + "{:05d}".format(start_timestep+1000))

    file_name_diff = '../../../../../../../projects/MUELLER/ltt/Output/h2_cont0/plt/plt_h'

    f_diff1 = yt.load(file_name_diff + "{:05d}".format(start_timestep))
    f_diff2= yt.load(file_name_diff + "{:05d}".format(start_timestep+1000))


    # Get the information needed for the grid
    max_level = f_1.index.max_level 

    lo =  np.array([0.0, 0.0,0.])
    hi = np.array([15.0, 5.0,0.025])

    dxmin = f_1.index.get_smallest_dx()
    dxmax = dxmin*2.0*2.0 # if amr level 2
    npts=np.floor((hi-lo)/dxmin)
    npts_np = np.array(npts)
    fields_load=["density","pressure", "Temp", "x_velocity", "y_velocity", "z_velocity","Y(H2O)"]

    # Get the values on the grid at level 0 (finest level)
    first = f_1.covering_grid(level=max_level, left_edge=lo, dims=npts, fields=fields_load)
    second = f_2.covering_grid(level=max_level, left_edge=lo, dims=npts, fields=fields_load)

    first_diff = f_diff1.covering_grid(level=max_level, left_edge=lo, dims=npts, fields=fields_load)
    second_diff = f_diff2.covering_grid(level=max_level, left_edge=lo, dims=npts, fields=fields_load)
    pres_1    = np.array(first["pressure"])
    pres_2    = np.array(second["pressure"])

    pres_diff1    = np.array(first_diff["pressure"])
    pres_diff2    = np.array(second_diff["pressure"])
    if start_timestep == 2000:
        ax = plt.figure(figsize=(5,3.75))
        plt.plot(x_arr,pres_1[:,2,0]*10**(-1), label="No Diffusion", color=colors[0], lw = 1.5)
        plt.plot(x_arr,pres_diff1[:,4,0]*10**(-1), label="Diffusion", color=colors[1], lw = 1.5)
        ax.legend()
        plt.grid()
        plt.xlabel("X (cm)")
        plt.ylabel("Pressure (Pa)")
        plt.savefig(f"pres_diff.png", dpi=1200)
        plt.close()


    x_arr = np.linspace(lo[0], hi[0], int(npts_np[0]))
    y_arr = np.linspace(lo[1], hi[1], int(npts_np[1]))

    dt = f_2.current_time - f_1.current_time
    dt_diff = f_diff2.current_time - f_diff1.current_time


    check = pres_1[:,0,0]
    check2 = pres_2[:,0,0]
    max_index1 = np.unravel_index(np.argmax(check), check.shape)[0]
    max_index2 = np.unravel_index(np.argmax(check2), check2.shape)[0]
    if max_index2 < max_index1:
        max_index2 = 600 + max_index2

    check_diff = pres_diff1[:,0,0]
    check2_diff = pres_diff2[:,0,0]
    max_index1_diff = np.unravel_index(np.argmax(check_diff), check_diff.shape)[0]
    max_index2_diff = np.unravel_index(np.argmax(check2_diff), check2_diff.shape)[0]

    if max_index2_diff < max_index1_diff:
        max_index2_diff = 600 + max_index2_diff

    if f_1.current_time > 0.35 * 10**(-3) and stab == 0:
        stab = int((start_timestep - start) / diff)

    speed = ((max_index2 - max_index1) * dxmin) / (dt) *(10**-2)
    speed_diff = ((max_index2_diff - max_index1_diff) * dxmin) / (dt_diff) *(10**-2)
    vel[int((start_timestep - start) / diff),:] = [f_1.current_time, speed]
    vel_diff[int((start_timestep - start) / diff),:] = [f_diff1.current_time, speed_diff]
    start_timestep = start_timestep + 1000

# ax = plt.figure()
# plt.plot(vel[:,0] * 10**3,vel[:,1], label="No Diffusion", color=colors[0], lw=1.5)
# plt.plot(vel_diff[:,0]* 10**3,vel_diff[:,1], label="Diffusion", color=colors[1], lw=1.5)
# ax.legend()
# plt.grid()
# plt.xlabel("Time (ms)")
# plt.ylabel("Velocity (m/s)")
# plt.savefig(f"Velocity_h2.png", dpi=1200)
# plt.close()

# axs = plt.figure()
# bplot = plt.boxplot(x=[vel[stab:,1],vel_diff[stab:,1]], 
#                  patch_artist=True)
# plt.grid(True, axis='y')
# # fill with colors
# for patch, color in zip(bplot['boxes'], colors[0:1]):
#     patch.set_facecolor(color)
# for median in bplot['medians']:
#     median.set_color('black')
# plt.xticks([y + 1 for y in range(2)],labels=["No Diffusion", "Diffusion"])
# plt.ylabel('Velocity (m/s)')
# plt.savefig(f"Velocity_box_diff.png", dpi=1200)
# plt.close()

f, (ax,axs) = plt.subplots(1,2, figsize=(7,4), width_ratios=[1,0.75])

ax.plot(vel[:,0] * 10**3,vel[:,1], label="No Diffusion", color=colors[0],lw=1.5)
ax.plot(vel_diff[:,0]* 10**3,vel_diff[:,1], label="Diffusion", color=colors[1],lw=1.5)
ax.grid()
ax.legend()
ax.set_xlabel("Time (ms)")
ax.set_ylabel("Velocity (m/s)")
# plt.savefig(f"Velocity_sing.png", dpi=1200)
# plt.close()

# axs = plt.figure()
bplot = axs.boxplot(x=[vel[stab:,1],vel_diff[stab:,1]], label=["No Diffusion", "Diffusion"],
                 patch_artist=True, meanprops={"markeredgecolor": "black",  "markerfacecolor": "black"})
axs.grid(True, axis='y')
# fill with colors
for patch, color in zip(bplot['boxes'], colors[0:2]):
    patch.set_facecolor(color)
for median in bplot['medians']:
    median.set_color('black')
axs.set_xticks([y + 1 for y in range(2)],labels=["No Diffusion", "Diffusion"])
plt.savefig(f"Velocity_diff.png", dpi=1200)
plt.close()