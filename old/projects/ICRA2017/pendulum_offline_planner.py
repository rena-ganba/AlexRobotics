# -*- coding: utf-8 -*-
"""
Created on Sun Mar  6 15:27:04 2016

@author: alex
"""

from AlexRobotics.planning import RandomTree           as RPRT
from AlexRobotics.dynamic  import CustomManipulator    as CM
from AlexRobotics.control  import RminComputedTorque   as RminCTC

import numpy as np
import matplotlib.pyplot as plt


ReComputeTraj = True
saving_auto   = False
simulation    = False
name_traj     = 'data/pendulum_traj.npy'


####################################
R  =  CM.TestPendulum()


R.ubar = np.array([0,0,0,1])

x_start = np.array([-np.pi + 0.05 ,0,0,0,0,0])
x_goal  = np.array([ 0,0,0,0,0,0])

RRT = RPRT.RRT( R , x_start )

T    = 0.02
u_R1 = 0
u_R2 = 0

#RRT.U = np.array([ [ T,0,0,u_R1] , [ 0,0,0,u_R1] , [ -T,0,0,u_R1] ])

RRT.U = np.array([ [ T,0,0,u_R1] , [ 0,0,0,u_R1] , [ -T,0,0,u_R1] , [ T,0,0,u_R2] , [ 0,0,0,u_R2] , [ -T,0,0,u_R2] ])


RRT.dt                    = 0.05
RRT.goal_radius           = 0.2
RRT.alpha                 = 0.8
RRT.max_nodes             = 10000
RRT.max_solution_time     = 3

# Make sure no low-gear is used at high-speed by the planner
RRT.test_u_domain = True

# Dynamic plot
RRT.dyna_plot             = False
RRT.dyna_node_no_update   = 1000

RRT.y1axis = 0
RRT.y2axis = 3

RRT.low_pass_filter.set_freq_to( fc = 5 , dt = RRT.dt )



if ReComputeTraj:
    
    RRT.find_path_to_goal( x_goal )
    RRT.plot_2D_Tree()
    
    if saving_auto:
        RRT.save_solution( name_traj  )
    
else:
    
    RRT.load_solution( name_traj  )
    RRT.test_u_domain = True

#RRT.plot_open_loop_solution()
#RRT.plot_open_loop_solution_acc()

#RRT.solution_smoothing()

#RRT.plot_open_loop_solution()
#RRT.plot_open_loop_solution_acc()


if simulation:
    
    # Assign controller
    CTC_controller      = RminCTC.RminComputedTorqueController( R )
    
    CTC_controller.load_trajectory( RRT.solution )
    CTC_controller.goal = x_goal
    R.ctl               = CTC_controller.ctl
    
    CTC_controller.n_gears      = 2
    CTC_controller.w0           = 2.0
    CTC_controller.zeta         = 0.7
    #CTC_controller.traj_ref_pts = 'closest'
    CTC_controller.traj_ref_pts = 'interpol'
    CTC_controller.hysteresis   = True
    CTC_controller.hys_level    = 0.005
    
    
    # Plot
    tf = RRT.time_to_goal + 5
    n  = int( np.round( tf / 0.005 ) ) + 1
    R.plotAnimation( x_start , tf , n , solver = 'euler' )
    R.Sim.plot_CL('x') 
    R.Sim.plot_CL('u')
    


plt.ion()



# Ploting

fig = RRT.phasefig
axe = RRT.phasefig.get_axes()[0]

fontsize = 5

#matplotlib.rc('xtick', labelsize = fontsize )
#matplotlib.rc('ytick', labelsize = fontsize )

axe.tick_params(axis='both', which='major', labelsize=fontsize)

axe.set_xlabel('Angle [rad]', fontsize = fontsize)
axe.set_ylabel('Speed [rad/sec]', fontsize = fontsize)
axe.set_xlim(-6,1)

fig.set_size_inches(3, 2)

fig.canvas.draw()
fig.show()


fig.savefig('output/rrt_fig.pdf', dpi = 300 , format = 'pdf' , bbox_inches='tight', pad_inches=0.05 )