import numpy as np


class NeuralNetwork:

    def __init__(self, architecture):
        self.network = []
        for i in range(1, len(architecture)):
            self.network.append(np.zeros((architecture[i - 1] + 1, architecture[i])))

    def feed_forward(self, input_vector):
        for matrix in self.network:
            input_vector = np.array(list(input_vector) + [1])
            input_vector = np.dot(input_vector, matrix)
            input_vector = self.sigmoid(input_vector)
        return input_vector

    @staticmethod
    def sigmoid(vector):
        return 1 / (1 + np.exp(-vector))

    def get_parameters(self):
        parameter_list = np.array([])
        for matrix in self.network:
            parameter_list = np.concatenate((parameter_list, matrix.flatten()))
        return parameter_list

    def set_parameters(self, parameter_list):
        i = 0
        for l_id, layer in enumerate(self.network):
            param_segment = parameter_list[i:layer.size+i]
            self.network[l_id] = param_segment.reshape(layer.shape)
            i += layer.size

    def get_num_params(self):
        return sum([layer.size for layer in self.network])

if __name__ == '__main__':
    nn = NeuralNetwork([3, 2, 1])
    params = nn.get_parameters()
    nn.set_parameters(params/2)
    nn.feed_forward(np.array([1, 0, 0]))

    import time
    start = time.time()
    nn = NeuralNetwork([1000, 500, 1])
    print(f'Instantiation: {time.time() - start} s')
    params = nn.get_parameters()
    print(f'Get params: {time.time() - start} s')
    nn.set_parameters(params / 2)
    print(f'Set params: {time.time() - start} s')

    nn = NeuralNetwork([3, 2, 1])

    def trial_fitness_func(array):
        nn.set_parameters(array)
        l1 = (nn.feed_forward(np.array([1,1,1])) - 1) ** 2
        l2 = (nn.feed_forward(np.array([0,0,0])) - 0) ** 2
        l3 = (nn.feed_forward(np.array([0,1,0])) - 1) ** 2
        l4 = (nn.feed_forward(np.array([1,0,1])) - 0) ** 2
        return 10 - (l1 + l2 + l3 + l4)

    from genetic_algorithm import GeneticAlgorithm
    ga = GeneticAlgorithm(nn.get_num_params(), trial_fitness_func, 100, 100)
    params = ga.evolve()

    nn.set_parameters(params)
    print(nn.feed_forward(np.array([1, 1, 1])))
    print(nn.feed_forward(np.array([0, 0, 0])))
    print(nn.feed_forward(np.array([0, 1, 0])))
    print(nn.feed_forward(np.array([1, 0, 1])))
    print(nn.feed_forward(np.array([1, 1, 0])))
    print(nn.feed_forward(np.array([0, 1, 1])))
