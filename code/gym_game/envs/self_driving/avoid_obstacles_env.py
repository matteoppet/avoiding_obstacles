import gymnasium as gym
import numpy as np
from gymnasium import spaces

import pygame
from ...helpers.cars import Agent
from ...helpers.sensors import update_sensors_position_data, collision_sensors, draw_sensors
from ...helpers.world import World, obstacle_sprites_group


class AvoidObstaclesEnv(gym.Env):
    metadata = {"render_modes": ["human"], "render_fps": 30}

    window_size = (1280, 720)

    def __init__(self, render_mode=None):
        super().__init__()

        self.action_space = spaces.Discrete(5)

        """Observations:
            - Position x agent
            - Position y agent
            - Sensor 1
            - Sensor 2
            - Sensor 3
            - Sensor 4
            - Sensor 5
            - Speed
            - Angle
        """
        low = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0])
        high = np.array([
            self.window_size[0],  self.window_size[1],
            200, 200, 200, 200, 200,
            4, 360])
        self.observation_space = spaces.Box(low=low, high=high,
                                            shape=(9,), dtype=np.float32)

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
        self.WORLD.create_rect()
        self.OBSTACLE_SPRITES_GROUP = obstacle_sprites_group

    def _get_sensors_info(self):
        data_sensors = update_sensors_position_data(
            self._agent_location, self.AGENT.angle)
        info_sensors_dict = collision_sensors(obstacle_sprites_group)

        return info_sensors_dict, data_sensors
 
    def _get_obs(self):
        sensors_dict, _ = self._get_sensors_info()
        return [
            self._agent_location[0],
            self._agent_location[1],
            sensors_dict["left"]["distance"],
            sensors_dict["diagonal_left"]["distance"],
            sensors_dict["center"]["distance"],
            sensors_dict["diagonal_right"]["distance"],
            sensors_dict["right"]["distance"],
            self.AGENT.vel,
            self.AGENT.angle
        ]
    
    def reward_function(self, agent_crashed, velocity_player):
        if velocity_player > 0:
            reward = 1 + velocity_player
        else:
            reward = -2

        if agent_crashed:
            reward = -100

        return reward

    def step(self, action):
        self.AGENT.update_position(action)
        self._agent_location = self.AGENT.rect.center

        terminated = False
        agent_crashed = self.AGENT.collisions(obstacle_sprites_group)

        if agent_crashed:
            terminated = True

        # reward
        reward = self.reward_function(agent_crashed, self.AGENT.vel)

        observation = self._get_obs()
        info = {}

        done = False
        if terminated:
            done = True

        if self.render_mode == "human":
            self.render(mode="human")

        return observation, reward, done, info

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        
        random_position_start = self.AGENT.get_random_position()
        self._agent_location = random_position_start
        self.AGENT.reset(random_position_start)

        observation = self._get_obs()
        info = {}

        if self.render_mode == "human":
            self.render(mode="human")

        return observation, info
    
    def render(self, mode):
        if mode == "human":
            self.render_mode = "human"
            self._render_frame()

    def _render_frame(self):
        if self.window is None and self.render_mode == "human":
            pygame.init()
            pygame.display.init()
            pygame.display.set_caption("Avoid Obstacles")

            self.window = pygame.display.set_mode(self.window_size)
            self.font = pygame.font.SysFont("calibri", 20)
        
        if self.clock is None and self.render_mode == "human":
            self.clock = pygame.time.Clock()

        if self.render_mode == "human":
            self.window.fill("#d3d3d3")

            self.WORLD.draw_rects(self.window)

            collisions_sensors_dict, data_sensors = self._get_sensors_info()
            for name, info in data_sensors.items():
                draw_sensors(
                    win=self.window,
                    start_position=info["start"],
                    end_position=info["end"]
                )

            for name_sensor in collisions_sensors_dict:
                if collisions_sensors_dict[name_sensor]["point_of_collision"] != None:
                    x = collisions_sensors_dict[name_sensor]["point_of_collision"][0]
                    y = collisions_sensors_dict[name_sensor]["point_of_collision"][1]

                    rect = pygame.Rect(x, y, 5, 5)
                    pygame.draw.rect(self.window, "red", rect)

            self.AGENT.draw(self.window)

            velocity_text = self.font.render(f"Velocity: {round(self.AGENT.vel, 2)}", False, (0,0,0))
            self.window.blit(velocity_text, (20, 315))

            fps_text = self.font.render(f"FPS: {self.clock.get_fps()}", False, (0,0,0))
            self.window.blit(fps_text, (20, 20))

            pygame.event.pump()
            pygame.display.update()

            self.clock.tick(self.metadata["render_fps"])

    def close(self):
        if self.window is not None:
            pygame.display.quit()
            pygame.quit()
