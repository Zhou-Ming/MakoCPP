#!/usr/bin/env python
"""
"""

_Indentation = '  '

def indent():
    return _Indentation

def set_indent(indentation):
    _Indentation = indentation

def _tolist(x):
    if isinstance(x, list):
        return x
    else:
        return [x]

def comma(args):
    assert(isinstance(args, list))
    return ', '.join(args)

NO_SEMICOLON = (
    (
        '#',
        '/',
        ),
    (
        '/',
        ';',
        '{',
        '}',
        '(',
        ),
    )

def add_semicolon(content):
    """
    Added semicolon to finish a (list of) statement(s)
    """
    if isinstance(content, list):
        ret = []
        for i in content:
            if i[0] in NO_SEMICOLON[0] or i[-1] in NO_SEMICOLON[1]:
                ret.append(i)
            else:
                ret.append(i + ';')
    else:
        if content[0] in NO_SEMICOLON[0] or content[-1] in NO_SEMICOLON[1]:
            ret = content
        else:
            ret = content + ';'
    return ret

def body(content):
    if isinstance(content, list):
        return '\n'.join(content)
    else:
        return content

def defined(name):
    return 'defined(' + name + ')'

def define(name, value=None):
    if value:
        return '#define ' + name + ' ' + value
    else:
        return '#define ' + name

def _bit_op(content, op):
    if isinstance(content, list):
        assert(len(content) > 1)
        ret = op.join(content)
    else:
        raise TypeError
    return ret

def bool_not(content):
    return '!' + content

def bool_equal(content):
    return _bit_op(content, ' == ')

def bool_not_equal(content):
    return _bit_op(content, ' != ')

def bool_greater_than(content):
    return _bit_op(content, ' > ')

def bool_lesser_than(content):
    return _bit_op(content, ' < ')

def bool_greater_than_or_equal_to(content):
    return _bit_op(content, ' >= ')

def bool_lesser_than_or_equal_to(content):
    return _bit_op(content, ' <= ')

def bool_and(content):
    return _bit_op(content, ' && ')

def bit_and(content):
    return _bit_op(content, ' & ')

def bool_or(content):
    return _bit_op(content, ' || ')

def bit_or(content):
    return _bit_op(content, ' | ')

def bit_xor(content):
    return _bit_op(content, ' ^ ')

def bit_complement(content):
    return '~' + content

def bit_shift_left(content, shift):
    return content + ' << ' + shift

def bit_shift_right(content, shift):
    return content + ' >> ' + shift

def undef(name):
    prefix = '#undef '
    if isinstance(name, list):
        return [prefix + x for x in name]
    else:
        return prefix + name

def typedef(old, new):
    return 'typedef ' + old + ' ' + new

def assign(left, right):
    return left + ' = ' + right

def add(left, right):
    return left + ' + ' + right

def variable(t, name, value=None):
    if value:
        return t + ' ' +  name + ' = ' + value
    else:
        return t + ' ' +  name

def _ifelse(condition, true_content, false_content, formatter, indentation=''):
    ret = []
    if isinstance(condition, list):
        assert(isinstance(true_content, list))
        number_conditions = len(condition)
        assert(number_conditions == len(true_content))
        for i in range(number_conditions):
            if i > 0:
                ret.append(formatter[1].format(condition[i]))
            else:
                ret.append(formatter[0].format(condition[i]))
            ret += [indentation + x for x in _tolist(true_content[i])]
    else:
        ret.append(formatter[0].format(condition))
        ret += [indentation + x for x in _tolist(true_content)]
    if false_content:
        ret.append(formatter[2][0])
        ret += [indentation + x for x in _tolist(false_content)]
    ret.append(formatter[3][0])
    return ret

_IFELSE_STATEMENT = (
    'if ({0}) {{',
    '}} else if ({0}) {{',
    ('} else {', '}} else {{ // !{0}'),
    ('}', '}} // {0}'),
    )

_IFELSE_PREPROCESS = (
    '#if {0}',
    '#elif {0}',
    ('#else', '#else // !{0}'),
    ('#endif', '#endif // {0}'),
    )

_IFDEF_PREPROCESS = (
    '#ifdef {0}',
    '#elif {0}',
    ('#else', '#else // !{0}'),
    ('#endif', '#endif // {0}'),
    )

def ifelse(condition, true_content, false_content=None):
    return _ifelse(condition, true_content, false_content,
		   _IFELSE_STATEMENT, indent())

def ifdef(condition, true_content, false_content=None):
    return _ifelse(condition, true_content, false_content, _IFDEF_PREPROCESS)

def func_typedef(ret, t, args):
    return 'typedef ' + ret + ' (*' + t + ') (' + comma(args) + ')'

def func_dec(ret, name, args):
    return ret + ' ' + name + '(' + comma(args) + ')'

def func_def(ret, name, args, content):
    ret = [ret + ' ' + name + '(' + comma(args) + ')', '{']
    ret += [indent() + x for x in _tolist(content)]
    ret.append('}')
    return ret

def struct(name, content):
    ret = ['struct ' + name + ' {']
    ret += _tolist(content)
    ret.append('}')

def classcpp(name, parent,
             public_content=None,
             protected_content=None,
             private_content=None):
    class_def = 'class ' + name
    if parent:
        if isinstance(parent, list):
            class_def += ': ' + comma(parent) + ' {'
        else:
            class_def += ': ' + parent + ' {'
    else:
        class_def += '{'
    ret = [class_def]
    def add_content(tag, content):
        if content:
            ret.append(tag)
            ret += _tolist(content)
    add_content(public_content)
    add_content(protected_content)
    add_content(private_content)
    ret.append('}')
    return ret

def cpp_if(content):
    return ifdef('__cplusplus', content)

def cpp_guard(c_content, cpp_content):
    ret = cpp_if('extern "C" {')
    ret += _tolist(c_content)
    _cpp_content = ['}']
    _cpp_content += _tolist(cpp_content)
    ret += cpp_if(_cpp_content)
    return ret

def header_if_guard(header_name, c_content, cpp_content):
    guard_def = header_name.replace('/', '_').upper() + '_H_'
    ret = ['#ifndef ' + guard_def, define(guard_def)]
    ret += cpp_guard(c_content, cpp_content)
    ret.append('#endif // ' + guard_def)
    return ret

def include_bracket(header_name):
    return '#include <' + header_name + '>'

def include_quoted(header_name):
    return '#include "' + header_name + '"'

C_SYSTEM_HEADERS = (
    'stdio.h',
    'stdlib.h',
    'stdint.h',
    'string.h',
    'errno.h',
    )

def _include(header_name):
    if header_name in C_SYSTEM_HEADERS:
        return include_bracket(header_name)
    else:
        return include_quoted(header_name)

def include(header_name):
    if isinstance(header_name, list):
        ret = []
        for i in header_name:
            ret.append(_include(i))
    else:
        ret = _include(header_name)
    return ret
