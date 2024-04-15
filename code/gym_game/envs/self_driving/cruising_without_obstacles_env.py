import gymnasium as gym
import numpy as np
from gymnasium import spaces

from ...helpers.cars import Agent
from ...helpers.world import World, obstacle_sprites_group
from ...helpers.sensors import update_position_sensors, collision_sensors, create_sensors_data, draw_sensors, SENSORS_COLLISIONS_DATA

import pygame

class WithoutObstacles(gym.Env):
    metadata = {"render_modes": ["human"], "render_fps": 60}

    window_size = (1280, 720)

    def __init__(self, render_mode=None):
        super().__init__()

        self.action_space = spaces.Discrete(5)

        low = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
        high = np.array([self.window_size[0], self.window_size[1], 4, 360, 9999, 9999,9999,9999,9999,9999,9999,9999])
        self.observation_space = spaces.Box(low=low, high=high,
                                            shape=(12,), dtype=np.int64)

        self.render_mode = render_mode

        self.window = None
        self.clock = None

        topSpeed = 4
        turnRate = 3
        self.AGENT = Agent(
            topSpeed,
            turnRate
        )

        self.WORLD = World()
        self.WORLD.create_rect(self.window_size)
        self.OBSTACLE_SPRITE_GROUP = obstacle_sprites_group

        self.stepCounter = 0

        self.SENSORS_DATA = create_sensors_data(self.AGENT.rect.center)


    def _get_obs(self):
        obs = [
            self._agent_location[0],
            self._agent_location[1],
            self.AGENT.vel,
            self.AGENT.angle
        ]

        for index in range(len(SENSORS_COLLISIONS_DATA)):
            obs.append(SENSORS_COLLISIONS_DATA[index+1]["distance"])

        return np.array(obs)
    

    def get_reward(self, agent_crashed, agent_velocity):
        reward = agent_velocity if agent_velocity > 0 else -5
        reward += 0.1 # time

        if agent_crashed:
            reward = -5000

        return reward


    def step(self, action):
        self.stepCounter += 1

        self.AGENT.update_position(action)
        self._agent_location = self.AGENT.rect.center

        update_position_sensors(self.SENSORS_DATA, self._agent_location, self.AGENT.angle)
        collision_sensors(self.SENSORS_DATA, self.OBSTACLE_SPRITE_GROUP)

        terminated = False
        truncated = False
        agent_crashed = self.AGENT.collisions(self.OBSTACLE_SPRITE_GROUP)

        if agent_crashed:
            terminated = True
            self.stepCounter = 0
        
        if self.stepCounter >= 800:
            truncated = True
            self.stepCounter = 0

        done = terminated or truncated

        reward = self.get_reward(agent_crashed, self.AGENT.vel)

        observation = self._get_obs()
        info = {}

        if self.render_mode == "human":
            self.render(mode="human")

        return observation, reward, terminated, truncated, info


    def reset(self, seed=None, options=None):
        super().reset(seed=seed)

        random_position_start = self.AGENT.get_random_start_pos(self.window_size, False)
        self.AGENT.reset(random_position_start)
        self._agent_location = self.AGENT.rect.center

        update_position_sensors(self.SENSORS_DATA, self._agent_location, self.AGENT.angle)
        collision_sensors(self.SENSORS_DATA, self.OBSTACLE_SPRITE_GROUP)

        observation = self._get_obs()
        info = {}

        if self.render_mode == "human":
            self.render(mode="human")

        return observation, info

    def _render_frame(self):
        if self.window is None and self.render_mode == "human":
            pygame.init()
            pygame.display.init()
            pygame.display.set_caption("Cruising around")

            self.window = pygame.display.set_mode(self.window_size)
            self.font = pygame.font.SysFont("calibri", 20)
        
        if self.clock is None and self.render_mode == "human":
            self.clock = pygame.time.Clock()

        if self.render_mode == "human":
            self.window.fill("#d3d3d3")

            self.WORLD.draw_rects(self.window)

            update_position_sensors(self.SENSORS_DATA, self.AGENT.rect.center, self.AGENT.angle)
            draw_sensors(self.SENSORS_DATA, self.window)

            for sensor_name in SENSORS_COLLISIONS_DATA:
                if SENSORS_COLLISIONS_DATA[sensor_name]["point_of_collision"] != None:
                    x = SENSORS_COLLISIONS_DATA[sensor_name]["point_of_collision"][0]
                    y = SENSORS_COLLISIONS_DATA[sensor_name]["point_of_collision"][1]

                    pygame.draw.circle(self.window, (215, 35, 35), (x, y), radius=3)

            self.AGENT.draw(self.window)

            velocity_text = self.font.render(f"Velocity: {round(self.AGENT.vel, 2)}", False, (0,0,0))
            self.window.blit(velocity_text, (20, 60))

            fps_text = self.font.render(f"FPS: {self.clock.get_fps()}", False, (0,0,0))
            self.window.blit(fps_text, (20, 20))

            stepCounter_text = self.font.render(f"Step count: {self.stepCounter}", False, (0,0,0))
            self.window.blit(stepCounter_text, (20, 100))

            pygame.event.pump()
            pygame.display.update()

            self.clock.tick(self.metadata["render_fps"])

    def render(self, mode):
        if mode == "human":
            self.render_mode = "human"
            self._render_frame()

    def close(self):
        if self.window is not None:
            pygame.display.quit()
            pygame.quit()
