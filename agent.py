import random
import numpy as np


class Agent:

    def __init__(self, n_words, n_dimensions, seed, n_exemplars, n_continuers, wedel_start, collateral_index):
        """
        Initialisation of the agent class.
        :param n_words: int; the number of word categories contained in the lexicons of the agents
        :param n_dimensions: int; the number of dimensions of the exemplars
        :param seed: int; the seed used to produce the means for sampling the word categories
        :param n_exemplars: int; the number of exemplars per word category
        :param n_continuers: int; the number of continuer v_words in the lexicon
        :param wedel_start: boolean; whether the means for initialising the lexicon are based on the one used in Wedel's
        model
        """

        self.n_words = n_words
        self.n_dimensions = n_dimensions
        self.seed = seed
        self.n_exemplars = n_exemplars
        self.n_continuers = n_continuers
        self.wedel_start = wedel_start
        self.collateral_index = collateral_index

    def generate_lexicon(self):
        """
        Generate a lexicon containing v_words, which in turn contains n_exemplar exemplars.
        :return: list; a list of words, for which each word consists of a list of exemplars, which in turn is a
                       list of the number of dimensions floats
                 list; a list containing the regular vocabulary words
                 list; a list containing the continuers
                 list; a list containing the indices of the continuers in the lexicon
        """

        # If a seed was provided, set the seed
        if self.seed:
            random.seed(self.seed)

        # Create a lexicon consisting of n_words v_words each in turn consisting of n_exemplars exemplars
        lexicon = []

        # The means of the starting condition of the v_words used in Wedel's paper
        means = [[20, 80], [40, 40], [60, 60], [80, 20]]

        means_collateral = [[20, 20], [40, 70], [50, 90], [55, 25], [80, 42], [10, 60], [90, 70], [70, 85], [40, 15],
                            [18, 50]]

        for w in range(self.n_words - self.n_continuers):
            word = []

            # Define the mean and the covariance to sample from a multivariate normal distribution to create clustered
            # exemplars for the v_words

            if self.wedel_start:
                mean = means[w]
            else:
                mean = [random.randrange(10, 91) for i in range(self.n_dimensions)]

            cov = [[10, 0], [0, 10]]
            x, y = np.random.multivariate_normal(mean, cov, self.n_exemplars).T
            word.append(list(map(lambda x, y: [x, y], x, y)))

            # Initialise all v_words as regular vocabulary words ('V')
            lexicon.append([word[0], "V"])

        # Split the lexicon into continuers and regular vocabulary words if applicable
        indices_continuer = False
        if self.n_continuers:

            # # If the number of continuer v_words is bigger than the number of v_words in the lexicon raise an error
            # # message
            # if self.n_continuers > self.n_words:
            #     raise ValueError("The number of continuers must be lower than the number of v_words.")
            #
            # # The continuers are randomly chosen out of the lexicon
            # indices_continuer = random.sample(range(self.n_words), k=self.n_continuers)
            #
            continuer_words = []
            # for index in indices_continuer:
            #     lexicon[index][1] = "C"

            if self.collateral_index > 9:
                self.collateral_index = self.collateral_index - 10
            continuer = []
            mean = means_collateral[self.collateral_index]
            cov = [[10, 0], [0, 10]]
            x, y = np.random.multivariate_normal(mean, cov, self.n_exemplars).T
            continuer.append(list(map(lambda x, y: [x, y], x, y)))

            # Initialise all c_words as continuer words ('C')
            lexicon.append([continuer[0], "C"])
            indices_continuer = lexicon.index([continuer[0], "C"])


            # Create a separate lexicon with the continuer words
            continuer_words.append([continuer[0], "C"])

            # The words that are not continuers are regular vocabulary words
            v_words = [word for word in lexicon if word not in continuer_words]

            # print("Lexicon:", lexicon)

            # print("Meta lexicon:", continuer_words)
            # print("Com lexicon:", v_words)

        # If there are no continuers, the continuers list is empty and all the words in the lexicon are
        # regular vocabulary words
        else:
            v_words = lexicon
            continuer_words = []

        return lexicon, v_words, continuer_words, indices_continuer
