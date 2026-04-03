from scripts.cortex.skeleton import get_node_skeleton


def test_get_node_skeleton_minimal():
    node_dict = {
        "signature": "def my_func():",
        "raw_body": '    """This is a docstring"""\n    pass'
    }
    result = get_node_skeleton(node_dict, detail="minimal")
    assert result == "def my_func():"

    # Missing signature
    result_no_sig = get_node_skeleton({}, detail="minimal")
    assert result_no_sig == ""


def test_get_node_skeleton_standard_with_docstring():
    # Test with """
    node_dict1 = {
        "signature": "def func1():",
        "raw_body": '"""Docstring here"""\n    pass'
    }
    expected1 = 'def func1():\n    """Docstring here"""'
    assert get_node_skeleton(node_dict1, detail="standard") == expected1

    # Test with '''
    node_dict2 = {
        "signature": "def func2():",
        "raw_body": "'''Another docstring'''\n    pass"
    }
    expected2 = "def func2():\n    '''Another docstring'''"
    assert get_node_skeleton(node_dict2, detail="standard") == expected2

    # Test with /*
    node_dict3 = {
        "signature": "void func3() {",
        "raw_body": "/* C-style docstring */\n}"
    }
    expected3 = "void func3() {\n    /* C-style docstring */"
    assert get_node_skeleton(node_dict3, detail="standard") == expected3

    # Test with //
    node_dict4 = {
        "signature": "void func4() {",
        "raw_body": "// Single line docstring\n}"
    }
    expected4 = "void func4() {\n    // Single line docstring"
    assert get_node_skeleton(node_dict4, detail="standard") == expected4


def test_get_node_skeleton_standard_no_docstring():
    node_dict = {
        "signature": "def my_func():",
        "raw_body": "    pass\n    return"
    }
    result = get_node_skeleton(node_dict, detail="standard")
    assert result == "def my_func():"


def test_get_node_skeleton_standard_no_raw_body():
    node_dict = {
        "signature": "def my_func():"
    }
    result = get_node_skeleton(node_dict, detail="standard")
    assert result == "def my_func():"


def test_get_node_skeleton_full():
    node_dict = {
        "signature": "def my_func():",
        "raw_body": "line 1\nline 2\nline 3\nline 4\nline 5\nline 6\nline 7"
    }
    result = get_node_skeleton(node_dict, detail="full")
    expected = "line 1\nline 2\nline 3\nline 4\nline 5 ... (truncated)"
    assert result == expected

    # Test with fewer than 5 lines
    node_dict_short = {
        "signature": "def my_func():",
        "raw_body": "line 1\nline 2"
    }
    result_short = get_node_skeleton(node_dict_short, detail="full")
    expected_short = "line 1\nline 2 ... (truncated)"
    assert result_short == expected_short

    # Test with no raw_body
    node_dict_empty = {
        "signature": "def my_func():"
    }
    result_empty = get_node_skeleton(node_dict_empty, detail="full")
    assert result_empty == " ... (truncated)"
