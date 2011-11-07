'''Some utilitary function for parse user set data
'''
import re

VALUE_PATTERN = re.compile('^[\d]+')
UNITS = ('px', '%')
LOOK_X = ('left', 'center', 'right')
LOOK_Y = ('top', 'middle', 'bottom')
OVERFLOW = ('none', 'x', 'y', 'both')


def parse_size(string_value):
    '''Parse size value from string "WIDTHxHEIGHT"
    '''
    width, height = string_value.split('x')
    return int(width), int(height)


def parse_units(string_value):
    '''Parse units
    '''
    match = VALUE_PATTERN.match(string_value)
    if not match:
        raise ValueError('Could not parse value "%s"' % string_value)
    value = match.group(0)
    units = string_value.replace(value, '')
    if len(units) > 0 and units.lower() not in UNITS:
        raise ValueError('Unsupported units "%s"' % units)
    return int(value), len(units) > 0 and units.lower() or 'px'


def parse_crop(crop_string):
    '''Parse crop string
    '''
    parts = crop_string.split(' ')
    length = len(parts)
    if length == 0 or length > 4:
        raise ValueError('Usupported crop string')
    top_crop = parse_units(parts[0])
    if length == 1:
        return top_crop, top_crop, top_crop, top_crop
    else:
        left_crop = parse_units(parts[1])
        if length == 2:
            return top_crop, left_crop, top_crop, left_crop
        else:
            bottom_crop = parse_units(parts[2])
            if length == 3:
                return top_crop, left_crop, bottom_crop, left_crop
            else:
                return top_crop, left_crop, bottom_crop, parse_units(parts[3])


def parse_look(look_string):
    '''Parse look string
    '''
    look_y, look_x = look_string.split(' ')
    if look_y not in LOOK_Y or look_x not in LOOK_X:
        raise ValueError('Unsupported look string')
    return look_x, look_y
