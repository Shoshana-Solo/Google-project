from dataclasses import dataclass


@dataclass
class AutoCompleteData:
    completed_sentence: str
    source_text: str
    offset: int
    score: int
    file_id: int


def get_score(len_str, pos, flag, flag2):
    '''

    :param len_str: len of user str
    :param pos:index changed -1 if not
    :param flag: 1 if switch, 2 if add or delete
    :param 0 if add , 1 if delete or switch
    :return:
    '''
    if pos == -1:
        return 2 * len_str

    pos = 4 if pos > 5 else pos
    return (len_str - flag2) * 2 - (5 * flag - pos * flag)


def get_change_of_delete(json_data, json_lines, user_input, i):
    if json_data.get(user_input[:i] + user_input[i + 1:], 0):
        return [AutoCompleteData(user_input[:i] + user_input[i + 1:],
                                 json_lines[f'{result[0]}']["path"], result[1],
                                 get_score(len(user_input), i, 2, 1), result[0]) for result in
                json_data[user_input[:i] + user_input[i + 1:]]]
    return []


def get_change_of_add(json_data, json_lines, user_input, i, j):
    if json_data.get(user_input[:i] + j + user_input[i:], 0):
        return [AutoCompleteData(user_input[:i] + j + user_input[i:],
                                 json_lines[f'{result[0]}']["path"], result[1],
                                 get_score(len(user_input), i, 2, 0), result[0]) for result in
                json_data[user_input[:i] + j + user_input[i:]]]

    return []


def get_change_of_switch(json_data, json_lines, user_input, i, j):
    if j != user_input[i]:
        if json_data.get(user_input[:i] + j + user_input[i + 1:], 0):
            return [AutoCompleteData(user_input[:i] + j + user_input[i + 1:],
                                     json_lines[f'{result[0]}']["path"], result[1],
                                     get_score(len(user_input), i, 1, 1), result[0]) for result in
                    json_data[user_input[:i] + j + user_input[i + 1:]]]

    return []


def allow_changes(json_data, json_lines, user_input, i, j, num_to_add):
    res = []
    res += get_change_of_switch(json_data, json_lines, user_input, i, j)

    if len(res) < num_to_add:
        res += get_change_of_add(json_data, json_lines, user_input, i, j)

    return res


def get_best_k_completions(json_data, json_lines, user_input):
    chars = ' qwertyuiopasdfghjklzxcvbnm1234567890'
    res = []
    if json_data.get(user_input, 0):
        res += [AutoCompleteData(user_input, json_lines[f'{i[0]}']["path"], i[1], get_score(len(user_input), -1, 0, 0),
                                 i[0]) for i in
                json_data[user_input]]
    if len(res) < 5:
        for i in range(len(user_input) - 1, 0, -1):
            for j in chars:
                res += allow_changes(json_data, json_lines, user_input, i, j, 5 - len(res))
                if len(res) >= 5:
                    return res
            res += get_change_of_delete(json_data, json_lines, user_input, i)
    return res
