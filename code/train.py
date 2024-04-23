from stable_baselines3 import PPO, DQN
from stable_baselines3.common.vec_env import DummyVecEnv

import os
import time

import gym_game.envs.self_driving.avoid_obstacles_env


#### HYPER PARAMETERS
TIMESTEPS = 10000000
N_CPU = 6
# IMPORTANT: Don't set the n of obstacles above 13 (not tested), if set to 0 WithoutObstacle env automatic loaded
NUM_OBSTACLES = 0
RENDER = None # None or "human"


def make_env_no_obstacle():
    return gym_game.envs.self_driving.avoid_obstacles_env.WithoutObstacles(render_mode=RENDER)

def make_env_with_obstacle():
    return gym_game.envs.self_driving.avoid_obstacles_env.WithObstacles(render_mode=RENDER, number_obstacles=NUM_OBSTACLES)


MODELS_DIR = f"trained_agent/models/PPO_MODELS"
LOGS_DIR = f"trained_agent/logs/PPO_MODELS"

if not os.path.exists(MODELS_DIR):
    os.makedirs(MODELS_DIR)
    print("> Models dir created")

if not os.path.exists(LOGS_DIR):
    os.makedirs(LOGS_DIR)
    print("> Logs dir created")

if NUM_OBSTACLES == 0:
    env = DummyVecEnv([make_env_no_obstacle for _ in range(N_CPU)])
else:
    env = DummyVecEnv([make_env_with_obstacle for _ in range(N_CPU)])

model = PPO(
    "MlpPolicy",
    env,
    verbose=1,
    tensorboard_log=LOGS_DIR,
    device="cpu",
    n_steps=800
)

try:
    model.learn(
        total_timesteps=TIMESTEPS,
        tb_log_name="PPO",
        reset_num_timesteps=True
    )
except KeyboardInterrupt:
    print("Model stopped and save and the current TIMESTEP where it was.")

model.save(f"{MODELS_DIR}/PPO_MODEL_{TIMESTEPS}")