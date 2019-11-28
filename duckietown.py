from gym_duckietown.simulator import Simulator
import numpy as np
from gym import spaces

import logging

logging.getLogger('gym-duckietown').setLevel(logging.ERROR)

logger = logging.getLogger('joystick')
logger.setLevel(logging.DEBUG)

class Duckietown(Simulator):
    """
    Wrapper to control the simulator using velocity and steering angle
    instead of differential drive motor velocities
    """

    def __init__(
        self,
        gain = 1.0,
        trim = 0.0,
        radius = 0.0318,
        k = 27.0,
        limit = 1.0,
        **kwargs
    ):
        Simulator.__init__(self, **kwargs)

        self.action_space = spaces.Box(
            low=np.array([-1,-1]),
            high=np.array([1,1]),
            dtype=np.float32
        )

    def move(self, velocities):
        obs, reward, done, info = Simulator.step(self, np.array(velocities))

        return obs  # , reward, done