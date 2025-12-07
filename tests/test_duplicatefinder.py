from duplicatefinder import find_duplicates


def test_find_duplicates_when_duplicates_exist():
    hashes_to_paths = {
        '123': ['/path/to/file1', '/path/to/file2'],
        '456': ['/path/to/file1']
    }

    duplicates = find_duplicates(hashes_to_paths)
    assert duplicates == {'123': ['/path/to/file1', '/path/to/file2']}


def test_find_duplicates_when_duplicates_do_not_exist():
    hashes_to_paths = {
        '123': ['/path/to/file1'],
        '456': ['/path/to/file2']
    }

    duplicates = find_duplicates(hashes_to_paths)
    assert duplicates == {}


def test_find_duplicates_empty_input():
    hashes_to_paths = {}
    duplicates = find_duplicates(hashes_to_paths)
    assert duplicates == {}


def test_find_duplicates_multiple_groups():
    hashes_to_paths = {
        '123': ['/path/to/file1', '/path/to/file2'],
        '456': ['/path/to/file3'],
        '789': ['/path/to/file4', '/path/to/file5', '/path/to/file6']
    }

    duplicates = find_duplicates(hashes_to_paths)
    assert len(duplicates) == 2
    assert '123' in duplicates
    assert '789' in duplicates
    assert len(duplicates['789']) == 3


def test_find_duplicates_exactly_two():
    hashes_to_paths = {
        '123': ['/path/to/file1', '/path/to/file2']
    }

    duplicates = find_duplicates(hashes_to_paths)
    assert len(duplicates['123']) == 2


def test_find_duplicates_many_in_one_group():
    paths = [f'/path/to/file{i}' for i in range(100)]
    hashes_to_paths = {'123': paths}

    duplicates = find_duplicates(hashes_to_paths)
    assert len(duplicates['123']) == 100
