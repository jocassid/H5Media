
from itertools import count, cycle
from typing import List, Union

from django.core.paginator import Page, Paginator
from django.template import Library

register = Library()

# This should be an odd number so current page is can be centered, at least
# if there is an odd number of items.
PAGINATOR_ITEMS = 9

ITEMS_TO_EACH_SIDE_OF_CENTER = 2


def count_for_steps(num_steps: int, start: int = 0, step: int = 1):
    for i, count_value in enumerate(count(start, step), 1):
        if i > num_steps:
            break
        yield count_value


# class Foo:
#
#     def __init__(self, paginator_items: int = PAGINATOR_ITEMS):
#         self.paginator_items = paginator_items
#
#     def get_paginator_items(
#             self,
#             page_num: int,
#             num_pages: int,
#     ) -> List[Union[int, str]]:
#
#         if num_pages < self.paginator_items:
#             return [i for i in range(1, num_pages + 1)]
#
#         page_numbers: List[Union[None, int, str]] = [
#             None for _ in range(self.paginator_items)
#         ]
#         page_numbers[0] = 1
#         page_numbers[-1] = num_pages
#         print(f"{page_numbers}")
#
#         return page_numbers

def get_paginator_items(
        page_num: int,
        num_pages: int,
        paginator_items: int = PAGINATOR_ITEMS,
        items_to_each_side_of_center: int = ITEMS_TO_EACH_SIDE_OF_CENTER,
) -> List[Union[int, str]]:
    if num_pages <= paginator_items:
        return list(range(1, num_pages + 1))

    items = [page_num]
    page_before = page_num - 1
    page_after = page_num + 1
    for insert_front in cycle([True, False]):

        if insert_front:
            if page_before > 0:
                items.insert(0, page_before)
                page_before -= 1
        else:
            if page_after <= num_pages:
                items.append(page_after)
                page_after += 1

        if len(items) >= paginator_items:
            break

        if page_before <= 0 and page_after > num_pages:
            break

    if items[0] != 1:
        items[0] = 1
        items[1] = '...'

    if items[-1] != num_pages:
        items[-1] = num_pages
        items[-2] = '...'

    return items


def get_paginator_items2(
        page_num: int,
        num_pages: int,
        paginator_items: int = PAGINATOR_ITEMS,
        items_to_each_side_of_center: int = ITEMS_TO_EACH_SIDE_OF_CENTER,
) -> List[Union[int, str]]:
    """
    Helper function to generate list of page numbers for pagination
    """
    if num_pages <= paginator_items:
        return list(range(1, num_pages + 1))

    print('V' * 40)
    print(f"{page_num=}")
    print(f"{num_pages=}")
    print(f"{paginator_items=}")

    pages_before = page_num - 1
    pages_after = num_pages - page_num

    print(f"{pages_before=}")
    print(f"{pages_after=}")

    if pages_before == 0 and pages_after == 0:
        return [page_num]
    if pages_before == 0 and pages_after > 0:
        return list(range(1, num_pages - 2)) + ['...', num_pages]
    if pages_before > 0 and pages_after == 0:
        remaining_items = list(
            count_for_steps(
                paginator_items - 2,
                start=num_pages,
                step=-1,
            )
        )
        remaining_items.reverse()
        return [1, '...'] + remaining_items

    middle_index = paginator_items // 2
    print(f"{middle_index=}")

    slots_before = middle_index - 1
    slots_after = paginator_items - middle_index
    print(f"{slots_before=}")
    print(f"{slots_after=}")

    ellipsis_start = pages_before > slots_before
    ellipsis_end = pages_after > slots_after
    print(f"{ellipsis_start=}")
    print(f"{ellipsis_end=}")

    items: List[Union[None, int, str]] = [None] * paginator_items
    items[0] = 1
    items[-1] = num_pages

    if not ellipsis_start and not ellipsis_end:
        raise NotImplemented("how does this happen?")
    elif not ellipsis_start and ellipsis_end:
        items[1] = '...'
        current_page = 2
        for i in range(2, num_pages):
            items[i] = current_page
            current_page += 1
    elif ellipsis_start and not ellipsis_end:
        pass
    else:
        pass

    return items









    # foo = Foo(paginator_items)
    # return foo.get_paginator_items(page_num, num_pages)

    # if num_pages <= paginator_items:
    #     return list(range(1, num_pages + 1))
    #
    # print('foo')
    # page_numbers = []
    # pages_before = page_num - 1
    # pages_after = num_pages - page_num
    # print(f"{pages_before=}  {pages_after=}")
    #
    # if pages_before > 0:
    #     if pages_before > items_to_each_side_of_center:
    #         page_numbers.extend([1, '...'])
    #         items_before_page_num = list(
    #             count_for_steps(
    #                 items_to_each_side_of_center,
    #                 page_num - 1,
    #                 step=-1,
    #             )
    #         )
    #         items_before_page_num.reverse()
    #         page_numbers.extend(items_before_page_num)
    #     else:
    #         page_numbers.extend(range(1, page_num))
    #
    # page_numbers.append(page_num)
    #
    # if pages_after > 0:
    #     if pages_after > items_to_each_side_of_center:e
    #         steps = paginator_items - len(page_numbers) - 2
    #         page_numbers.extend(
    #             count_for_steps(steps, page_num + 1)
    #         )
    #         page_numbers.extend(['...', num_pages])
    #     else:
    #         pass
    pass




@register.simple_tag
def pagination(page: Page):
    return "Start of pagination tag"
