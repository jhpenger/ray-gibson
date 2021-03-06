from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import os
import ray
from ray.rllib.agents import ppo
from ray.tune.registry import register_env
from ray.tune import run_experiments
from gibson.envs.husky_env import HuskyNavigateEnv
from my_husky_env import MyHusky

def getGibsonEnv(env_config):
    print('creating Husky Env')
    if True:
        config_file = os.path.join('/root/mount/gibson/ray-gibson/train/', '..', 'configs', 'husky_128.yaml')
        env = MyHusky(config_file)
        return env
    return

ray.init()
env_name = "test"
register_env(env_name, lambda _ : getGibsonEnv(_))

config = ppo.DEFAULT_CONFIG.copy()
config.update({
    "model": {
        "conv_filters": [
            [32, [8, 8], 4],
            [64, [4, 4], 2],
            [64, [10, 10], 8],
        ],
    },
    "num_workers": 1,
    "train_batch_size": 2000,
    "sample_batch_size": 100,
    "lambda": 0.95,
    "clip_param": 0.2,
    "num_sgd_iter": 20,
    "lr": 0.0001,
    "sgd_minibatch_size": 32,
    "num_gpus": 0.1,
    "num_gpus_per_worker": 0.1,
    'use_gae': True,
    'horizon': 4096,
    'kl_coeff': 0.0,
    'vf_loss_coeff': 0.0,
    'entropy_coeff': 0.0,
    'tf_session_args': {
        'gpu_options': {'allow_growth': True}
    }
})

alg = ppo.PPOAgent(config=config, env=env_name)

for i in range(8888):
    result = alg.train()
    print('result = {}'.format(result))

    if i % 10 == 0:
        checkpoint = alg.save()
        print('checkpoint saved at', checkpoint)
