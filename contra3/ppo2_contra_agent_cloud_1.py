#!/usr/bin/env python

"""
Train an agent on Sonic using PPO2 from OpenAI Baselines.
"""

import tensorflow as tf

from baselines.common.vec_env.dummy_vec_env import DummyVecEnv
import baselines.ppo2.ppo2 as ppo2
import baselines.ppo2.policies as policies
import gym_remote.exceptions as gre

from sonic_util_test import make_env

def main():
    """Run PPO until the environment throws an exception."""
    config = tf.ConfigProto()
    config.gpu_options.allow_growth = True # pylint: disable=E1101
    with tf.Session(config=config):
        # Take more timesteps than we need to be sure that
        # we stop due to an exception
        ppo2.learn(policy=policies.CnnPolicy,
                   env=DummyVecEnv([make_env]), #for contest/trajectory_max need to edit sonic_util_test defaults
                   nsteps=2768,
                   nminibatches=251,
                   lam=0.977,
                   gamma=0.995,
                   noptepochs=9,
                   log_interval=100,
                   ent_coef=0.003, #many actions
                   vf_coef=0.667,
                   lr=lambda _: 7.66654e-5,
                   cliprange=lambda _: 0.179,
                   save_interval=500,
                   save_path='ppo_save',
                   total_timesteps=int(2e9))
                   #total_timesteps=int(10000))

if __name__ == '__main__':
    try:
        main()
    except gre.GymRemoteError as exc:
        print('exception', exc)
