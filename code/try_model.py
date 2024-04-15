from stable_baselines3 import PPO, DQN
from gym_game.envs.self_driving.avoid_obstacles_env import WithObstacles, WithoutObstacles

import gym


if __name__ == "__main__": 
    # gym.envs.register(
    #     id='AvoidObstaclesEnv-v0',
    #     entry_point='gym_game.envs.self_driving:AvoidObstaclesEnv',
    #     max_episode_steps=700,
    # )

    # env = gym.make("AvoidObstaclesEnv-v0")

    # env.render_mode = "human"

    env = WithObstacles(render_mode="human")

    path_model = "trained_agent/models/1713043920/PPO_MODEL_500000.zip"
    MODEL = PPO.load(path_model)

    obs, _info = env.reset()
    for i in range(10000):
        action, _states = MODEL.predict(obs)
        obs, reward, terminated, truncated, info = env.step(action)

        if terminated or truncated:
            obs, _info = env.reset()