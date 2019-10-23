import numpy as np
import hmm

states = ('Intruder', 'Non-Intruder')

observations = ('Below Threshold', 'Above Threshold')

start_probability = {'Intruder': 0.2, 'Non-Intruder': 0.8}

transition_probability = {
    'Intruder': {'Intruder': 0.5, 'Non-Intruder': 0.5},
    'Non-Intruder': {'Intruder': 0.3, 'Non-Intruder': 0.7},
}

emission_probability = {
    'Intruder': {'Below Threshold': 0.2, 'Above Threshold': 0.8},
    'Non-Intruder': {'Below Threshold': 0.7, 'Above Threshold': 0.3},
}


def generate_index_map(lables):
    index_label = {}
    label_index = {}
    i = 0
    for l in lables:
        index_label[i] = l
        label_index[l] = i
        i += 1
    return label_index, index_label


states_label_index, states_index_label = generate_index_map(states)
observations_label_index, observations_index_label = generate_index_map(observations)
print(observations_index_label, observations_label_index)

def convert_observations_to_index(observations, label_index):
    list = []
    for o in observations:
        list.append(label_index[o])
    return list


def convert_map_to_vector(map, label_index):
    v = np.empty(len(map), dtype=float)
    for e in map:
        v[label_index[e]] = map[e]
    return v


def convert_map_to_matrix(map, label_index1, label_index2):
    m = np.empty((len(label_index1), len(label_index2)), dtype=float)
    for line in map:
        for col in map[line]:
            m[label_index1[line]][label_index2[col]] = map[line][col]
    return m


A = convert_map_to_matrix(transition_probability, states_label_index, states_label_index)
# print A
B = convert_map_to_matrix(emission_probability, states_label_index, observations_label_index)
# print B
observations_index = convert_observations_to_index(observations, observations_label_index)
pi = convert_map_to_vector(start_probability, states_label_index)
# print pi

h = hmm.HMM(A, B, pi)
V, p = h.viterbi(observations_index)
print " " * 7, " ".join(("%10s" % observations_index_label[i]) for i in observations_index)
for s in range(0, 2):
    print "%7s: " % states_index_label[s] + " ".join("%10s" % ("%f" % v) for v in V[s])
# print '\nThe most possible states and probability are:'
p, ss = h.state_path(observations_index)
# for s in ss:
#     print states_index_label[s],

print '\nThe probability of Intruder is : ' + str(p) + '\n'
if p < 0.5:
    print 'You have successfully cleared the Intrusion Detection :)'
else:
    print 'Invalid User : Caught in Intrusion Detection!!!'

# run a baum_welch_train
observations_data, states_data = h.simulate(100)
# print observations_data
# print states_data
guess = hmm.HMM(np.array([[0.5, 0.5],
                          [0.5, 0.5]]),
                np.array([[0.3, 0.3, 0.3],
                          [0.3, 0.3, 0.3]]),
                np.array([0.5, 0.5])
                )
guess.baum_welch_train(observations_data)
states_out = guess.state_path(observations_data)[1]
p = 0.0
for s in states_data:
    if next(states_out) == s: p += 1

# print p / len(states_data)



