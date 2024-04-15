from gym_game.envs.self_driving.avoid_obstacles_env import WithoutObstacles, WithObstacles
from stable_baselines3.common.vec_env import DummyVecEnv


env = WithObstacles(render_mode=None)
n_cpu = 6
env = DummyVecEnv([lambda: env])


from stable_baselines3 import DQN, PPO 
import os
import time


path_model = "trained_agent/models/" + "1712831354" + "/PPO_MODEL_10000000"

model = PPO.load(
    path=path_model,
    env=env,
    device="cpu",
)


MODELS_DIR = f"trained_agent/models/{int(time.time())}"
LOGS_DIR = f"trained_agent/logs/{int(time.time())}"

if not os.path.exists(MODELS_DIR):
    os.makedirs(MODELS_DIR)
    print("> Models dir created")

if not os.path.exists(LOGS_DIR):
    os.makedirs(LOGS_DIR)
    print("> Logs dir created")


TIMESTEPS = 500000
try:
    model.learn(
        total_timesteps=TIMESTEPS,
        tb_log_name="PPO",
        reset_num_timesteps=False
    )
except KeyboardInterrupt:
    print("Model stopped and save and the current TIMESTEP where it was.")

model.save(f"{MODELS_DIR}/PPO_MODEL_{TIMESTEPS}") # stopped at 6377472
