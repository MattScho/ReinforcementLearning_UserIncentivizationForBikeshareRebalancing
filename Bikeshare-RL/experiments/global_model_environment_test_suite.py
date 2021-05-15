import sys

# Important for cloud compute
# Change this to the directory that contains the environments directory
sys.path.insert(0, "/home/your-name/Bikeshare-RL")

# Imports
from environment.bss_controller_SADUE_A import BSS_Controller_SADUE_A
from environment.bss_controller_S_A import BSS_Controller_S_A
from environment.bss_controller_S_Aplus import BSS_Controller_S_Aplus
from environment.bss_controller_SApDp_Aplus import BSS_Controller_SApDp_Aplus
from environment.bss_controller_SApDp_AplusDplus import BSS_Controller_SApDp_AplusDplus
import numpy as np
from stable_baselines import PPO2
from stable_baselines.common.policies import MlpPolicy
import time
import pickle as pkl

'''
Experimental Set-Up
'''
# Get env identifier
bss_init_env = "DC_base"
# Load environment
env_settings_init = pkl.load(
    open("../environment/generated_environments/DC_base.pkl", 'rb'))


# Number of steps to apply in training the agent
learnSteps = 250000
# Number of steps to evaluate the agent
evaluationLen = 2400

for budget in [300, 500, 1000, 2000, 4000, 10000]:
    # Number of users per day
    for users in [5000, 10000, 15000]:
        # Total available supply
        for supply in [4500, 3375, 2250, 450]:
            # Environments
            for env, expName in [
                (
                    BSS_Controller_SADUE_A(env_settings_init, budget, users, supply,
                                        open(bss_init_env + "/v1_gamesBudget" + str(budget) + "_" + str(users) + "_" + str(supply)+ ".csv", 'a+'),
                                        open(bss_init_env + "/v1_stepsBudget" + str(budget) + "_" + str(users) + "_" + str(supply)+ ".csv", 'a+')),
                    "v1"
                ),
                (
                    BSS_Controller_S_A(env_settings_init, budget, users, supply,
                                        open(bss_init_env + "/v2_gamesBudget" + str(budget) + "_" + str(users) + "_" + str(supply)+ ".csv", 'a+'),
                                        open(bss_init_env + "/v2_stepsBudget" + str(budget) + "_" + str(users) + "_" + str(supply)+ ".csv", 'a+')),
                    "v2"
                ),
                (
                    BSS_Controller_S_Aplus(env_settings_init, budget, users, supply,
                                        open(bss_init_env + "/v3_gamesBudget" + str(budget) + "_" + str(users) + "_" + str(supply)+ ".csv", 'a+'),
                                        open(bss_init_env + "/v3_stepsBudget" + str(budget) + "_" + str(users) + "_" + str(supply)+ ".csv", 'a+')),
                    "v3"
                ),
                (
                    BSS_Controller_SApDp_Aplus(env_settings_init, budget, users, supply,
                                        open(bss_init_env + "/v4_gamesBudget" + str(budget) + "_" + str(users) + "_" + str(supply)+ ".csv", 'a+'),
                                        open(bss_init_env + "/v4_stepsBudget" + str(budget) + "_" + str(users) + "_" + str(supply)+ ".csv", 'a+')),
                    "v4"
                ),
                (
                    BSS_Controller_SApDp_AplusDplus(env_settings_init, budget, users, supply,
                                        open(bss_init_env + "/v5_gamesBudget" + str(budget) + "_" + str(users) + "_" + str(supply)+ ".csv", 'a+'),
                                        open(bss_init_env + "/v5_stepsBudget" + str(budget) + "_" + str(users) + "_" + str(supply)+ ".csv", 'a+')),
                    "v5"
                )
            ]:
                # Init agent and env
                agent = PPO2(MlpPolicy, env)

                # Time learning
                start = time.time()
                print("Beginning to learn " + expName)

                # Training
                agent.learn(learnSteps)
                print(time.time() - start)
                print("\tDone Learning")
                state = env.reset()

                # Evaluate agent
                for _ in range(evaluationLen):
                    action = agent.predict(state)
                    state, reward, done, info = env.step(action[0])
                    if done:
                        env.reset()
                env.close()

            """
            No Agent
            """
            print("No agent")
            env = BSS_Controller_SADUE_A(env_settings_init, 0, users, supply,
                                         open(bss_init_env + "/noAgent_games_" + str(users) + "_" + str(supply)+".csv", "a+"),
                                         open(bss_init_env + "/noAgent_steps_" + str(users) + "_" + str(supply)+".csv", 'a+'))
            env.reset()
            for _ in range(evaluationLen):
                state, reward, done, info = env.step(np.zeros((100,))) # No incentive

                if done:
                    env.reset()
            env.close()

            '''
            EmpOpt Agent
            '''
            print("Opt agent")
            env = BSS_Controller_SADUE_A(env_settings_init, 1000000, users, supply,
                                         open(bss_init_env + "/opt_games_" + str(users) + "_" + str(supply)+".csv", 'a+'),
                                         open(bss_init_env + "/opt_steps_" + str(users) + "_" + str(supply)+".csv", 'a+'))
            env.reset()
            noAgent = open(bss_init_env + "/opt.csv", "a+")
            env.reset()
            for _ in range(evaluationLen):
                state, reward, done, info = env.step(np.full((100,), 4.0))

                if done:
                    env.reset()
            noAgent.close()
            env.close()
