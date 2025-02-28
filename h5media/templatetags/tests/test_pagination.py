
from collections import namedtuple

from django.test import TestCase

from h5media.templatetags.pagination import count_for_steps, get_paginator_items


class PaginationTest(TestCase):

    def test_count_steps(self):

        self.assertEqual(
            [0, 1, 2, 3],
            list(count_for_steps(4)),
        )

        self.assertEqual(
            [3, 4, 5],
            list(
                count_for_steps(3, 3)
            )
        )

    def test_get_paginator_items(self):

        TestGroup = namedtuple(
            'TestGroup',
            ['paginator_items', 'test_sets'],
        )

        # have tests to run < paginator items and page_num == all pages for
        # paginator items in (5, 6)
        test_groups = (
            TestGroup(
                5,
                (
                    (1, 4, [1, 2, 3, 4]),  # num_pages < paginator_items
                    (1, 6, [1, 2, 3, '...', 6]),
                    (2, 6, [1, 2, 3, '...', 6]),
                    (3, 6, [1, 2, 3, '...', 6]),
                    (4, 6, [1, '...', 4, 5, 6]),
                    (5, 6, [1, '...', 4, 5, 6]),
                    (6, 6, [1, '...', 4, 5, 6]),
                    (3, 7, [1, 2, 3, '...', 7]),
                    (4, 7, [1, '...', 4, '...', 7]),
                )
            ),
        )

        for test_group in test_groups:
            for page_num, num_pages, expected in test_group.test_sets:
                with self.subTest(
                        paginator_items=test_group.paginator_items,
                        page_num=page_num,
                        num_pages=num_pages,
                        expected=expected
                ):
                    self.assertEqual(
                        expected,
                        get_paginator_items(
                            page_num=page_num,
                            num_pages=num_pages,
                            paginator_items=test_group.paginator_items,
                        )
                    )







        self.fail()
