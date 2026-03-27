import math


def get_domain(function, draw_domain: range, holes: list[int]):
    i = 0
    while i < len(draw_domain):
        try:
            function(draw_domain[i])
        except ValueError:
            i += 1
        except ZeroDivisionError:
            i += 1
        else:
            break
    if i == len(draw_domain):
        return range(0, 0)
    x_min = draw_domain[i]

    while i < len(draw_domain):
        if draw_domain[i] not in holes:
            try:
                function(draw_domain[i])
            except ValueError:
                break
            except ZeroDivisionError:
                break
        i += 1
    if i == len(draw_domain):
        x_max = draw_domain[i - 1] + draw_domain.step
    else:
        x_max = draw_domain[i]

    return range(x_min, x_max)


def get_range(function, draw_domain: range, holes: list[int]):
    function_domain = get_domain(function, draw_domain, holes)
    if function_domain == range(0, 0):
        return range(0, 0)
    y_min = y_max = int(function(function_domain[0]))
    for x in function_domain:
        if x not in holes:
            y = int(function(x))
            if y_min > y:
                y_min = y
            elif y_max < y:
                y_max = y
    if y_max - y_min < 5:
        if y_max != y_min:
            print('Hmm... That\'s a little bit small. Maybe use larger scale?')
        if y_max > 0:
            y_max *= 2
        else:
            y_max //= 2
        if y_min > 0:
            y_min //= 2
        else:
            y_min *= 2
    return range(y_min - 1, y_max + 2)


def get_holes(function, draw_domain: range):
    i = 1
    holes = []
    while i < len(draw_domain) - 1:
        try:
            function(draw_domain[i-1])
            function(draw_domain[i+1])
        except ValueError:
            pass
        except ZeroDivisionError:
            pass
        else:
            try:
                function(draw_domain[i])
            except ValueError:
                holes.append(draw_domain[i])
            except ZeroDivisionError:
                holes.append(draw_domain[i])
        finally:
            i += 1
    return holes


def draw(function, draw_domain: range):
    holes = get_holes(function, draw_domain)
    function_domain = get_domain(function, draw_domain, holes)
    function_range = get_range(function, draw_domain, holes)
    print('Domain: [' + str(function_domain.start) + ', ' + str(function_domain.stop - 1) + ']')
    print('Range: [' + str(-function_range.stop + 2) + ', ' + str(-function_range.start - 1) + ']')
    print()

    for y in function_range:
        for x in draw_domain:
            if x == y == 0:
                point = '0'
            elif x == 0:
                point = '|'
            elif y == 0:
                point = '-'
            else:
                point = ' '
            if x in function_domain and x not in holes:
                if y == function(x):
                    point = '*'
                elif (x - 1 in function_domain and x - 1 not in holes
                      and function(x) < y < function(x - 1)
                      or x + 1 in function_domain and x + 1 not in holes
                      and function(x) < y < function(x + 1)):
                    point = '*'
                elif y == int(function(x)) and y < 0:
                    point = '*'
                elif y - 1 == int(function(x)) and y > 1 and not function(x).is_integer():
                    point = '*'
            print(point, end=' ')
        print()


def get_1st_parenthesis(function: str, open_symbol: str, close_symbol: str):
    if open_symbol == close_symbol:
        open_index = function.find(open_symbol)
        close_index = function.rfind(close_symbol)
    else:
        open_index = function.find(open_symbol)
        open_count = 0
        i = open_index + 1
        while not (function[i] == close_symbol and open_count == 0):
            if function[i] == open_symbol:
                open_count += 1
            elif function[i] == close_symbol:
                open_count -= 1
            i += 1
        close_index = i
    return {'open': open_index, 'close': close_index}


def add_math(function: str) -> str:
    i = 0
    while i < len(function):
        if function[i].isalpha() and function[i] != 'x':
            function = function[:i] + 'math.' + function[i:]
            i += 5  # i += len('math.')
            while function[i].isalpha():
                i += 1
                if i == len(function):
                    break
        else:
            i += 1
    function = function.replace('math.int', 'int')
    return function


