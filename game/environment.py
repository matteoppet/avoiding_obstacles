import gymnasium as gym
import numpy as np
from gymnasium import spaces


class AvoidObstacles(gym.Env):
    metadata = {"render_modes": ["human"], "render_fps": 30}

    def __init__(self, render_mode=None):
        super().__init__()

        self.action_space = spaces.Discrete(...)
        self.observation_space = spaces.Box(low=..., high=...,
                                            shape=..., dtype=...)

        self.render_mode = render_mode

        self.window = None
        self.clock = None


    def step(self):
        ...
        return observation, reward, terminated, truncated, info

    def reset(self, seed=None, options=None):
        ...
        return observation, info

    def _render_frame(self):
        ...

    def close(self):
        ...
