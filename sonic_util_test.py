"""
Environments and wrappers for Sonic training.
"""

import gym
import numpy as np

from baselines.common.atari_wrappers import WarpFrame, FrameStack
import gym_remote.client as grc
from retro_contest.local import make #added for local

def make_env(stack=True, scale_rew=True, scenario = 'scenario'): #scenario =  #'contest'
    """
    Create an environment with some standard wrappers.
    """
    #env = grc.RemoteEnv('tmp/sock')
    #env = make(game='SonicTheHedgehog-Genesis', state='SpringYardZone.Act1', bk2dir='videos', monitordir='logs',scenario=scenario)
#'BustAMove.1pplay.Level1' #BustAMove.Challengeplay0
    #env = make(game='BustAMove-Snes', state='BustAMove.1pplay.Level1', bk2dir='videos', monitordir='logs',scenario=scenario)
    env = make(game='ContraIII-Snes', state='level1.1player.easy.100lives', bk2dir='videos', monitordir='logs',
               scenario=scenario)

    env = SonicDiscretizer(env)
    if scale_rew:
        env = RewardScaler(env)
    env = WarpFrame(env)
    if stack:
        env = FrameStack(env, 4)
    return env

class SonicDiscretizer(gym.ActionWrapper):
    """
    Wrap a gym-retro environment and make it use discrete
    actions for the Sonic game.
    """
    def __init__(self, env):
        super(SonicDiscretizer, self).__init__(env)
        #SNES keys
        buttons = ["B", "Y", "SELECT", "START", "UP", "DOWN", "LEFT", "RIGHT", "A", "X", "L", "R"]
        #bust a move keys
        #actions = [['LEFT'], ['RIGHT'], ['B'], ['L'], ['R']]
        #Contra 3 keys side scrolling levels
        #level 1
        actions = [['Y'],['A'],['Y','LEFT'],['Y','RIGHT'],['Y','X'],['Y','B','LEFT'],['Y','B','RIGHT'],
                   ['Y','UP','LEFT'],['Y','UP','RIGHT'],['Y','DOWN','LEFT'],['Y','DOWN','RIGHT'],
                   ['Y', 'DOWN'],['Y','L','R','RIGHT'],['Y','L','R','LEFT']]
        #level 3,4,6
        # actions = [['Y'], ['A'], ['Y', 'LEFT'], ['Y', 'RIGHT'], ['Y', 'X'], ['Y', 'B', 'LEFT'], ['Y', 'B', 'RIGHT'],
        #            ['Y', 'UP', 'LEFT'], ['Y', 'UP', 'RIGHT'], ['Y', 'DOWN', 'LEFT'], ['Y', 'DOWN', 'RIGHT'],
        #            ['Y', 'DOWN'], ['Y', 'L', 'R', 'RIGHT'], ['Y', 'L', 'R', 'LEFT'],
        #            ['Y', 'R', 'UP', 'LEFT'], ['Y', 'R', 'UP', 'RIGHT'], ['Y', 'R', 'DOWN', 'LEFT'],
        #            ['Y', 'R', 'DOWN', 'RIGHT'],['UP'],['RIGHT'],['Y','DOWN'],['Y','UP']]

        # actions = [['Y','LEFT'],['Y','RIGHT'],['Y','X'],['Y','B','LEFT'],['Y','B','RIGHT'],
        #            ['Y','UP','LEFT'],['Y','UP','RIGHT'],['Y','DOWN','LEFT'],['Y','DOWN','RIGHT'],
        #            ['Y', 'DOWN']]
                    #due to cheesing the scrolling part, can't do R actions and up/down
                    #['Y', 'UP'], ['Y', 'DOWN'],['Y','B'],['Y','X'],['Y','B','DOWN'],
                   #['Y','R','UP','LEFT'],['Y','R','UP','RIGHT'],['Y','R','DOWN','LEFT'],['Y','R','DOWN','RIGHT']]
        self._actions = []
        for action in actions:
            arr = np.array([False] * 12)
            if action == ['NOOP']:
                self._actions.append(arr)
                continue
            for button in action:
                arr[buttons.index(button)] = True
            self._actions.append(arr)
        self.action_space = gym.spaces.Discrete(len(self._actions))

    def action(self, a): # pylint: disable=W0221
        return self._actions[a].copy()

class RewardScaler(gym.RewardWrapper):
    """
    Bring rewards to a reasonable scale for PPO.

    This is incredibly important and effects performance
    drastically.
    """
    def reward(self, reward):
        #sonic rewards generally in the low -5 to 5 range, hundreds bonus at level end
        #return reward * 0.01
        #bust a move (for score) in the 30 to 100 range for score (in general, many in high hundres low thouands).
            # thousands/tenthousands bonus at lvl end
        #bust a move for bubbles is fine with 0.01
        #return reward * 0.0005
        return reward * 0.01

class AllowBacktracking(gym.Wrapper):
    """
    Use deltas in max(X) as the reward, rather than deltas
    in X. This way, agents are not discouraged too heavily
    from exploring backwards if there is no way to advance
    head-on in the level.
    """
    def __init__(self, env):
        super(AllowBacktracking, self).__init__(env)
        self._cur_x = 0
        self._max_x = 0

    def reset(self, **kwargs): # pylint: disable=E0202
        self._cur_x = 0
        self._max_x = 0
        return self.env.reset(**kwargs)

    def step(self, action): # pylint: disable=E0202
        obs, rew, done, info = self.env.step(action)
        self._cur_x += rew
        rew = max(0, self._cur_x - self._max_x)
        self._max_x = max(self._max_x, self._cur_x)
        return obs, rew, done, info
