from stable_baselines3 import PPO

import gym


if __name__ == "__main__": 
    gym.envs.register(
        id='AvoidObstaclesEnv-v0',
        entry_point='gym_game.envs.self_driving:AvoidObstaclesEnv',
        max_episode_steps=1000000000,
    )

    env = gym.make("AvoidObstaclesEnv-v0")

    env.render_mode = "human"

    path_model = "trained_agent/models/1710689970/PPO_MODEL_3000000.zip"
    MODEL = PPO.load(path_model)

    obs, _info = env.reset()
    for i in range(10000):
        action, _states = MODEL.predict(obs, deterministic=True)
        obs, reward, done, info = env.step(action)

        if done:
            obs, _info = env.reset()

        env.render(mode="human")