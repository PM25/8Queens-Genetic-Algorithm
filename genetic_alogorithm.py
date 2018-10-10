import random
import heapq

queen_count = 8


def initial(len, count):
    seq = []
    for seq_step in range(count):
        num = []
        for num_step in range(len):
            num.append(random.randint(0, len-1))
        seq.append(num)

    return seq


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


def crossover(seqs):
    childs = []

    for cur_seq, next_seq in zip(seqs[::2], seqs[1::2]):
        slice_pos = random.randint(0, len(cur_seq))
        childs.append(cur_seq[:slice_pos] + next_seq[slice_pos:])
        childs.append(next_seq[:slice_pos] + next_seq[slice_pos:])

    return childs


def mutation(seqs, times):
    for seq in seqs:
        for step in range(times):
            pos = random.randint(0, len(seq)-1)
            seq[pos] = random.randint(0, len(seq)-1)

    return seqs


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



if(__name__ == "__main__"):
    top_individuals = initial_best(4, 12)

    while(True):
        selected_parent = selection(top_individuals, 4)
        children = crossover(selected_parent)
        result_children = mutation(children, 1)

        top_individuals.clear()
        for child in result_children:
            score = fitness(child)
            print(score)
            if(score == 28):
                print(child)
                exit()

            top_individuals.append((score, child))