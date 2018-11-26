from gibson.envs.husky_env import HuskyNavigateEnv
import numpy as np


class MyHusky(HuskyNavigateEnv):
    def reset(self):
        observations = super()._reset()
        obs = np.concatenate([observations.get('rgb_filled'), observations.get('depth')], axis = 2) if 'depth' in observations.keys() else observation.get('rgb_filled')
        return obs

    def step(self, a):
        observations, sensor_reward, done, sensor_meta = super()._step(a)
        obs = np.concatenate([observations.get('rgb_filled'), observations.get('depth')], axis = 2) if 'depth' in observations.keys() else observation.get('rgb_filled')
        return obs, sensor_reward, done, sensor_meta
