import random
import heapq
import matplotlib.pyplot as plt

# Feel free to mass with argument below
queen_count = 8 # Board size and Queen amount
try_times = 1000000 # Maximum generation of child
child_amount = 4 # Only work with even number
initial_population = 12 # Starting population size
mutate_times = 1 # How many times to mutate
static_analysis = True # Static Analysis will cause slow performance


# Randomly generate a population size of {count}
# with each sequence size of {len}
def initial(len, count):
    seq = []
    for seq_step in range(count):
        num = []
        for num_step in range(len):
            num.append(random.randint(0, len-1))
        seq.append(num)

    return seq


# Give a sequence and return with a fitness score (higher mean better)
def fitness(seq):
    nonattack_pair = 0

    def check_hit(pos1, pos2):
        if(pos1[0] == pos2[0] or pos1[1] == pos2[1]):
            return True
        elif(abs(pos2[0]-pos1[0]) == abs(pos2[1]-pos1[1])):
            return True
        else:
            return False

    for i in range(len(seq)):
        for other in range(len(seq)):
            if(not check_hit((i, seq[i]), (other, seq[other]))):
                nonattack_pair = nonattack_pair + 1

    return (nonattack_pair / 2)


# Select {count} number of sequence with probability base on their score
def selection(seq_scores, count):
    score_accumulate = []
    sum = 0
    for seq_score in seq_scores:
        sum = sum + seq_score[0]
        score_accumulate.append(sum)

    result = []
    for iter in range(count):
        draw = random.randint(0, score_accumulate[-1])

        for pos in range(len(score_accumulate)):
            if(draw <= score_accumulate[pos]):
                result.append(seq_scores[pos][1])
                break

    return result


# Give a list of sequences, slice and combine them randomly
def crossover(seqs):
    childs = []

    for cur_seq, next_seq in zip(seqs[::2], seqs[1::2]):
        slice_pos = random.randint(0, len(cur_seq))
        childs.append(cur_seq[:slice_pos] + next_seq[slice_pos:])
        childs.append(next_seq[:slice_pos] + next_seq[slice_pos:])

    return childs


# Give a list of sequences and randomly change number
# More {times} mean mutate more
def mutation(seqs, times):
    for seq in seqs:
        for step in range(times):
            pos = random.randint(0, len(seq)-1)
            seq[pos] = random.randint(0, len(seq)-1)

    return seqs


# Initial with {population} amount of number
# and choose the top {top_count} individuals in population
def initial_best(top_count, population):
    seq_list = initial(queen_count, population)
    result = []
    for seq in seq_list:
        score = fitness(seq)
        result.append((score, seq))

    result_heap = list(result)
    heapq._heapify_max(result_heap)

    result.clear()
    for _ in range(top_count):
        result.append(heapq._heappop_max(result_heap))

    return result



# Start from here
if(__name__ == "__main__"):
    # Calculate the terminate condition (fitness score)
    ans_score = (queen_count * (queen_count - 1)) / 2
    # Show information to user
    if(static_analysis):
        plt.title(str(queen_count) + "-Queens Genetic Alogorithm\n"
                    + "Answer score = " + str(ans_score))
        plt.ylabel("Fitness score")
        plt.xlabel("Iter")
    else:
        print(str(queen_count) + "-Queens Genetic Algorithm")
        print("Answer score = " + str(ans_score))
        print('-'*10 + '\n')

    # Initial a population and choose best individual in it
    top_individuals = initial_best(child_amount, initial_population)
    # Starting individuals average score
    score_avg = sum([individual[0] for individual in top_individuals]) / child_amount
    if(static_analysis):
        plt.scatter(0, score_avg)
        plt.pause(1)

    # Genetic Algorithm with maximum {try_times} of try
    for step in range(1, try_times):
        selected_parent = selection(top_individuals, child_amount)
        children = crossover(selected_parent)
        result_children = mutation(children, mutate_times)

        # Replace {top_individuals} with {result_children}
        top_individuals.clear()
        score_avg = 0
        for child in result_children:
            score = fitness(child)
            # Calculate this generation's average score
            score_avg = score_avg + score/len(result_children)
            # Terminate condition
            if(score == ans_score):
                print("\nAfter", step, "of Generations,")
                print("The algorithm found one of the solution!")
                print("Sequence:", child)
                if(static_analysis):
                    plt.scatter(step, score)
                    plt.show()
                exit()
            # Replace {top_individuals} with {result_children}
            top_individuals.append((score, child))
        if(static_analysis):
            plt.scatter(step, score_avg)
            plt.pause(0.01)
        elif((step % 1000) == 0):
            print("Iter times:", step)
    print("Failed to find solution with", try_times, "times of try QQ")