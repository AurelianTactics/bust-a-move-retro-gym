import sys
import retro
import csv
import time
import pickle
from baselines.common.atari_wrappers import WarpFrame, FrameStack
import numpy as np
#from sonic_util_test import AllowBacktracking #, make_env
from collections import OrderedDict

#1 for viewing videos, 0 for creating waypoints
debug = int(sys.argv[1])

level_string = 'BustAMove.1pplay.Level1'#'BustAMove.Challengeplay0'
replay_number = '0'
#movie_path = 'human/BustAMove-Snes/scenario/BustAMove-Snes-{}.state-0{}.bk2'.format(level_string,replay_number)
movie_path = 'videos/BustAMove-Snes-{}-00000{}.bk2'.format(level_string,replay_number)
print(movie_path)
movie = retro.Movie(movie_path)
movie.step()

scenario_string= 'scenario'#'test_retro' #'trajectory_max'
env = retro.make(game=movie.get_game(), state=level_string, scenario=scenario_string)
env.initial_state = movie.get_state()
env.reset()

button_dict = ['B', 'A', 'MODE', 'START', 'UP', 'DOWN', 'LEFT', 'RIGHT', 'C', 'Y', 'X', 'Z']
num_buttons = 12#len(button_dict)

num_steps = 0
total_reward = 0.
keys_file = open('keys.csv','w')
keys_csv = csv.DictWriter(keys_file,fieldnames=['step','keys','action','r','x','y','rings'])
keys_csv.writeheader()

trajectory_steps = 0
traj_dict = OrderedDict()

#creates a waypoint for the reward function when the user holds waypoint_key down for waypoint_threshold number of steps
waypoint_steps = 0
waypointx_dict = OrderedDict()
waypointy_dict = OrderedDict()
waypoint_key = 'DOWN'
waypoint_this_frame = 0
waypoint_press = 0
waypoint_threshold = 30
prev_waypoint_x = 0
prev_waypoint_y = 0

print('stepping movie')

while movie.step():
    if debug:
        env.render()
        time.sleep(0.01)
    keys = []
    #key_string = '_'
    #waypoint_this_frame = 0
    for i in range(num_buttons):
        #print(i)
        keys.append(movie.get_key(i,0))
        #if movie.get_key(i):
            #key_string += button_dict[i] + "_"
        #    if button_dict[i] == waypoint_key:
                #print(movie.get_key(i),button_dict[i])
        #        waypoint_this_frame = 1

    _obs, _rew, _done, _info = env.step(keys)
    num_steps += 1
    total_reward += _rew

    #keys_csv.writerow({'step': num_steps, 'keys':key_string, 'action':key_string, 'r':_rew, 'x':current_x, 'y':current_y, 'rings':_info['rings']})
    if debug: #and _rew > -1000:
        print(np.round(_rew,2), "_",np.round(total_reward,0),"_", _info['bubbles'],"--{},{}--{}".format(_done,_done,_done))



keys_file.close()

if not debug:
    t_file = open('traj_dict_{}_{}.csv'.format(level_string,replay_number),'w')
    t_csv = csv.DictWriter(t_file,fieldnames=['line'])
    for key,value in traj_dict.items():
        zString = "    ret_value[{}] = {}".format(key, value)
        t_csv.writerow({'line':zString})
    t_file.close()

    w_file = open('waypoint_dict_{}_{}.csv'.format(level_string,replay_number),'w')
    w_csv = csv.DictWriter(w_file,fieldnames=['line'])
    for key,value in waypointx_dict.items():
        zString = "    ret_x[{}] = {}".format(key,value)
        w_csv.writerow({'line':zString})
    for key,value in waypointy_dict.items():
        zString = "    ret_y[{}] = {}".format(key,value)
        w_csv.writerow({'line':zString})
    w_file.close()
