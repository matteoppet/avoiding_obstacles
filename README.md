# Obstacle avoidance agent
This project is developed in a custom [Gym](https://www.gymlibrary.dev/content/basic_usage/) environment and with [Pygame](https://www.pygame.org/wiki/about) to help to visualize the agent and the environment. The goal of this agent is to avoid some n obstacles with helping himself with sensors all around the agent, the obstacles positions are random generated also as the agent position.


## How the obstacles are random generated
The obstacles random positions has some criteria to respect: <br>
1. Does not have to spawn on a position already taken
2. Each obstacles needs to be at least 200 pixels from eachother
   - calculated from the center of each obstacles
3. Does not have to collide with any other obstacles


## Prerequisites
To install the requirements for the project run
``` bash
pip install -r requirements.txt
```

## Training
In `train.py` file, set the **HYPER PARAMETERS** as your choice then train the agent by running
``` bash
python train.py
```
File of the model is saved in this location `trained_agent/models/PPO_MODELS`


## Contributing
Feel free to contribute on get the code works better or some new features to implement.
Any contributions you make are **greatly appreaciated**.