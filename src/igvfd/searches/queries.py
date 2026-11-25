from snosearch.queries import BasicSearchQueryFactory


class BasicSearchQueryFactoryWithSort(BasicSearchQueryFactory):

    def build_query(self):
        super().build_query()
        self.add_sort()
        return self.search
