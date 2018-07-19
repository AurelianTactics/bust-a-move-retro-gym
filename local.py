import retro
import retro_contest
import gym
import os


def make(game, state=retro.State.DEFAULT, discrete_actions=False, bk2dir=None,monitordir=None, scenario='scenario'):
    use_restricted_actions = retro.Actions.FILTERED#retro.ACTIONS_FILTERED
    if discrete_actions:
        use_restricted_actions = retro.Actions.DISCRETE#retro.ACTIONS_DISCRETE
    try:
        #env = retro.make(game, state, scenario='contest', use_restricted_actions=use_restricted_actions)
        env = retro.make(game, state, scenario=scenario, use_restricted_actions=use_restricted_actions)
    except Exception:
        env = retro.make(game, state, use_restricted_actions=use_restricted_actions)
    if bk2dir:
        env.auto_record(bk2dir)
    #added this
    if monitordir:
        env = retro_contest.Monitor(env, os.path.join(monitordir, 'monitor.csv'), os.path.join(monitordir, 'log.csv'))
    env = retro_contest.StochasticFrameSkip(env, n=16, stickprob=0.0)
    #env = retro_contest.StochasticFrameSkip(env, n=4, stickprob=0.25)
    #env = gym.wrappers.TimeLimit(env, max_episode_steps=4500)
    #env.serve(timestep_limit=10000, ignore_reset=True)
    return env

