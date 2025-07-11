import numpy as np 
import time
import os 

class GridWorld():
    def __init__(self, 
                 shape=(3, 3), 
                 obstacles=[], 
                 terminal_pos=None, 
                 init_agent_pos=(0,0),
                  #               up     down   left     right
                 action_space=[(-1, 0), (1, 0),(0, -1), (0, 1)]
                 ):
        self.agent_init_pos = init_agent_pos
        self.agent_pos = init_agent_pos
        self.action_space = action_space
        self.rows = shape[0]
        self.cols = shape[1]
        self.obstacles = obstacles
        if terminal_pos == None:
            self.terminal_pos = (self.rows-1, self.cols-1)
        else:
            self.terminal_pos = terminal_pos
        self.done = False

        self.add_pos_action = lambda s, a : tuple(np.array(s) + np.array(a))
        self.is_same_pos = lambda s1, s2 : (np.array(s1)==np.array(s2)).all()

        self.clear = lambda: os.system('cls' if os.name == 'nt' else 'clear')

    def _is_obstacle(self, pos):
        if pos in self.obstacles:
            return True
        return False

    def _is_terminal(self, pos):
        return self.is_same_pos(pos, self.terminal_pos)

    def _is_outside(self, pos):
        if pos[0] < 0 or pos[0] > (self.rows -1) \
            or pos[1] < 0 or pos[1] > (self.cols -1):
            return True
        return False

    def _set_pos(self, pos):
        self.agent_pos = pos

    def _get_pos(self):
        return self.agent_pos

    def _next_pos(self, action):
        next_state = self.add_pos_action(self._get_pos(), action) 
        if self._is_obstacle(next_state) or self._is_outside(next_state):
            return 0
        return 1

    def _game_state(self):
      state = [ self._next_pos(action) for action in self.action_space]
      state.append(self._get_pos()[0])
      state.append(self._get_pos()[1])
      return state
        
    def step(self, action_idx ):
        agent_pos = self._get_pos()
        action = self.action_space[action_idx]
        tmp_pos = self.add_pos_action(agent_pos, action) 
        if self._is_obstacle(tmp_pos):
            pass
        elif self._is_terminal(tmp_pos):
            self._set_pos(tmp_pos)
            self.done = True
        elif self._is_outside(tmp_pos):
            pass
        else:        
            self._set_pos(tmp_pos)
        
        reward = -1 if not self.done else 0

        return self._game_state(), reward, self.done, None

    def reset(self):
        self._set_pos(self.agent_init_pos)
        self.done = False
        return self._game_state(), None

    def render(self, func=None, *args):
        self.clear()
        for r in range(self.rows):
            for c in range(self.cols):
                state = (r, c)
                if self._is_terminal(state):
                    if self.done:
                        print('[O]', end="\t")
                    else:
                        print('[]', end="\t")
                elif  self.is_same_pos(self._get_pos(), state): 
                    print('O', end="\t")
                elif self._is_obstacle(state):
                    print('X', end="\t")
                else:
                    print('-', end="\t")
            print()
            if func != None:
                func(*args)

    def close(self, info=None):
        self.render()
        if info != None:
            print(info)
        print("close")

if __name__ == "__main__":
    env = GridWorld(shape = (5,5), 
                    init_agent_pos=(0,0),
                    terminal_pos=None,
                    obstacles = [(0,1),(1,1), (2,1), (3,1),(2,3),(3,3),(4,3) ])
    state, _ = env.reset()
    env.render()
    state, _ , __, ___ = env.step(1)
    time.sleep(.5)
    env.render()    

    state, _ , __, ___ = env.step(1)
    time.sleep(.5)
    env.render()    

    state, _ , __, ___ = env.step(1)
    time.sleep(.5)
    env.render()    
    
    state, _ , __, ___ = env.step(1)
    time.sleep(.5)
    env.render()    

    state, _ , __, ___ = env.step(3)
    print(state)
    time.sleep(.5)
    env.render()    
