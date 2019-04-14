# qlearning

In a incomplete information game, a big challenge is to find the best way of exploiting available information for optimal decision making of agents. This project implements repeated Cournot competition of the generators in a day-ahead electricity market using reinforcement learning.

该项目实现了基于强化学习Qlearning的古诺模型下的电力市场发电商竞价策略的选择。

算法流程如下：

1. 初始化state = Demand(t) - q(t-1) ，模糊得到S~j~(fuzzy_labels)
2. 根据q_table S~j~的一行选max的action的A~k~(fuzzy_labels)——原始策略，其中A~k~(fuzzy_labels)如何变成一个连续性的quantity值？
3. 得到reward， next_state
4. 根据reward update q_table
5. 基于$\epsilon-greedy$ or softmax 进行决策
6. 考虑到多个状态S~j~, $q^*(t)=\sum_{j=1}^{M}S_jq_j(t)$
7. 得到reward^'^,next_state^'^, 重复

> 参考文献：Model-Based and Learning-Based Decision Making in Incomplete Information Cournot Games: A state Estimation Approach

参考：[seyedsaeidmasoumzadeh/Fuzzy-Q-Learning](https://github.com/seyedsaeidmasoumzadeh/Fuzzy-Q-Learning)

