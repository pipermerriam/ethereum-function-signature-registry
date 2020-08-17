from collections import namedtuple

ImportStats = namedtuple('ImportStats', ['num_processed', 'num_imported',
                                         'num_duplicates', 'num_ignored'])

def empty_import_stats():
    return ImportStats(
        num_processed=0,
        num_imported=0,
        num_duplicates=0,
        num_ignored=0,
    )

def retrieve_stats_from_import_results(raw_import_results):
    num_processed = len(raw_import_results)

    import_results = [
        result
        for result in raw_import_results
        if result is not None
    ]

    num_ignored = num_processed - len(import_results)

    if len(import_results) == 0:
        num_imported = 0
        num_duplicates = 0
    else:
        num_imported = sum(tuple(zip(*import_results))[1])
        num_duplicates = len(import_results) - num_imported

    return ImportStats(
        num_processed=num_processed,
        num_imported=num_imported,
        num_duplicates=num_duplicates,
        num_ignored=num_ignored,
    )