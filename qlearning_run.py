import qlearning_brain
import qlearning_env
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from scipy.linalg import solve


num_of_generators = 3
S_max = 300  # MW
S_min = 0  # MW
num_of_S_fuzzy_labels = 2
A_max = 100  # MW 假设不能超过满发
A_min = 0  # MW
num_of_A_fuzzy_labels = 3


# Import demand & price
file1 = open('D:/0毕设/data/demand/demand.csv')
demand_table = pd.read_csv(file1)
# file2 = open('D:/0毕设/data/price/price.txt')
# price_table = pd.read_csv(file2)
# demand.ix[0,1] 来表示每一个值

# Create FIS
# state
input_variable_state = []
for num in range(0, num_of_S_fuzzy_labels):
    input_variable_state.append(qlearning_env.Triangles(num*S_max/(num_of_S_fuzzy_labels+1),(num+1)*S_max/(num_of_S_fuzzy_labels+1),
                                                        (num+2)*S_max/(num_of_S_fuzzy_labels+1)))
s = qlearning_env.InputStateVariable(*input_variable_state)
fis_s = qlearning_env.Build(s)

# action
input_variable_action = []
for num in range(0, num_of_A_fuzzy_labels):
    input_variable_action.append(qlearning_env.Triangles(num*A_max/(num_of_A_fuzzy_labels+1),(num+1)*A_max/(num_of_A_fuzzy_labels+1),
                                                        (num+2)*A_max/(num_of_A_fuzzy_labels+1)))
a = qlearning_env.InputStateVariable(*input_variable_action)
fis_a = qlearning_env.Build(a)
action_top = A_max/(num_of_A_fuzzy_labels+1)

# create model
model = qlearning_brain.Model(gamma=0.9, alpha=0.1, ee_rate=0.999, action_top = action_top, q_initial_value='random',fis1=fis_s, fis2 = fis_a)
env = qlearning_env.Environment()

state_record = []  # 记录用来画图
action_record = [] # 记录用来画图
action_temp_record = []
nash_record = []
reward_record = []
# 初始化
action = model.get_initial_action(env.state)
action_temp = action  # action_temp画迭代图
action_record.append(action)
action_temp_record.append(action_temp)

# nash
rho = 0.0206
theta = 106.1176
phi_a = 0.015718
phi_b = 0.021052
phi_c = 0.012956
gamma_a = 1.360575
gamma_b = -2.07807
gamma_c = 8.105354
A = np.array([[2*rho+phi_a, rho, rho], [rho, 2*rho+phi_b, rho], [rho, rho, 2*rho+phi_c]])
B = np.array([theta-gamma_a, theta-gamma_b, theta-gamma_c])
x = solve(A,B)
x = x/np.sum(x)
print(x)

for i in range(0,1872): # 1872
    demand_current = demand_table.ix[(i // 24) , i % 24 + 2]  # x1
    nash_record.append(x[0]*demand_current*3) # nash均衡

    for j in range(0,200):  # 迭代200次
        reward_temp, state_value_temp = env.apply_action(demand_current,action_temp)
        action_temp = model.run(state_value_temp, reward_temp, action_temp_record[j])  # 上一个action
        action_temp_record.append(action_temp)

    reward = reward_temp
    state_value = state_value_temp
    action = action_temp
    reward_record.append(reward)
    state_record.append(state_value)
    action_record.append(action)

    # reward, state_value = env.apply_action(demand_current, action)
    # reward_record.append(reward)
    # state_record.append(state_value)
    # action = model.run(state_value, reward,action_record[i]) # 上一个action
    # action_record.append(action)

    # 看中间迭代过程
    if i % 100 == 0:
        x0 = np.arange(0, 201, 1)
        y5 = np.array(action_temp_record)
        y6 = np.full(201, nash_record[i])
        plt.figure()
        plot3, = plt.plot(x0, y5, 'r')
        plot4, = plt.plot(x0, y6,'b--')
        l2 = plt.legend([plot3, plot4], ["RL", "Nash"], loc='upper right')
        plt.savefig("./result0410/" + str(i) + ".png")
        print(i)
        # plt.show()

    action_temp_record.clear()
    action_temp_record.append(action_record[i+1])  # 当前结果为下一迭代过程的初始值

x1 = np.arange(0,1873,1)
x2 = np.arange(0,1872,1)
y1 = np.array(action_record)
y2 = np.array(state_record)
y3 = np.array(reward_record)
y4 = np.array(nash_record)

# 最后结果
plt.figure()
plot1, = plt.plot(x1,y1,'r')
plot2, = plt.plot(x2,y4,'b--')
l1 = plt.legend([plot1, plot2], ["RL", "Nash"], loc='upper right')

plt.savefig("./result0410/00.png")
plt.show()





