from gym_game.envs.self_driving.avoid_obstacles_env import WithoutObstacles, WithObstacles
from stable_baselines3.common.vec_env import DummyVecEnv


env = WithObstacles(render_mode=None, number_obstacles=10)
n_cpu = 6
env = DummyVecEnv([lambda: env])


from stable_baselines3 import DQN, PPO 
import os
import time


path_model = "trained_agent/models/" + "PPO_MODELS" + "/PPO_MODEL"

model = PPO.load(
    path=path_model,
    env=env,
    device="cpu",
)


MODELS_DIR = f"trained_agent/models/PPO_MODELS"
LOGS_DIR = f"trained_agent/logs/PPO_MODELS"

if not os.path.exists(MODELS_DIR):
    os.makedirs(MODELS_DIR)
    print("> Models dir created")

if not os.path.exists(LOGS_DIR):
    os.makedirs(LOGS_DIR)
    print("> Logs dir created")


TIMESTEPS = 2500000
try:
    model.learn(
        total_timesteps=TIMESTEPS,
        tb_log_name="PPO",
        reset_num_timesteps=False
    )
except KeyboardInterrupt:
    print("Model stopped and save and the current TIMESTEP where it was.")

model.save(f"{MODELS_DIR}/PPO_MODEL")
