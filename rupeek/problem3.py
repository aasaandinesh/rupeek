num_of_testcases = int(input())
index = 0
numbers = []


def is_valid_second(first, second):
    string_second = str(second)
    string_first = str(first)
    return len(string_first) - len(string_second) == 1



def is_valid_third(first, second):
    return True


def is_valid_fourth(first, second):
    string_second = str(second)
    string_first = str(first)
    index = 0
    while index < len(string_first):
        if string_first[:index] + string_first[index+1:] == string_second:
            return True
        index +=1
    return False


def is_valid(first, second):
    s_cond = is_valid_second(first, second)
    t_cond = is_valid_third(first, second)
    f_cond = is_valid_fourth(first, second)

    if (first == 10 or first == '10') and (second == 1 or second == '1') :
        print("Condition first is {0}, second is {1} and third is {2}".format(s_cond, t_cond, f_cond))
    return s_cond and t_cond and f_cond


def get_second_numbers(first, second):
    s = str(second)
    second_numbers = []
    while len(s) < 6:
        second_numbers.append(s)
        s = '0' + s
    return second_numbers


def get_results(num):
    first = 10

    pairs = []
    while first < num:
        second = num - first
        # Attempting to add zero to second
        all_second_numbers = get_second_numbers(first, second)

        for s in all_second_numbers:

            if is_valid(first, s):
                #print("Condition is True")
                pairs.append({"first": first, "second": s})

        first += 1

    print("{0} pairs found:".format(len(pairs)))
    for p in pairs:
        print("{0} + {1} = {2}".format(p['first'], p['second'], num))


while index < num_of_testcases:
    num = int(input())
    numbers.append(num)
    index += 1

for n in numbers:
    get_results(n)
