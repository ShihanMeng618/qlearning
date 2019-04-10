
import numpy as np
import random
import qlearning_env
import sys


class Model(object):
    action_M = []  # 选出来的action的index
    degree_of_truth_action = []
    degree_of_truth_state = []
    state_history = []
    action_history = []
    q_table = np.array([])
    num_of_state_fuzzy_labels = 2  # 要跟run里面的同步改
    num_of_action_fuzzy_labels = 3  # 要跟run里面的同步改

    def __init__(self, gamma, alpha, ee_rate, q_initial_value, action_top, fis1 = qlearning_env.Build(), fis2 = qlearning_env.Build()):
        self.gamma = gamma
        self.alpha = alpha
        self.ee_rate = ee_rate
        self.action_top = action_top
        self.q_initial_value = q_initial_value
        self.fis1 = fis1  # state
        self.fis2 = fis2  # action
        if self.q_initial_value == "random":
            self.q_table = np.random.random((self.num_of_state_fuzzy_labels, self.num_of_action_fuzzy_labels))
        if self.q_initial_value == "zero":
            self.q_initial_value = np.zeros((self.num_of_state_fuzzy_labels, self.num_of_action_fuzzy_labels))

    def CalculateTruthValueState(self,state_value):  # membership of state
        self.degree_of_truth_state = []
        input_variable = self.fis1.list_of_input_variable
        for index, variable in enumerate(input_variable):
            S = []
            fuzzy_sets = variable.get_fuzzy_sets()
            for set in fuzzy_sets:
                membership_value = set.membership_value(state_value)
                S.append(membership_value)
            self.degree_of_truth_state.append(S)

    def CalculateTruthValueAction(self,action_value): # membership of action
        self.degree_of_truth_action = []
        input_variable = self.fis2.list_of_input_variable
        for index, variable in enumerate(input_variable):
            A = []
            fuzzy_sets = variable.get_fuzzy_sets()
            for set in fuzzy_sets:
                membership_value = set.membership_value(action_value)
                A.append(membership_value)
            self.degree_of_truth_action.append(A)

    def ActionSelection(self):  # epsilon-greedy 每一行的最大值放在action_M里面遍历整个q_table
        self.action_M = []
        r = random.uniform(0,1)
        max = -sys.maxsize
        for rull in self.q_table:  # rull一行
            if r < self.ee_rate:
                for index, action in enumerate(rull):
                    if action > max:  # 选一个最大的q值
                        action_index = index
            else:
                action_index = random.randint(0, self.num_of_action_fuzzy_labels-1)
            self.action_M.append(action_index)

    def InferredAction(self):  # 多个状态合成一个action
        action = 0
        for i in range(0, self.num_of_state_fuzzy_labels):
            action = action + self.degree_of_truth_state[0][i] * self.action_M[i] * (i+1) * self.action_top
            # action_label怎么对应到action
        return action

    def UpdateqValue(self, reward):
        for state_index in range(0, self.num_of_state_fuzzy_labels):
            for action_index in range(0, self.num_of_action_fuzzy_labels):
                temp = self.q_table[state_index, action_index]
                Q_new = (1 - self.alpha) * temp + self.alpha * reward * self.degree_of_truth_state[0][state_index] * \
                        self.degree_of_truth_action[0][action_index]
                self.q_table[state_index, action_index] = Q_new

    def KeepStateHistory(self):
        self.state_history.append(self.degree_of_truth_state)

    def KeepActionHistory(self):
        self.action_history.append(self.degree_of_truth_action)

    def run(self, state, reward, quantity):
        self.CalculateTruthValueState(state)
        self.CalculateTruthValueAction(quantity)
        self.UpdateqValue(reward)
        self.ActionSelection()
        action = self.InferredAction()
        self.KeepStateHistory()
        self.KeepActionHistory()
        return action

    def get_initial_action(self, state):
        self.CalculateTruthValueState(state)
        self.ActionSelection()
        action = self.InferredAction()
        self.KeepStateHistory()
        self.KeepActionHistory()
        return action


















