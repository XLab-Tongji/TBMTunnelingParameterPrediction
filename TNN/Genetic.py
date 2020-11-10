# -*- coding:utf-8 -*-

import numpy as np
from operator import itemgetter
import sys
# sys.path.append('/Users/shuangliz/Desktop/TBMTunnelingParameterPrediction/TNN/TNN.py')

from TNN import TNN

INPUT_SIZE = 784
OUTPUT_SIZE = 10


class Genetic(object):
    '''
    Class to implement genetic algorithm on neural network architecture
    '''
    def __init__(self):
        '''
        Instantiates:
            nb_layers: a list having all possible number of hidden layers
                        in our network
            nb_nodes : a list having all possible number of nodes in each
                        hidden layer in our network
        '''
        self.param_choices = ["nb_layers", "nb_nodes", "activations", "optimizers"]
        self.nb_layers = range(3, 7)
        self.nb_nodes = [4, 8, 16, 32, 64, 84, 96, 128, 196, 256, 324, 420, 512, 720, 960, 1024]
        self.optimizers = ["Adam", "Adagrad", "Adadelta", "Momentum", "RMSProp", "sgd"]
        self.activations = ["relu", "sigmoid", "elu", "leaky_relu", "tanh"]

    def create_population(self, strength):
        '''
        Creates a random population in the generation.
        @input:
            strength: number of members in the generation, each member with parameters as follows
        parameters:
            nb_layers: int, number of the layers
            layer_dims: list, the dim of each layer
            activations: list, the AF of each layer
            optimizer: the OP of the NN
        '''
        members = []
        for _ in range(strength):
            # create a random neural net architecture
            nb_layers = np.random.choice(self.nb_layers)
            parameters = dict()
            parameters["nb_layers"] = nb_layers
            parameters["layer_dims"] = list()
            parameters["activations"] = list()
            # input layer
            parameters["layer_dims"].append(INPUT_SIZE)
            parameters["activations"].append("None")
            for _ in range(1, nb_layers - 1):
                nb_node = np.random.choice(self.nb_nodes)
                activation = np.random.choice(self.activations)
                parameters["layer_dims"].append(nb_node)
                parameters["activations"].append(activation)
            # output layer
            parameters["layer_dims"].append(OUTPUT_SIZE)
            parameters["activations"].append("None")
            parameters["optimizer"] = np.random.choice(self.optimizers)
            members.append(parameters)
        return members

    def breed(self, mother, father, K=1):
        '''
        create K children network by mixing parameters of mother and father
        @input:
            mother: parameters dictionary of a neural net
            father: parameters dictionary of another neural net
            K: No. of children required
        '''
        children = []
        for _ in range(K):
            child = dict()
            # decide nb_layers first
            m_nb_layers = mother["nb_layers"]
            f_nb_layers = father["nb_layers"]
            child["nb_layers"] = np.random.choice(
                            [m_nb_layers, f_nb_layers]
                        )
            # decide the dominant parent
            nb_layers_max = np.max([m_nb_layers, f_nb_layers])
            if nb_layers_max == m_nb_layers:
                p_dom = mother
            else:
                p_dom = father
            if child["nb_layers"] == nb_layers_max:
                # inherit nodes and activations from the dominant parent
                # TODO: define a dominancy factor and choose according to it
                child["layer_dims"] = p_dom["layer_dims"]
                child["activations"] = p_dom["activations"]
            else:
                # inherit randomly
                inherit = np.random.choice([mother, father])
                child["layer_dims"] = inherit["layer_dims"][:child["nb_layers"]-1]
                inherit = np.random.choice([mother, father])
                child["activations"] = inherit["activations"][:child["nb_layers"]-1]
                # take care of the last output layer
                child["layer_dims"].append(OUTPUT_SIZE)
                child["activations"].append("None")
            child["optimizer"] = np.random.choice(
                                    [mother["optimizer"], father["optimizer"]]
                                 )
            children.append(child)

        return children

    def mutate(self, nn_parameters):
        '''
        randomly mutate parameters of the nn
        @input:
            nn_parameters: dictionary of parameters of the network
        '''
        param_to_be_mutated = np.random.choice(self.param_choices)
        if param_to_be_mutated == "nb_layers":
            new_nb_layers = np.random.choice(self.nb_layers)
            if new_nb_layers > nn_parameters["nb_layers"]:
                # pick random number of nodes for the new layers
                for _ in range(new_nb_layers - nn_parameters["nb_layers"] - 1):
                    nb_node = np.random.choice(self.nb_nodes)
                    nn_parameters["layer_dims"].append(nb_node)
                    activation = np.random.choice(self.activations)
                    nn_parameters["activations"].append(activation)
                # take care of last output layer
                nn_parameters["layer_dims"].append(OUTPUT_SIZE)
                nn_parameters["activations"].append("None")
            else:
                # select a subarray of size `new_nb_layers` for each
                # parameter from the beginning
                nn_parameters["layer_dims"] = nn_parameters["layer_dims"][:new_nb_layers]
                nn_parameters["activations"] = nn_parameters["activations"][:new_nb_layers]
            nn_parameters["nb_layers"] = new_nb_layers
        elif param_to_be_mutated == "optimizer":
            nn_parameters["optimizer"] = np.random.choice(self.optimizers)
        else:
            # choose a random index and modify its nb_node or activation
            index = int(np.random.random() * nn_parameters["nb_layers"])
            if param_to_be_mutated == "activations":
                new_attr = np.random.choice(self.activations)
            else:
                new_attr = np.random.choice(self.nb_nodes)
            nn_parameters[param_to_be_mutated][index] = new_attr

        return nn_parameters

    def evolve(self, population, retain=0.25, select=0.15, mutation=0.15):
        '''
        Train all members of the population and evolve based on their fitness
        This function mutates and breeds new babies.
        @input:
            population: a list of parameter dictionaries of all members
        '''
        # get fitness scores for all members
        trained_pop = [(self.evaluate_fitness(member), member)
                    for member in population]
        # arrange members according to their fitness scores
        sorted_scores = sorted(trained_pop, key=itemgetter(0))
        fittest_members = [pair[1] for pair in sorted_scores]
        accuracy_scores = [pair[0] for pair in sorted_scores]

        #retain some members for next generation
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
            # decide number of babies for a pair of parents randomly
            # TODO: Give more babies to fitter parents
            K = 1 + int(3 * np.random.random())
            # get random mom & dad(not both identical)
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

    def evaluate_fitness(self, nn_parameters=None):
        # The nn_parameters here is a member of the population
        # nn = NeuralNetwork(nn_parameters)
        nn = TNN()
        # accuracy = nn.run_model(num_epochs=25, batch_size=100)
        # # accuracy is the fitness score of network
        # return accuracy * 100


if __name__ == '__main__':
    genome = Genetic()
    genome.evaluate_fitness()