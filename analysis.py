import matplotlib.pyplot as plt
import pandas as pd
from itertools import chain
from math import hypot
from itertools import combinations
import seaborn as sns
import matplotlib
import numpy as np


# ======================================================================================================================

# Define the Euclidean distance measure between two points in a 2D space
def distance(p1, p2):
    """
    Calculate the Euclidean distance between two points.
    :param p1: list; the first point in the 2D space
    :param p2: list; the second point in the 2D space
    :return: float; the Euclidean distance
    """

    # Get the coordinates for both points
    x1, y1 = p1
    x2, y2 = p2

    # Return the Euclidean distance between the 2D points
    return hypot(x2 - x1, y2 - y1)


# ======================================================================================================================

# Functions for squareness measure

def pairwise_distances(centroids, all_possible_pairings, n_dimensions):
    distances_per_dimension = np.zeros((len(all_possible_pairings), n_dimensions))
    distances_pairings = np.zeros(len(all_possible_pairings))
    for p in range(len(all_possible_pairings)):
        pairing = all_possible_pairings[p]
        # print('')
        # print('')
        # print("pairing is:")
        # print(pairing)
        distance_per_dimension = np.zeros(n_dimensions)
        for d in range(n_dimensions):
            total_distance = 0.
            for pair in pairing:
                # print('')
                # print("pair is:")
                # print(pair)
                index_i = pair[d][0]
                index_j = pair[d][1]
                segment_value_i = centroids[index_i][d]
                segment_value_j = centroids[index_j][d]
                # print("segment_value_i is:")
                # print(segment_value_i)
                # print("segment_value_j is:")
                # print(segment_value_j)
                total_distance += abs(segment_value_i - segment_value_j)
                # print("distance is:")
                # print(abs(segment_value_i - segment_value_j))
            distance_per_dimension[d] = total_distance
        # print("total_distance is:")
        # print(total_distance)
        distances_per_dimension[p] = distance_per_dimension
        distances_pairings[p] = np.sum(distances_per_dimension[p])
    return distances_per_dimension, distances_pairings


def choose_fitting_pairing(distances_pairings):
    smallest_distance = np.amin(distances_pairings)
    smallest_index = np.argmin(distances_pairings)

    return smallest_distance, smallest_index


# ======================================================================================================================

# Start the analysis of the results data selected

