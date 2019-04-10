class Environment(object):  # environment
    action = 100  # 初始化满发
    state = 200  # 初始化假设另外两个generator也是满发
    parameter = [0.007859, 1.360575, 9490.366, 0.010526, -2.07807, 11128.95, 0.006478, 8.105354,
                 6821.482]  # 3个generators的cost参数

    # demand = 0

    def __init__(self):
        self.state = 200
        self.action = 100

    def apply_action(self, demand, action):
        self.state = demand * 3 - action  # 同比放缩市场demand
        reward = self.get_reward(action)
        return reward, self.state

    def get_reward(self, action):
        i = 1  # generator i
        cost = self.parameter[3 * i - 3] * action ** 2 + self.parameter[3 * i - 2] * action + self.parameter[3 * i - 1]
        price = -0.02775 * action + 108.4096  # price与quantity有关，是个已知的曲线 Utility A
        reward = price * action - cost
        return reward


class Build(object):  # FIS
    list_of_input_variable = []

    def __init__(self, *args):
        self.list_of_input_variable = args

    def get_input(self):
        return self.list_of_input_variable

    def get_number_of_rules(self):
        number_of_rules = 1
        for input_variable in self.list_of_input_variable:
            number_of_rules = (number_of_rules * self.get_number_of_fuzzy_sets(input_variable))
        return number_of_rules

    def get_number_of_fuzzy_sets(self, input_variable):
        return len(input_variable.get_fuzzy_sets())


class InputStateVariable(object):  # StateVariable
    fuzzy_set_list = []

    def __init__(self, *args):
        self.fuzzy_set_list = args

    def get_fuzzy_sets(self):
        return self.fuzzy_set_list


class Triangles(object):  # fuzzy set membership function 有两个，action&state 但是class不影响
    def __init__(self, left, top, right):
        self.left = left
        self.top = top
        self.right = right

    def membership_value(self, input_value):
        if input_value == self.top:
            membership_value = 1.0
        elif input_value <= self.left or input_value >= self.right:
            membership_value = 0.0
        elif input_value < self.top:
            membership_value = (input_value - self.left) / (self.top - self.left)
        elif input_value > self.top:
            membership_value = (input_value - self.right) / (self.top - self.right)
        return membership_value
