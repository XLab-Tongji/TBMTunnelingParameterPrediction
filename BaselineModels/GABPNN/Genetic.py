# -*- coding:utf-8 -*-

from operator import itemgetter
from BaselineModels.GABPNN import BPNN
from BaselineModels.GABPNN import *


class Genetic(object):
    def __init__(self):
        self.nb_layers = range(3, 7)
        self.nb_nodes = [4, 8, 16, 32, 64, 84, 96, 128, 196, 256, 324, 420, 512, 720, 960, 1024]
        self.optimizers = ["Adam", "Adagrad", "Adadelta", "RMSProp", "sgd"]
        self.activations = ["relu", "sigmoid", "tanh"]
        self.param_choices = ['layer_num', 'layer_dims', 'activations','optimizer']

    def create_population(self, strength):
        '''
        :param strength: number of members in the generation, each member with parameters
        :return: members
        parameters:
            layer_num
            layer_dims
            activations
            optimizer
        '''
        members = []
        for _ in range(strength):
            parameters = dict()
            num_layer = np.random.choice(self.nb_layers)  # BPNN的网络层数
            parameters['layer_num'] = num_layer
            parameters['layer_dims'] = list()  # BPNN每一层节点数
            parameters['activations'] = list()  # BPNN每一层使用的激励函数
            for _ in range(1, num_layer-1):
                num_nodes = np.random.choice(self.nb_nodes)
                activation = np.random.choice(self.activations)
                parameters['layer_dims'].append(num_nodes)
                parameters['activations'].append(activation)
            # leaf NN的output层
            parameters['layer_dims'].append(OUTPUT_NUM)
            parameters['activations'].append("None")
            # 整个神经网络的优化函数
            parameters['optimizer'] = np.random.choice(self.optimizers)
            # 加入到种群
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
            # 决定NN的网络层数、网络结构、激活函数、优化器
            m_layer_num = mother['layer_num']
            f_layer_num = father['layer_num']
            child['layer_num'] = np.random.choice([m_layer_num, f_layer_num])
            max_layer_num = np.max([m_layer_num, f_layer_num])
            if m_layer_num == max_layer_num:
                p_dom = mother
            else:
                p_dom = father
            if child['layer_num'] == max_layer_num:
                # inherit the fixed parameters
                child['layer_dims'] = p_dom['layer_dims']
                child['activations'] = p_dom['activations']
            else:
                # inherit randomly
                inherit = np.random.choice([mother, father])
                child['layer_dims'] = inherit['layer_dims'][:child['layer_num']-1]
                inherit = np.random.choice([mother, father])
                child['activations'] = inherit['activations'][:child['layer_num']-1]
                child['layer_dims'].append(OUTPUT_NUM)
                child['activations'].append('None')

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
        param_to_be_mutated = np.random.choice(self.param_choices)
        # layer num
        if param_to_be_mutated =='layer_num':
            new_layer_num = np.random.choice(self.nb_layers)
            if new_layer_num > nn_parameters[param_to_be_mutated]:
                for _ in range(new_layer_num - nn_parameters[param_to_be_mutated] - 1):
                    nodes_num = np.random.choice(self.nb_nodes)
                    nn_parameters['layer_dims'].append(nodes_num)
                    activation = np.random.choice(self.activations)
                    nn_parameters['activations'].append(activation)
            else:
                nn_parameters['layer_dims'] = nn_parameters['layer_dims'][:new_layer_num]
                nn_parameters['activations'] = nn_parameters['activations'][:new_layer_num]
            nn_parameters['layer_dims'].append(OUTPUT_NUM)
            nn_parameters['activations'].append('None')
            nn_parameters[param_to_be_mutated] = new_layer_num
        # optimizer
        elif param_to_be_mutated == 'optimizer':
            nn_parameters['optimizer'] = np.random.choice(self.optimizers)
        # layer dims or activations
        else:
            # choose a random index and modify its nodes_num or activation
            layer_name = param_to_be_mutated.split('_')[0]
            index = int(np.random.random() * nn_parameters['layer_num'])
            if param_to_be_mutated =="layer_dims":
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
        nn = BPNN.BPNN(nn_parameters)
        r2_value = nn.build_model(model_name)
        return 100 * r2_value