def analysis(folder, results_file, intermediate=None, wedel_start=True):
    # Read in the data
    results = pd.read_pickle(folder + results_file)

    # A list collecting all the probabilities of signals being stored in the rounds of the simulation runs
    probability_storages = []

    # A list collecting the error rate/Exclusion rates
    excluded_signals_runs = []

    # Initialise some empty lists to put in the average distances between the centroids and the two dimensional SD of
    # the word categories
    average_centroid_distances = []
    average_sd = []

    # Initialise empty lists for the average distance of the v_words and continuer v_words to the middle of the
    # 2D space
    averages_word_runs = []
    averages_continuer_runs = []

    # Initialise empty lists for the average distance of the v_words and continuer v_words to their
    # initialisation state
    v_word_distance_run1_average = []
    continuer_distance_run1_average = []

    # Initialise empty lists for the v_words and continuer v_words
    v_words = []
    continuer_words = []

    exemplar_list = []

    # Iterate over the total number of runs to access every independent simulation run
    for run in range(results.iloc[-1]["Simulation_run"] + 1):

        # Define the number of rounds used in the simulations
        if intermediate is None:
            n_rounds = results.iloc[0]["N_rounds"]
        else:
            n_rounds = intermediate

        # Calculate the number of states used in the simulation (start, middle (multiple middle states are possible),
        # end) based on the number of rounds
        n_states = (n_rounds / 500) + 1

        # Define the number of v_words used in the simulations
        n_words = results["N_words"].iloc[0]

        # Calculate the start and end position in the results dataframe for every simulation
        end = int(2 * n_words * n_states)
        start_position = run * end

        if intermediate is None:
            end_position = ((run + 1) * end) - 2

        # Define the end position if you want an intermediate result
        else:
            end_position = start_position + ((intermediate // 500) * 8) + 3

        # print(results.iloc[end_position])

        # Define the start and end lexicons
        lexicon_start = results["Lexicon"].iloc[start_position]
        lexicon_end = results["Lexicon"].iloc[end_position]

        # Plot the beginning first
        # for word_index in range(n_words):
        #     exemplars = lexicon_start[word_index][0]
        #     plt.scatter(*zip(*exemplars))
        #
        # plt.xlim(0, 100)
        # plt.ylim(0, 100)
        # plt.show()

        # ===============================================================================================================

        # Initialise empty lists to store the centroids and 2D SDs
        centroid_list = []
        average_distance_list = []

        for word_index in range(n_words):
            # Define the exemplars of the word
            exemplars = lexicon_end[word_index][0]
            exemplar_list.append(exemplars)

            # Gather the centroids for the first agent only, for the current word, for the end position of the
            # simulation and for the current simulation run
            if intermediate is None:
                centroid = results.loc[(results["Word"] == word_index) & (results["Agent"] == 1) &
                                       (results["State"] == "End") & (results["Simulation_run"] == run), "Centroid"]
                centroid_list.append(centroid.tolist())

                # Do the same for the 2D SDs
                average_distance = results.loc[(results["Word"] == word_index) & (results["Agent"] == 1) &
                                               (results["State"] == "End") & (results["Simulation_run"] == run),
                                               "Average_distance"]

            # The centroids and average distance measures for intermediate rounds
            else:
                centroid_list.append(centroid.tolist())
                average_distance = results.loc[(results["Word"] == word_index) & (results["Agent"] == 1) &
                                               (results["N_rounds"] == n_rounds) & (results["Simulation_run"] == run),
                                               "Average_distance"]

            average_distance_list.append(average_distance.tolist())
        # print("List of centroids: ", centroid_list)

        average_distance_list = list(chain.from_iterable(average_distance_list))
        # print("Average SD: ", sum(average_distance_list)/len(average_distance_list))

        # Calculate the distances between the word centroids
        centroid_list = list(chain(*centroid_list))
        centroid_distances = [distance(*combo) for combo in combinations(centroid_list, 2)]

        # Calculate the average centroids distance and 2D SD per simulation run
        average_centroid_distances.append(sum(centroid_distances) / len(centroid_distances))
        average_sd.append(sum(average_distance_list) / len(average_distance_list))

        # ==================================================================================================================

        # Calculate the error: exclusion rates (how often the signal is not stored)

        # Get the value from the column "Store" and divide that by the number of words * number of simulation runs
        if intermediate is None:
            stored_signals = results.loc[(results["Word"] == n_words - 1) & (results["Agent"] == 1) &
                                         (results["State"] == "End") & (
                                                 results["Simulation_run"] == run), "Store"].values
            relative_stored = stored_signals / (n_words * (n_rounds / 2))

        # For intermediate results
        else:
            stored_signals = results.loc[(results["Word"] == n_words - 1) & (results["Agent"] == 1) &
                                         (results["N_rounds"] == n_rounds) & (results["Simulation_run"] == run),
                                         "Store"].values
            relative_stored = stored_signals / (n_words * (n_rounds / 2))

        # Calculate how often the signal gets excluded
        excluded_signals = 1 - relative_stored
        excluded_signals_runs.append(excluded_signals)

        # ==============================================================================================================

        # Calculate the average probability storage of all signals in all the simulation runs

        # Only applied when there is an anti-ambiguity bias
        if results["Anti_ambiguity_bias"].iloc[0]:
            if intermediate is None:
                probability_storage = results.loc[(results["Word"] == n_words - 1) & (results["Agent"] == 1) &
                                                  (results["State"] == "End") & (results["Simulation_run"] == run),
                                                  "Probability_storages"].values

            # For intermediate results
            else:
                probability_storage = results.loc[(results["Word"] == n_words - 1) & (results["Agent"] == 1) &
                                                  (results["N_rounds"] == n_rounds) & (
                                                          results["Simulation_run"] == run),
                                                  "Probability_storages"].values

            probability_storages.append(probability_storage)

        # ==============================================================================================================

        # Calculate the squareness of all the saved rounds (per 500 rounds)

        # First create a list of the centroids of all words
        for n_round in range(0, n_rounds, 500):
            centroid_list = []
            for word_index in range(n_words):
                centroid = results.loc[(results["Word"] == word_index) & (results["Agent"] == 1) &
                                       (results["N_rounds"] == n_round) & (results["Simulation_run"] == run), "Centroid"]
                centroid_list.append(centroid.tolist())
            print(centroid_list)

        # for round in n_rounds:
        #     squareness_distance = results.loc[(results["Word"] == n_words - 1) & (results["Agent"] == 1) &
        #                                       (results["N_rounds"] == round) & (results["Simulation_run"] ==
        #                                                                         run), "Centroid"].values
        #     distances_per_dimension, distances_pairings = pairwise_distances(centroids_square, all_possible_pairings,
        #                                                                      n_dimensions)
        # print("distances_per_dimension are:")
        # print(distances_per_dimension)
        # print("distances_possibilities are:")
        # print(distances_pairings)
        #
        # smallest_distance, smallest_index = choose_fitting_pairing(distances_pairings)
        # print("Smallest distance: ", smallest_distance)
        # print("Index smallest distance: ", smallest_index)

        # ==============================================================================================================

        # Calculate the distance to the middle of the space for the different types of v_words: v_words vs continuers

    #     distances_word = []
    #     distances_continuer = []
    #     for word_index in range(n_words):
    #         # Calculate the exemplar distances to the middle for the v_words
    #         if lexicon_end[word_index][1] == "V":
    #             exemplars = lexicon_end[word_index][0]
    #             v_words.append(exemplars)
    #             for exemplar in exemplars:
    #                 distance_exemplar = distance(exemplar, [50, 50])
    #                 distances_word.append(distance_exemplar)
    #         else:
    #             # Calculate the exemplar distances to the middle for the continuer v_words
    #             exemplars = lexicon_end[word_index][0]
    #             continuer_words.append(exemplars)
    #             for exemplar in exemplars:
    #                 distance_exemplar = distance(exemplar, [50, 50])
    #                 distances_continuer.append(distance_exemplar)
    #
    #     # Calculate the average distance to the middle of the space for the v_words and continuer v_words
    #     average_distance_words = sum(distances_word) / len(distances_word)
    #     average_distance_continuer = sum(distances_continuer) / len(distances_continuer)
    #
    #     print("Regular vocabulary v_words average distance to middle: ", average_distance_words)
    #     print("Continuer average distance to middle: ", average_distance_continuer)
    #
    #     # Calculate the average distance to the middle of the space over all runs for the v_words and continuer
    #     # v_words
    #     averages_word_runs.append(average_distance_words)
    #     averages_continuer_runs.append(average_distance_continuer)
    #
    #     # ============================================================================================================
    #
    #     # 2D SD measure across all simulations: SD of first run to every other run compared for the v_words and
    #     # continuer v_words
    #
    #     v_word_distance_run1 = []
    #     continuer_distance_run1 = []
    #
    #     for word_index in range(n_words):
    #         # Calculate the distance between the start and end state of the centroid of the selected word
    #         if lexicon_end[word_index][1] == "V":
    #             centroid_first = results.loc[(results["Word"] == word_index) & (results["Agent"] == 1) &
    #                                          (results["State"] == "End") & (results["Simulation_run"] == 0),
    #                                          "Centroid"]
    #             centroid_end = results.loc[(results["Word"] == word_index) & (results["Agent"] == 1) &
    #                                        (results["State"] == "End") & (results["Simulation_run"] == run),
    #                                        "Centroid"]
    #             distance_centroid = distance(list(chain(*centroid_first)), list(chain(*centroid_end)))
    #             v_word_distance_run1.append(distance_centroid)
    #         # Calculate the distance between the start and end state of the centroid of the selected continuer word
    #         else:
    #             centroid_first = results.loc[(results["Word"] == word_index) & (results["Agent"] == 1) &
    #                                          (results["State"] == "End") & (results["Simulation_run"] == 0),
    #                                          "Centroid"]
    #             centroid_end = results.loc[(results["Word"] == word_index) & (results["Agent"] == 1) &
    #                                        (results["State"] == "End") & (results["Simulation_run"] == run),
    #                                        "Centroid"]
    #             distance_centroid = distance(list(chain(*centroid_first)), list(chain(*centroid_end)))
    #             continuer_distance_run1.append(distance_centroid)
    #
    #     # Calculate the average distance of the start and end states of the centroids over all v_words
    #     v_word_distance_run1_average.append(sum(v_word_distance_run1) / len(v_word_distance_run1))
    #     continuer_distance_run1_average.append(sum(continuer_distance_run1) / len(continuer_distance_run1))
    #
    # # Calculate the average distance of the start and end states of the centroids for the v_words and continuer
    # v_words over all
    # # runs
    # average_word_runs = sum(averages_word_runs) / len(averages_word_runs)
    # average_continuer_runs = sum(averages_continuer_runs) / len(averages_continuer_runs)
    # print("Regular vocabulary word average distance over all runs: ", average_word_runs)
    # print("Continuer average distance over all runs: ", average_continuer_runs)
    #
    # # Print the average distance (averaged over v_words) between centroids of the initialisation versus the end for
    # every word
    # print("Regular vocabulary word average distance per run: ", v_word_distance_run1_average)
    # print("Continuer average distance per run: ", continuer_distance_run1_average)

    # ======================================================================================================================

    # Save the plot of the end state of the simulation runs of the first agent
    matplotlib.rc('xtick', labelsize=12)
    matplotlib.rc('ytick', labelsize=12)

    with sns.axes_style("whitegrid"):
        sns.set_palette("colorblind")
        fig, axs = plt.subplots(5, 4, figsize=(8, 8))
        axs = axs.ravel()
    for run in range(results.iloc[-1]["Simulation_run"] + 1):
        for word_index in range(n_words):
            exemplars = exemplar_list[(run * n_words) + word_index]
            axs[run].scatter(*zip(*exemplars), edgecolors="white", linewidths=0.5)
        sns.set_style("whitegrid")
        sns.set_palette("colorblind")
        axs[run].set_xlim([0, 100])
        axs[run].set_ylim([0, 100])

    for ax in axs.flat:
        ax.label_outer()

    if results["Anti_ambiguity_bias"].iloc[0]:
        if wedel_start:
            fig.suptitle("With anti-ambiguity bias and with Wedel initialisation of \n" + str(n_words) + " words: " +
                         str(n_rounds) + " rounds",
                         size=20)
        else:
            fig.suptitle("With anti-ambiguity bias and with random initialisation of \n" + str(n_words) + " words: " +
                         str(n_rounds) + " rounds",
                         size=20)
    else:
        if wedel_start:
            fig.suptitle("Without anti-ambiguity bias and with Wedel initialisation of \n" + str(n_words) + " words: " +
                         str(n_rounds) + " rounds",
                         size=20)
        else:
            fig.suptitle("Without anti-ambiguity bias and with random initialisation of \n" + str(n_words) + " words: "
                         + str(n_rounds) + " rounds",
                         size=20)

    fig.text(0.5, 0.04, 'Dimension 1', ha='center', size=18)
    fig.text(0.04, 0.5, 'Dimension 2', va='center', rotation='vertical', size=18)
    plt.setp(axs, xticks=np.arange(0, 101, 25), yticks=np.arange(0, 101, 25))
    # plt.show()
    if results["Anti_ambiguity_bias"].iloc[0]:
        plt.savefig(folder + "exemplars_amb_" + str(n_rounds) + "_" + str(n_words) + ".pdf")
    else:
        plt.savefig(folder + "exemplars_no_amb_" + str(n_rounds) + "_" + str(n_words) + ".pdf")
    plt.clf()

    # Save the plot of the average centroids distance
    r = list(range(1, results.iloc[-1]["Simulation_run"] + 2))
    sns.set_style("whitegrid")
    sns.color_palette("colorblind")
    plt.bar(x=r, height=average_centroid_distances)
    plt.ylim(0, 50)
    plt.xticks(r)
    plt.xlabel("Simulation run", size=18)
    plt.ylabel("Average centroids distance", size=18)

    if results["Anti_ambiguity_bias"].iloc[0]:
        if wedel_start:
            fig.suptitle("With anti-ambiguity bias and with Wedel initialisation of \n" + str(n_words) + " words: " +
                         str(n_rounds) + " rounds",
                         size=20)
        else:
            fig.suptitle("With anti-ambiguity bias and with random initialisation of \n" + str(n_words) + " words: " +
                         str(n_rounds) + " rounds",
                         size=20)
    else:
        if wedel_start:
            fig.suptitle("Without anti-ambiguity bias and with Wedel initialisation of \n" + str(n_words) + " words: "
                         + str(n_rounds) + " rounds",
                         size=20)
        else:
            fig.suptitle("Without anti-ambiguity bias and with random initialisation of \n" + str(n_words) + " words: "
                         + str(n_rounds) + " rounds",
                         size=20)

    # plt.show()
    if results["Anti_ambiguity_bias"].iloc[0]:
        plt.savefig(folder + "centroid_amb_" + str(n_rounds) + "_" + str(n_words) + ".pdf")
    else:
        plt.savefig(folder + "centroid_no_amb_" + str(n_rounds) + "_" + str(n_words) + ".pdf")
    plt.clf()

    # Save the plot of the average SD for a two dimensional space
    r = list(range(1, results.iloc[-1]["Simulation_run"] + 2))
    sns.set_style("whitegrid")
    sns.color_palette("colorblind")
    plt.bar(x=r, height=average_sd)
    plt.ylim(0, 5)
    plt.xticks(r)
    plt.xlabel("Simulation run", size=18)
    plt.ylabel("Average distance of exemplars to centroids", size=18)

    if results["Anti_ambiguity_bias"].iloc[0]:
        if wedel_start:
            fig.suptitle("With anti-ambiguity bias and with Wedel initialisation of \n" + str(n_words) + " words: " +
                         str(n_rounds) + " rounds",
                         size=20)
        else:
            fig.suptitle("With anti-ambiguity bias and with random initialisation of \n" + str(n_words) + " words: " +
                         str(n_rounds) + " rounds",
                         size=20)
    else:
        if wedel_start:
            fig.suptitle("Without anti-ambiguity bias and with Wedel initialisation of \n" + str(n_words) + " words: " +
                         str(n_rounds) + " rounds",
                         size=20)
        else:
            fig.suptitle("Without anti-ambiguity bias and with random initialisation of \n" + str(n_words) + " words: "
                         + str(n_rounds) + " rounds",
                         size=20)

    # plt.show()
    if results["Anti_ambiguity_bias"].iloc[0]:
        plt.savefig(folder + "sd_amb_" + str(n_rounds) + "_" + str(n_words) + ".pdf")
    else:
        plt.savefig(folder + "sd_no_amb_" + str(n_rounds) + "_" + str(n_words) + ".pdf")
    plt.clf()

    # ==================================================================================================================
    if results["Anti_ambiguity_bias"].iloc[0]:
        # Calculate the average exclusion rate for the independent simulation runs
        average_exclusion_rate = sum(excluded_signals_runs) / len(excluded_signals_runs)
        print("Average exclusion rate: ", average_exclusion_rate)

        # ==============================================================================================================

        # Calculate the average probability storage over all rounds and simulation runs
        probability_storages = list(chain.from_iterable(probability_storages))[0]
        average_probability_storage = sum(probability_storages) / len(probability_storages)
        print("Average probability storage: ", average_probability_storage)

    # ======================================================================================================================
    # Plot the distinct v_words over all the simulation runs per word (one plot per word to see how they move in the
    # space)

    # # Create subplots for the different words (5 words: 4 V 1 C)
    # ax1 = plt.subplot(231)
    # ax2 = plt.subplot(232)
    # ax3 = plt.subplot(233)
    # ax4 = plt.subplot(234)
    # ax5 = plt.subplot(236)
    #
    # # # Plot every run on the same subplot
    # # for run in range(results.iloc[-1]["Simulation_run"] + 1):
    # #     ax1.scatter(*zip(*v_words[0+(run*4)]), c="tab:blue")
    # #     ax2.scatter(*zip(*v_words[1+(run*4)]), c="tab:orange")
    # #     ax3.scatter(*zip(*v_words[2+(run*4)]), c="tab:green")
    # #     ax4.scatter(*zip(*v_words[3+(run*4)]), c="tab:red")
    # #     ax5.scatter(*zip(*continuer_words[0+run]), c="tab:purple")
    #
    # # print(v_words[0])
    # # print(np.array(v_words)[0].T)
    #
    # # for run in range(results.iloc[-1]["Simulation_run"] + 1):
    # #     sns.scatterplot(np.array(v_words)[0+(run*4)].T, c="tab:blue")
    # #     # ax2.sns.scatterplot(*zip(*v_words[1+(run*4)]), c="tab:orange")
    # #     # ax3.sns.scatterplot(*zip(*v_words[2+(run*4)]), c="tab:green")
    # #     # ax4.sns.scatterplot(*zip(*v_words[3+(run*4)]), c="tab:red")
    # #     # ax5.sns.scatterplot(*zip(*continuer_words[0+run]), c="tab:purple")
    #
    #
    # # for word in v_words:
    # #     ax1.scatter(*zip(*word))
    # #
    # # for word in continuer_words:
    # #     ax2.scatter(*zip(*word))
    #
    # # # Plot the in between states as well
    # # sliced_results = results[results["Agent"] == 1]
    # #
    # # for index, row in sliced_results.iterrows():
    # #     if row["Lexicon"][1] == "W":
    # #         exemplars = row["Exemplars"]
    # #         plt.scatter(*zip(*exemplars))
    # #     else:
    # #         exemplars = row["Exemplars"]
    # #         plt.scatter(*zip(*exemplars))
    # # plt.show()
    #
    # # Plot all the v_words for all runs
    # ax1.set_xlim([0, 100])
    # ax1.set_ylim([0, 100])
    #
    # ax2.set_xlim([0, 100])
    # ax2.set_ylim([0, 100])
    #
    # ax3.set_xlim([0, 100])
    # ax3.set_ylim([0, 100])
    #
    # ax4.set_xlim([0, 100])
    # ax4.set_ylim([0, 100])
    #
    # ax5.set_xlim([0, 100])
    # ax5.set_ylim([0, 100])
    #
    # plt.show()
