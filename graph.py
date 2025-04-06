import yt
import numpy as np
import matplotlib.pyplot as plt
import sys

start_timestep = 10000
end_timestep = 78000
#end_timestep  = 22000
vel = np.zeros((int((end_timestep - start_timestep) / 2000),2))
vel_diff = np.zeros((int((end_timestep - start_timestep) / 2000),2))
while (start_timestep < end_timestep):
    file_name = '/scratch/gpfs/MUELLER/ltt/Hydrogen/2D/plt/65_nodiff/plt_h' 
    f_1 = yt.load(file_name + str(start_timestep))
    f_2= yt.load(file_name + str(start_timestep + 2000))

    file_name_diff = '/scratch/gpfs/MUELLER/ltt/Hydrogen/2D/plt/60_inlet/plt_h'

    f_diff1 = yt.load(file_name_diff + str(start_timestep))
    f_diff2= yt.load(file_name_diff + str(start_timestep + 2000))


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

    speed = ((max_index2 - max_index1) * dxmin) / (dt) *(10**-2)
    speed_diff = ((max_index2_diff - max_index1_diff) * dxmin) / (dt_diff) *(10**-2)
    vel[int((end_timestep - start_timestep) / 2000) - 1,:] = [f_1.current_time, speed]
    vel_diff[int((end_timestep - start_timestep) / 2000) -1,:] = [f_diff1.current_time, speed_diff]
    start_timestep = start_timestep + 2000

ax = plt.figure()
plt.plot(vel[:,0] * 10**3,vel[:,1], label="No Diffusion")
plt.plot(vel_diff[:,0]* 10**3,vel_diff[:,1], label="Diffusion")
ax.legend()
plt.xlabel("Time (ms)")
plt.ylabel("Velocity (m/s)")
plt.savefig(f"Velocity_h2.png")
plt.close()

ax2 = plt.figure()
plt.boxplot(x=[vel[:,1],vel_diff[:,1]], label=["No Diffusion", "Diffusion"])
# plt.boxplot(vel_diff[:,1], label="Diffusion")
ax2.legend()
plt.ylabel("Velocity (m/s)")
plt.savefig(f"Velocity_box.png")
plt.close()