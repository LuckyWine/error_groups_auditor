from data_getter import DataGetter
from error_group_auditor import ErrorGroupAuditor


def validate_error_groups() -> None:
    data_getter = DataGetter()
    error_groups = data_getter.get_error_groups()
    tracebacks = data_getter.get_tracebacks()
    auditor = ErrorGroupAuditor(error_groups, tracebacks)
    auditor.classify_tracebacks()
    zero_groups, non_zero_groups = auditor.highlight_groups(unique_group_is_empty=True)
    unique_groups, multi_groups = auditor.highlight_groups(unique_group_is_empty=False)
    total_connected_components, connected_components = auditor.find_connected_components(multi_groups)
