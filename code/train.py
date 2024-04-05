from stable_baselines3 import PPO, DQN
from stable_baselines3.common.vec_env import DummyVecEnv

import os
import time


MODELS_DIR = f"trained_agent/models/{int(time.time())}"
LOGS_DIR = f"trained_agent/logs/{int(time.time())}"

if not os.path.exists(MODELS_DIR):
    os.makedirs(MODELS_DIR)
    print("> Models dir created")

if not os.path.exists(LOGS_DIR):
    os.makedirs(LOGS_DIR)
    print("> Logs dir created")


from gym_game.envs.self_driving.avoid_obstacles_env import AvoidObstaclesEnv
from gym_game.envs.self_driving.cruising_without_obstacles_env import WithoutObstacles

env = WithoutObstacles(render_mode=None)
n_cpu = 6
env = DummyVecEnv([lambda: env])

model = PPO(
    "MlpPolicy",
    env,
    verbose=1,
    tensorboard_log=LOGS_DIR,
    device="cpu",
)

TIMESTEPS = 10000000
try:
    model.learn(
        total_timesteps=TIMESTEPS,
        tb_log_name="PPO",
        reset_num_timesteps=False
    )
except KeyboardInterrupt:
    print("Model stopped and save and the current TIMESTEP where it was.")

model.save(f"{MODELS_DIR}/PPO_MODEL_{TIMESTEPS}") # stopped at 6377472

"""
Finish training

Is important the reward function,
and if not work check for observation if are right or not
"""