import re
from collections import defaultdict

import pandas as pd

Graph = dict[str, dict[str, int]]


class ErrorGroupAuditor:
    def __init__(self, error_groups: pd.DataFrame, tracebacks: pd.DataFrame):
        self._df_error_groups = error_groups
        self._df_tracebacks = tracebacks
        self._group_intersection_dictionary: Graph = defaultdict(lambda: defaultdict(int))

    def classify_tracebacks(self) -> None:
        for traceback in self._df_tracebacks.error_txt:
            classified_groups = self._get_classified_groups(traceback)
            total_classified_groups = len(classified_groups)
            if total_classified_groups == 1:
                classified_group = classified_groups[0]
                self._group_intersection_dictionary[classified_group][classified_group] += 1
                continue
            for i in range(total_classified_groups):
                for j in range(i + 1, total_classified_groups):
                    first_group = classified_groups[i]
                    second_group = classified_groups[j]
                    self._group_intersection_dictionary[first_group][second_group] += 1
                    self._group_intersection_dictionary[second_group][first_group] += 1

    def _get_classified_groups(self, traceback: str) -> list[str]:
        classified_groups = list()
        for _, row in self._df_error_groups.iterrows():
            for rule in row.Rules:
                if not re.search(rule, traceback):
                    break
            else:
                code = row.error_type_code
                classified_groups.append(code)
        return classified_groups

    def find_connected_components(self, graph: Graph) -> tuple[int, list[list[str]]]:
        def dfs(vertex: str, component: str) -> None:
            visited.add(vertex)
            components[vertex] = component
            for neighbor in graph[vertex]:
                if neighbor not in visited:
                    dfs(neighbor, component)

        visited: set[str] = set()
        components: dict[str, str] = {}
        for vertex in graph:
            if vertex not in visited:
                dfs(vertex, vertex)

        components_dict = defaultdict(list)
        for vertex, component in components.items():
            components_dict[component].append(vertex)

        return len(components_dict), list(components_dict.values())

    def highlight_groups(self, unique_group_is_empty: bool) -> tuple[set[str], Graph]:
        correct_groups = set()
        other_groups = dict()
        for group in self._group_intersection_dictionary:
            if (self._group_intersection_dictionary[group][group] == 0) == unique_group_is_empty and len(
                self._group_intersection_dictionary[group]
            ) == 1:
                correct_groups.add(group)
            else:
                other_groups[group] = self._group_intersection_dictionary[group]
        return correct_groups, other_groups
