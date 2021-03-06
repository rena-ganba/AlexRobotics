# -*- coding: utf-8 -*-
"""
Created on Sun Mar  6 15:27:04 2016

@author: alex
"""

from AlexRobotics.planning import RandomTree           as RPRT
from AlexRobotics.dynamic  import Hybrid_Manipulator   as HM

import numpy as np
import matplotlib.pyplot as plt

R  =  HM.HybridOneLinkManipulator()
R.ubar = np.array([0.0,1])

x_start = np.array([-3.0,0])
x_goal  = np.array([0,0])

RRT = RPRT.RRT( R , x_start )

RRT.U = np.array([[10.0,1],[0.0,1],[-10.0,1],[3.0,10],[0.0,10],[-3.0,10]])

RRT.dt                    = 0.1
RRT.goal_radius           = 0.5
RRT.max_nodes             = 5000
RRT.max_solution_time     = 5

#RRT.compute_steps(1000,True)
RRT.find_path_to_goal( x_goal )

# Assign controller
#R.ctl = RRT.open_loop_controller
R.ctl             = RRT.trajectory_controller
RRT.traj_ctl_kp   = 25
RRT.traj_ctl_kd   = 10

# Plot
tf = RRT.time_to_goal + 5
n = int( tf / 0.05 ) +1
R.plotAnimation( x_start , tf , n , solver = 'euler' )
R.Sim.plot_CL()
#R.phase_plane_trajectory([0,1],x_start,tf,True,False,False,True)
R.Sim.phase_plane_trajectory(True,False,False,True)
RRT.plot_2D_Tree()


# Hold figures alive
plt.show()