
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import os, inspect
import ray
import gym
from ray.rllib.agents import ppo
from ray.tune.registry import register_env
from ray.tune import run_experiments

import gym, logging
from mpi4py import MPI
from gibson.envs.husky_env import HuskyNavigateEnv
import baselines.common.tf_util as U
import datetime
from baselines import logger
import os.path as osp
import tensorflow as tf
import random
import sys

import numpy as np
from numba import cuda


ray.init()

#cuda.select_device(0)
#with tf.device('/gpu:0'):
def getGibsonEnv(env_config):
    print('creating Husky Env')
    if env_config.worker_index % 2 == 0:
        print("!!!!!!!!!!!Worker_num:%s  !!!!!!!!!!" %env_config.worker_index)
        config_file = os.path.join('/root/mount/gibson/examples/train/', '..', 'configs', 'husky_navigate_rgb_train.yaml')
        print(config_file)
        env = HuskyNavigateEnv(gpu_idx=0,
                                   config=config_file)
        return env
    else:

        #env.reset()
    return

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
    "num_workers": 2,
    "train_batch_size": 2000,
    "sample_batch_size": 100,
    "lambda": 0.95,
    "clip_param": 0.2,
    "num_sgd_iter": 20,
    "lr": 0.0001,
    "sgd_minibatch_size": 32,
    "num_gpus": 1,
    "num_gpus_per_worker": 0.1,
    'use_gae': True,
    'horizon': 4096,
    'kl_coeff': 0.0,
    'vf_loss_coeff': 0.0,
    'entropy_coeff': 0.0
})

alg = ppo.PPOAgent(config=config, env=env_name)

for i in range(3888):
    result = alg.train()
    print('result = {}'.format(result))

    if i % 10 == 0:
        checkpoint = alg.save()
        print('checkpoint saved at', checkpoint)
