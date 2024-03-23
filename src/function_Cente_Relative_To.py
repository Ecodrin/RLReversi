def center_relative_to(object_for_center, relative_center, center_mode: str = 'both',
                       murgins: tuple = (1000, 1000, 1000, 1000)) -> None:
    """
    -----------
    |<x,y>    |
    |         |
    |         |
    -----------
    Объект вида<x, y(относительно левого верхнего угла), длина, высота>
    Отцентровывает объект относительно другого (посередине?).
    В объектах обязательно должны быть координаты
    :param object_for_center: Объект для оцентровки
    :param relative_center: Объект относительно которого происходит оцентровка
    :param center_mode: Режим оцентровки (horizontally / vertically / both)
    :param murgins: (отступы) расстояние в пикселях для отступа от центра,
    на вход принимается через массив (top, right, bottom, left).
    :return:
    """
    coordinate_center_object = [relative_center[2] // 2 + relative_center[0], relative_center[3] // 2 + relative_center[1]]
    object_top_right_bottom_left: list[int] = [object_for_center[3] // 2, object_for_center[2] // 2,
                                               object_for_center[3] // 2, object_for_center[2] // 2]
    # Сравниваем murgins и текущую длину объекта, чтобы взять наименьшую величину
    if object_for_center[3] // 2 > murgins[0]:
        object_top_right_bottom_left[0] = murgins[0]
    if object_for_center[3] // 2 > murgins[2]:
        object_top_right_bottom_left[2] = murgins[2]
    if object_for_center[2] // 2 > murgins[1]:
        object_top_right_bottom_left[1] = murgins[1]
    if object_for_center[2] // 2 > murgins[3]:
        object_top_right_bottom_left[3] = murgins[3]

    # Работаем по режимам
    if center_mode == 'both':
        object_for_center[0] = coordinate_center_object[0] - object_top_right_bottom_left[1]
        object_for_center[1] = coordinate_center_object[1] - object_top_right_bottom_left[0]
    elif center_mode == 'horizontally':
        object_for_center[0] = coordinate_center_object[0] - object_top_right_bottom_left[1]
    elif center_mode == 'vertically':
        object_for_center[1] = coordinate_center_object[1] - object_top_right_bottom_left[0]
    else:
        raise ValueError(f'Ошибка, передан неверный режим оцентровки')
    object_for_center[2] = object_top_right_bottom_left[1] + object_top_right_bottom_left[3]
    object_for_center[3] = object_top_right_bottom_left[0] + object_top_right_bottom_left[2]
