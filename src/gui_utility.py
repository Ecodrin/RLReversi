from typing import Any


def center_relative_to(element, relative_to, mode: str = 'both',
                       margins: tuple | list = (0, 0, 0, 0)) -> Any:
    """
    -----------
    |<x,y>    |
    |         |
    |         |
    -----------
    Объект вида <x, y> (относительно левого верхнего угла), <длина, высота>
    Отцентровывает объект относительно другого.
    В объектах обязательно должны быть координаты
    :param element: Объект для отцентровки
    :param relative_to: Объект относительно которого происходит отцентровка
    :param mode: Режим отцентровки (horizontally / vertically / both)
    :param margins: (отступы) расстояние в пикселях для отступа от центра,
    на вход принимается через массив (top, right, bottom, left).
    :return: Возвращает измененный объект, также изменяет его
    """
    coordinate_center_element = [relative_to[2] // 2 + relative_to[0] + margins[1] - margins[3],
                                 relative_to[3] // 2 + relative_to[1] + margins[2] - margins[0]]
    match mode:
        case 'both':
            element[0] = coordinate_center_element[0] - element[2] // 2
            element[1] = coordinate_center_element[1] - element[3] // 2
        case 'vertical':
            element[1] = coordinate_center_element[1] - element[3] // 2
        case 'horizontal':
            element[0] = coordinate_center_element[0] - element[2] // 2
        case _:
            raise ValueError('Invalid mode')

    return element
