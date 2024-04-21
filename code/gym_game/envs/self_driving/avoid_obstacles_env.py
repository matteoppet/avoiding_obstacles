import gymnasium as gym
import numpy as np
from gymnasium import spaces

import pygame
from ...helpers.cars import Agent
from ...helpers.sensors import update_position_sensors, collision_sensors, create_sensors_data, draw_sensors, SENSORS_COLLISIONS_DATA
from ...helpers.world import World


class BaseEnv(gym.Env):
    metadata = {"render_modes": ["human"], "render_fps": 40}

    window_size = (1280, 720)

    def __init__(self):
        super().__init__()

        self.action_space = spaces.Discrete(5)

        low = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
        high = np.array([self.window_size[0], self.window_size[1], 4, 360, 9999, 9999,9999,9999,9999,9999,9999,9999])
        shape = (len(low),)
        self.observation_space = spaces.Box(
            low=low,
            high=high,
            shape=shape,
            dtype=np.float32
        )

        self.window = None
        self.clock = None

        topSpeed = 3
        turnRate = 3
        self.AGENT = Agent(
            topSpeed,
            turnRate
        )

        self.stepCounter = 0

        self.SENSORS_DATA = create_sensors_data(self.AGENT.rect.center)

    def create_world(self, number_obstacles=0):
        self.WORLD = World(self.window_size)
        self.obstacle_group = pygame.sprite.Group()
        self.NUM_OBSTACLE_TO_GENERATE = number_obstacles
        self.WORLD.reset_obstacles(self.obstacle_group, self.NUM_OBSTACLE_TO_GENERATE)


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
    

    def step(self, action):
        self.stepCounter += 1

        self.AGENT.update_position(action)
        self._agent_location = self.AGENT.rect.center

        update_position_sensors(self.SENSORS_DATA, self._agent_location, self.AGENT.angle)
        collision_sensors(self.SENSORS_DATA, self.obstacle_group)

        terminated = False
        truncated = False
        agent_crashed = self.AGENT.collisions(self.obstacle_group)

        if agent_crashed:
            terminated = True
        
        if self.stepCounter >= 800:
            truncated = True

        reward = self.get_reward(agent_crashed, self.AGENT.vel)

        observation = self._get_obs()
        info = {}

        if self.render_mode == "human":
            self.render()

        return observation, reward, terminated, truncated, info


    def _render_frame(self):
        if self.window is None and self.render_mode == "human":
            pygame.init()
            pygame.display.init()
            pygame.display.set_caption("Cruising around")

            self.window = pygame.display.set_mode(self.window_size)
            self.background = pygame.Surface(self.window_size)
            self.font = pygame.font.SysFont("calibri", 20)
        
        if self.clock is None and self.render_mode == "human":
            self.clock = pygame.time.Clock()

        if self.render_mode == "human":
            self.window.fill("#d3d3d3")

            self.obstacle_group.draw(self.window, self.background)

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


    def render(self):
        if self.render_mode == "human":
            self._render_frame()

    
    def close(self):
        if self.window is not None:
            pygame.display.quit()
            pygame.quit()



class WithoutObstacles(BaseEnv):
    def __init__(self, render_mode=None):
        super().__init__()

        self.render_mode = render_mode
        self.create_world(number_obstacles=0)


    def get_reward(self, agent_crashed, velocity_player):
        reward = velocity_player if velocity_player > 0 else -5
        reward += 0.1 # time

        if agent_crashed:
            reward = -5000

        return reward


    def reset(self, seed=None, options=None):
        super().reset(seed=seed)

        random_position_start = self.AGENT.get_random_start_pos(self.window_size)
        self.AGENT.reset(random_position_start)
        self._agent_location = self.AGENT.rect.center

        update_position_sensors(self.SENSORS_DATA, self._agent_location, self.AGENT.angle)
        collision_sensors(self.SENSORS_DATA, self.obstacle_group)

        self.stepCounter = 0

        observation = self._get_obs()
        info = {}

        if self.render_mode == "human":
            self.render()

        return observation, info
 


class WithObstacles(BaseEnv):
    def __init__(self, render_mode=None, number_obstacles=0):
        super().__init__()
        
        self.render_mode = render_mode
        self.create_world(number_obstacles=number_obstacles)


    def get_reward(self, agent_crashed, velocity_player):
        reward = velocity_player if velocity_player > 0 else -5
        reward += 0.1 # time

        if agent_crashed:
            reward = -5000

        return reward


    def reset(self, seed=None, options=None):
        super().reset(seed=seed)

        position_to_start = self.AGENT.start_position_with_obstacles(self.window_size, self.obstacle_group)
        self.AGENT.reset(position_to_start)
        self._agent_location = self.AGENT.rect.center

        self.WORLD.reset_obstacles(self.obstacle_group, self.NUM_OBSTACLE_TO_GENERATE)

        update_position_sensors(self.SENSORS_DATA, self._agent_location, self.AGENT.angle)
        collision_sensors(self.SENSORS_DATA, self.obstacle_group)
        
        self.stepCounter = 0

        observation = self._get_obs()
        info = {}

        if self.render_mode == "human":
            self.render()

        return observation, info
    


# IDEA: maybe implement a path where the agent already passed and penalize if the agent re-pass on the same path
# TODO: read me