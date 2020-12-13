# -*- coding:utf-8 -*-

import numpy as np
from operator import itemgetter
from TDNN import TNN
import copy
from TDNN import *


class Genetic(object):
    def __init__(self):
        self.nb_layers = range(3, 7)
        self.nb_nodes = [4, 8, 16, 32, 64, 84, 96, 128, 196, 256, 324, 420, 512, 720, 960, 1024]
        self.optimizers = ["Adam", "Adagrad", "Adadelta", "RMSProp", "sgd"]
        self.activations = ["relu", "sigmoid", "tanh"]
        self.nb_leaf_input = range(2, 10)
        self.param_choices = ['leaf_input_num',
                              'leaf_layer_num', 'leaf_layer_dims', 'leaf_activations',
                              'aggre_layer_num', 'aggre_layer_dims', 'aggre_activations',
                              'root_layer_num', 'root_layer_dims', 'root_activations',
                              'optimizer']

    def create_population(self, strength):
        '''
        :param strength: number of members in the generation, each member with parameters
        :return: members
        parameters:
           # leaf_NN_num
           # leaf_last_input_num: 等于num_leaf_input说明每个NN输入相同，不同时则说明总特征数不能整除每个NN特征数
            leaf_input_num
            leaf_layer_num
            leaf_layer_dims
            leaf_activations

          # aggre_NN_num
          #   aggre_input_num
            aggre_layer_num
            aggre_layer_dims
            aggre_activations

            root_layer_num
            root_layer_dims
            root_activations

            optimizer
        '''
        members = []
        for _ in range(strength):
            parameters = dict()
            num_leaf_input = np.random.choice(self.nb_leaf_input)  # leaf NN的输入特征数
            # num_leaf_NN = np.ceil(INPUT_TOTAL_NUM/num_leaf_input)  # leaf NN的数量
            # parameters['num_leaf_NN'] = num_leaf_NN
            parameters['leaf_input_num'] = num_leaf_input  # leaf NN的输入特征数量
            # num_leaf_last_input = INPUT_TOTAL_NUM % num_leaf_input  # 最后一个leaf NN的输入特征数量
            # if num_leaf_last_input == 0:
            #     num_leaf_last_input = num_leaf_input
            # parameters['num_leaf_last_input'] = num_leaf_last_input
            num_leaf_layer = np.random.choice(self.nb_layers)  # leaf NN的网络层数
            parameters['leaf_layer_num'] = num_leaf_layer
            parameters['leaf_layer_dims'] = list()  # leaf NN每一层节点数
            parameters['leaf_activations'] = list()  # leaf NN每一层使用的激励函数
            for _ in range(1, num_leaf_layer-1):
                num_nodes = np.random.choice(self.nb_nodes)
                activation = np.random.choice(self.activations)
                parameters['leaf_layer_dims'].append(num_nodes)
                parameters['leaf_activations'].append(activation)
            # leaf NN的output层
            parameters['leaf_layer_dims'].append(LEAF_OUTPUT_NUM)
            parameters['leaf_activations'].append("None")

            # Aggregation NN
            # parameters['aggre_input_num'] = AGGREGATION_INPUT  # AL的输入特征数
            # parameters['aggre_NN_num'] = num_leaf_NN / AGGREGATION_INPUT  # AL的NN数
            num_aggre_layer = np.random.choice(self.nb_layers)  # AL NN的网络层数
            parameters['aggre_layer_num'] = num_aggre_layer
            parameters['aggre_layer_dims'] = list()  # AL NN每一层的节点数
            parameters['aggre_activations'] = list()  # AL NN每一层使用的激励函数
            for _ in range(1, num_aggre_layer-1):
                num_nodes = np.random.choice(self.nb_nodes)
                activation = np.random.choice(self.activations)
                parameters['aggre_layer_dims'].append(num_nodes)
                parameters['aggre_activations'].append(activation)
            # Aggregation NN的output层
            parameters['aggre_layer_dims'].append(AGGREGATION_OUTPUT_NUM)
            parameters['aggre_activations'].append("None")

            # Root NN
            root_layer_num = np.random.choice(self.nb_layers)
            parameters['root_layer_num'] = root_layer_num
            parameters['root_layer_dims'] = list()
            parameters['root_activations'] = list()
            for _ in range(1, root_layer_num-1):
                num_nodes = np.random.choice(self.nb_nodes)
                activation = np.random.choice(self.activations)
                parameters['root_layer_dims'].append(num_nodes)
                parameters['root_activations'].append(activation)
            parameters['root_layer_dims'].append(ROOT_OUTPUT_NUM)
            parameters['root_activations'].append('None')
            # 整个神经网络的优化函数
            parameters['optimizer'] = np.random.choice(self.optimizers)
            members.append(parameters)
        return members

    # 遗传算法的培育操作
    def breed(self, mother, father, K=1):
        '''
        :param mother: parameters dictionary of a neural net
        :param father: parameters dictionary of another neural net
        :param K: number of children required
        :return: children
        '''
        children = []
        for _ in range(K):
            child = dict()
            # 1：决定leaf NN的输入特征数
            m_leaf_input_num = mother['leaf_input_num']
            f_leaf_input_num = father['leaf_input_num']
            child['leaf_input_num'] = np.random.choice([m_leaf_input_num, f_leaf_input_num])
            # 2: 决定leaf NN的网络层数
            m_leaf_layer_num = mother['leaf_layer_num']
            f_leaf_layer_num = father['leaf_layer_num']
            child['leaf_layer_num'] = np.random.choice([m_leaf_layer_num, f_leaf_layer_num])
            max_leaf_layer_num = np.max([m_leaf_layer_num, f_leaf_layer_num])
            if m_leaf_layer_num == max_leaf_layer_num:
                p_dom = mother
            else:
                p_dom = father
            if child['leaf_layer_num'] == max_leaf_layer_num:
                # inherit the fixed leaf parameters
                child['leaf_layer_dims'] = p_dom['leaf_layer_dims']
                child['leaf_activations'] = p_dom['leaf_activations']
            else:
                # inherit randomly
                inherit = np.random.choice([mother, father])
                child['leaf_layer_dims'] = inherit['leaf_layer_dims'][:child['leaf_layer_num']-1]
                inherit = np.random.choice([mother, father])
                child['leaf_activations'] = inherit['activations'][:child['leaf_layer_num']-1]
                child['leaf_layer_dims'].append(LEAF_OUTPUT_NUM)
                child['leaf_activations'].append('None')
            # 3: 决定aggregation NN的网络层数
            m_aggre_layer_num = mother['aggre_layer_num']
            f_aggre_layer_num = father['aggre_layer_num']
            child['aggre_layer_num'] = np.random.choice([m_aggre_layer_num, f_aggre_layer_num])
            max_aggre_layer_num = np.max([m_aggre_layer_num, f_aggre_layer_num])
            if m_aggre_layer_num == max_aggre_layer_num:
                p_dom = mother
            else:
                p_dom = father
            if child['aggre_layer_num'] == max_aggre_layer_num:
                child['aggre_layer_dims'] = p_dom['aggre_layer_dims']
                child['aggre_activations'] = p_dom['aggre_activations']
            else:
                inherit = np.random.choice([mother, father])
                child['aggre_layer_dims'] = inherit['aggre_layer_dims'][:child['aggre_layer_num'] - 1]
                inherit = np.random.choice([mother, father])
                child['aggre_activations'] = inherit['aggre_activations'][:child['aggre_layer_num'] - 1]
                child['aggre_layer_dims'].append(AGGREGATION_OUTPUT_NUM)
                child['aggre_activations'].append('None')
            # 4: 决定root NN的网络层数
            m_root_layer_num = mother['root_layer_num']
            f_root_layer_num = father['root_layer_num']
            child['root_layer_num'] = np.random.choice([m_root_layer_num, f_root_layer_num])
            max_root_layer_num = np.max([m_root_layer_num, f_root_layer_num])
            if m_root_layer_num == max_root_layer_num:
                p_dom = mother
            else:
                p_dom = father
            if child['root_layer_num'] == max_root_layer_num:
                child['root_layer_dims'] = p_dom['root_layer_dims']
                child['root_activations'] = p_dom['root_activations']
            else:
                inherit = np.random.choice([mother, father])
                child['root_layer_dims'] = inherit['root_layer_dims'][:child['root_layer_num'] - 1]
                inherit = np.random.choice([mother, father])
                child['root_activations'] = inherit['root_activations'][:child['root_layer_num'] - 1]
                child['root_layer_dims'].append(ROOT_OUTPUT_NUM)
                child['root_activations'].append('None')
            child['optimizer'] = np.random.choice([mother['optimizer'], father['optimizer']])
            children.append(child)
        return children

    # 遗传算法的变异操作
    def mutate(self, nn_parameters):
        '''
        randomly mutate parameters of the NN
        :param nn_parameters: dict of parameters of the network
        :return: nn_parameters after mutating
        '''
        layer_num_list = ['leaf_layer_num', 'aggre_layer_num', 'root_layer_num']
        layer_dims_list = ['leaf_layer_dims', 'aggre_layer_dims', 'root_layer_dims']
        layer_activations_list = ['leaf_activations', 'aggre_activations', 'root_activations']
        param_to_be_mutated = np.random.choice(self.param_choices)
        # leaf input num
        if param_to_be_mutated == 'leaf_input_num':
            new_leaf_input_num = np.random.choice(self.nb_leaf_input)
            nn_parameters['leaf_input_num'] = new_leaf_input_num
        # layer num
        elif param_to_be_mutated in layer_num_list:
            new_layer_num = np.random.choice(self.nb_layers)
            layer_name = param_to_be_mutated.split('_')[0]
            if new_layer_num > nn_parameters[param_to_be_mutated]:
                for _ in range(new_layer_num - nn_parameters[param_to_be_mutated] - 1):
                    nodes_num = np.random.choice(self.nb_nodes)
                    nn_parameters[layer_name + '_layer_dims'].append(nodes_num)
                    activation = np.random.choice(self.activations)
                    nn_parameters[layer_name + '_activations'].append(activation)
            else:
                nn_parameters[layer_name + '_layer_dims'] = nn_parameters[layer_name + '_layer_dims'][:new_layer_num]
                nn_parameters[layer_name + '_activations'] = nn_parameters[layer_name + '_activations'][:new_layer_num]
            if layer_name == 'leaf':
                nn_parameters[layer_name + '_layer_dims'].append(LEAF_OUTPUT_NUM)
            elif layer_name == 'aggre':
                nn_parameters[layer_name + '_layer_dims'].append(AGGREGATION_OUTPUT_NUM)
            elif layer_name == 'root':
                nn_parameters[layer_name + '_layer_dims'].append(ROOT_OUTPUT_NUM)
            nn_parameters['leaf_activations'].append('None')
            nn_parameters[param_to_be_mutated] = new_layer_num
        # optimizer
        elif param_to_be_mutated == 'optimizer':
            nn_parameters['optimizer'] = np.random.choice(self.optimizers)
        # layer dims or activations
        else:
            # choose a random index and modify its nodes_num or activation
            layer_name = param_to_be_mutated.split('_')[0]
            index = int(np.random.random() * nn_parameters[layer_name + '_layer_num'])
            if param_to_be_mutated in layer_dims_list:
                new_attr = np.random.choice(self.nb_nodes)
            else:
                new_attr = np.random.choice(self.activations)
            nn_parameters[param_to_be_mutated][index] = new_attr
        return nn_parameters

    def evolve(self, population, retain=0.25, select=0.15, mutation=0.15):
        # get fitness scores for all members
        trained_pop = [(self.evaluate_fitness(member, model_name='population_'+str(i)), member)
                       for i, member in enumerate(population)]
        # arrange members according to their fitness scores
        sorted_scores = sorted(trained_pop, key=itemgetter(0))
        fittest_members = [pair[1] for pair in sorted_scores]
        accuracy_scores = [pair[0] for pair in sorted_scores]
        # retain some members for next generation
        retain_length = int(retain * len(fittest_members))
        parents = fittest_members[:retain_length]
        # randomly add some low performing networks
        for member in fittest_members[retain_length:]:
            if np.random.random() < select:
                parents.append(member)
        # time to make babies
        # for now, preserve the strength of population
        nb_babies = len(population) - len(parents)
        children = []
        while len(children) < nb_babies:
            K = 1 + int(3 * np.random.random())
            mother = np.random.choice(parents)
            father = None
            while not father == mother:
                father = np.random.choice(parents)
            # now breed
            babies = self.breed(mother, father, K)
            for baby in babies:
                # randomly mutate a baby
                if np.random.random() < mutation:
                    baby = self.mutate(baby)
                if len(children) < nb_babies:
                    children.append(baby)
            # we have evolved
        parents.extend(children)
        return accuracy_scores, parents

    def evaluate_fitness(self, nn_parameters=None, model_name=None):
        nn = TNN.TNN(nn_parameters)
        r2_value = nn.build_model(model_name)
        return 100 * r2_value