def convert_absolute_value(function: str) -> str:
    if '|' not in function:
        return function
    parenthesis = get_1st_parenthesis(function, '|', '|')
    function = (function[:parenthesis['open']]
                + 'abs('
                + function[parenthesis['open']+1:parenthesis['close']]
                + ')'
                + function[parenthesis['close']+1:])
    return function


def add_multiplication(function: str) -> str:
    if 'ex' in function and 'exp' not in function:
        x_ind = function.find('ex') + 1
        print(x_ind)
        function = function[:x_ind] + '*' + function[x_ind:]
    for i in range(1, len(function)):
        if (function[i - 1].isnumeric() and function[i].isalpha()
                or function[i - 1] == 'π' and function[i].isalpha()):
            function = function[:i] + '*' + function[i:]
    return function


# def convert_factorial(function: str) -> str:
#     if 'fact' not in function:
#         return function
#     # fact(...),    factorial(...)
#     parenthesis = get_1st_parenthesis(function, '(', ')')
#     open_ = parenthesis['open']
#     close_ = parenthesis['close']
#     # fact(int(...))
#     function = function[:open_+1] + 'int(' + function[open_+1:close_] + ')' + function[close_:]
#     return function
# no longer needed - used gamma instead


def convert_factorial_to_gamma(function: str) -> str:
    if 'fact' not in function:
        return function
    # fact(x) -> gamma(x+1)
    function = function.replace('factorial', 'gamma')
    function = function.replace('fact', 'gamma')

    parenthesis = get_1st_parenthesis(function, '(', ')')
    close_ = parenthesis['close']
    function = function[:close_] + '+1' + function[close_:]
    return function


def convert_function_notation(function: str) -> str:
    if '(' not in function:
        function = add_multiplication(function)
        function = convert_absolute_value(function)

        function = function.replace('^', '**')
        function = function.replace(':', '/')
        function = function.replace('π', 'pi')
        function = function.replace('%', '/100')
        function = function.replace('abs', 'fabs')
        function = function.replace('ffabs', 'fabs')
        if 'gamma' not in function:
            function = function.replace('factorial', 'gamma')
            function = function.replace('fact', 'gamma')

        function = add_math(function)
        return function

    else:
        if '|' in function and function.find('|') < function.find('('):
            function = convert_absolute_value(function)
        if 'fact' in function and function.find('fact') < function.find('('):
            function = convert_factorial_to_gamma(function)

        parenthesis = get_1st_parenthesis(function, '(', ')')

        result_left = convert_function_notation(function[:parenthesis['open']])
        result_mid = convert_function_notation(function[parenthesis['open'] + 1:parenthesis['close']])
        result_end = convert_function_notation(function[parenthesis['close']+1:])

        return result_left + '(' + result_mid + ')' + result_end


def is_correct(function: str) -> bool:
    if function.count('(') != function.count(')'):
        print('Wrong format:')
        print('\'(\' appears ' + str(function.count('(')) + ' times')
        print('\')\' appears ' + str(function.count(')')) + ' times')
        return False
    if '!' in function:
        print('Wrong format:')
        print('Use factorial() or fact() instead of \'!\' symbol')
        return False
    if '√' in function:
        print('Wrong format:')
        print('Use sqrt() instead of \'√\' symbol')
        return False
    return True


def unscaled(x):
    return eval(input_function)


def f(x):
    return -input_y_scale * unscaled(x / input_x_scale)


if __name__ == "__main__":
    input_function = input('Enter a function f(x) = ')
    while not is_correct(input_function):
        input_function = input('Enter a function f(x) = ')

    input_function = convert_function_notation(input_function)

    input_domain_start = int(input('Enter domain start: '))
    input_domain_end = int(input('Enter domain end: '))
    input_x_scale = float(input('Enter x axis scale: '))
    input_y_scale = float(input('Enter y axis scale: '))

    if input_x_scale >= 1 and input_y_scale >= 1:
        domain = range(int(input_x_scale * input_domain_start), int(input_x_scale * input_domain_end + 1))
    else:
        domain = range(input_domain_start, input_domain_end + 1)

    print()
    print('Python notation:', input_function)
    print('Drawing ', end='')
    if input_y_scale != 1:
        print(input_y_scale, end='*')
    print('f(x', end='')
    if input_x_scale != 1:
        print('/' + str(input_x_scale), end='')
    print(')')

    draw(f, domain)
