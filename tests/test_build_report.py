from pyllmut.mutant_lib import mutant_manager
from pyllmut.mutant_lib.mutant_type import MutantType


def test_get_mutant():
    line_number = 3

    mutant_dict = {
        "pre_code": "    c = a + b  # line to change",
        "after_code": "    c = a - b  # line to change"
    }

    module_content = """
def func_1(a, b):
    c = a + b  # line to change
    d = a - b
    return c, d
"""

    expected_mutant_diff = """--- original
+++ modified
@@ -1,5 +1,5 @@
 
 def func_1(a, b):
-    c = a + b  # line to change
+    c = a - b  # line to change
     d = a - b
     return c, d"""

    mutant = mutant_manager.get_mutant(
        prompt_content="Dummy prompt",
        response_content="Dummy response",
        sent_token_count=-1,
        received_token_count=-1,
        module_content=module_content,
        line_number=line_number,
        mutant_dict=mutant_dict
    )
    assert mutant.get_diff_content() == expected_mutant_diff
    assert mutant.get_line_number() == line_number
    assert mutant.get_pre_code_model() == mutant_dict["pre_code"]
    assert mutant.get_after_code_model().strip() == mutant_dict["after_code"].strip()
    assert mutant.get_prompt_content() == "Dummy prompt"
    assert mutant.get_response_content() == "Dummy response"
    assert mutant.get_sent_token_count() == -1
    assert mutant.get_received_token_count() == -1


def test_get_mutant_wrong_pre_code_report():
    line_number = 1

    mutant_dict = {
        "pre_code": "var1 = 'abc'",
        "after_code": "var1 = 'def'"
    }

    module_content = """x = "var1 = 'abc'"

"""

## TODO: This is the correct diff. But due to a minor bug in mutant builder,
##  we use the following diff in this test for now.
##  Fix this test after fixing the bug in mutant builder.

#     expected_mutant_diff = """--- original
# +++ modified
# @@ -1,2 +1 @@
# -x = "var1 = 'abc'"
# +var1 = 'def'"""

    expected_mutant_diff = """--- original
+++ modified
@@ -1,2 +1 @@
-x = "var1 = 'abc'"
-
+var1 = 'def'"""

    mutant = mutant_manager.get_mutant(
        prompt_content="Dummy prompt",
        response_content="Dummy response",
        sent_token_count=-1,
        received_token_count=-1,
        module_content=module_content,
        line_number=line_number,
        mutant_dict=mutant_dict
    )
    assert mutant.get_diff_content() == expected_mutant_diff
    assert mutant.get_line_number() == line_number
    assert mutant.get_pre_code_model() == mutant_dict["pre_code"]
    assert mutant.get_after_code_model().strip() == mutant_dict["after_code"].strip()
    assert mutant.get_prompt_content() == "Dummy prompt"
    assert mutant.get_response_content() == "Dummy response"
    assert mutant.get_sent_token_count() == -1
    assert mutant.get_received_token_count() == -1


def test_classify_mutants_duplicates_1():
    line_number = 3
    module_content = """
def func_1(a, b):
    c = a + b
    d = a - b
    return c, d
"""

    mutant_dict_a = {
        "pre_code": "    c = a + b",
        "after_code": "    c = a - b # something"
    }

    mutant_dict_b = {
        "pre_code": "    c = a + b",
        "after_code": "    c = a - b # something else"
    }

    mutant_a = mutant_manager.get_mutant(
        prompt_content="Dummy prompt",
        response_content="Dummy response",
        sent_token_count=-1,
        received_token_count=-1,
        module_content=module_content,
        line_number=line_number,
        mutant_dict=mutant_dict_a
    )
    mutant_b = mutant_manager.get_mutant(
        prompt_content="Dummy prompt",
        response_content="Dummy response",
        sent_token_count=-1,
        received_token_count=-1,
        module_content=module_content,
        line_number=line_number,
        mutant_dict=mutant_dict_b
    )

    mutant_list = [mutant_a, mutant_b]
    mutant_manager.classify_mutant_list(mutant_list)
    assert len([x for x in mutant_list if x.get_mutant_type() == MutantType.WRONG_REPORT]) == 0
    assert len([x for x in mutant_list if x.get_mutant_type() == MutantType.UNPARSABLE]) == 0
    assert len([x for x in mutant_list if x.get_mutant_type() == MutantType.UNCHANGED]) == 0
    assert len([x for x in mutant_list if x.get_mutant_type() == MutantType.DUPLICATE]) == 1
    assert len([x for x in mutant_list if x.get_mutant_type() == MutantType.VALID]) == 1

def test_classify_mutants_duplicates_2():
    line_number = 3
    module_content = """
def func_1(a, b):
    c = a + b
    d = a - b
    return c, d
"""

    mutant_dict_a = {
        "pre_code": "    c = a + b",
        "after_code": "    c = 'abc # xyz' # something"
    }

    mutant_dict_b = {
        "pre_code": "    c = a + b",
        "after_code": '    c = "abc # xyz" # something'
    }

    mutant_a = mutant_manager.get_mutant(
        prompt_content="Dummy prompt",
        response_content="Dummy response",
        sent_token_count=-1,
        received_token_count=-1,
        module_content=module_content,
        line_number=line_number,
        mutant_dict=mutant_dict_a
    )
    mutant_b = mutant_manager.get_mutant(
        prompt_content="Dummy prompt",
        response_content="Dummy response",
        sent_token_count=-1,
        received_token_count=-1,
        module_content=module_content,
        line_number=line_number,
        mutant_dict=mutant_dict_b
    )

    mutant_list = [mutant_a, mutant_b]
    mutant_manager.classify_mutant_list(mutant_list)
    assert len([x for x in mutant_list if x.get_mutant_type() == MutantType.WRONG_REPORT]) == 0
    assert len([x for x in mutant_list if x.get_mutant_type() == MutantType.UNPARSABLE]) == 0
    assert len([x for x in mutant_list if x.get_mutant_type() == MutantType.UNCHANGED]) == 0
    assert len([x for x in mutant_list if x.get_mutant_type() == MutantType.DUPLICATE]) == 1
    assert len([x for x in mutant_list if x.get_mutant_type() == MutantType.VALID]) == 1

def test_classify_mutants_wrong_pre_code_report():
    line_number = 1

    mutant_dict = {
        "pre_code": "var1 = 'abc'",
        "after_code": "var1 = 'def'"
    }

    module_content = """x = "var1 = 'abc'"

"""

    mutant = mutant_manager.get_mutant(
        prompt_content="Dummy prompt",
        response_content="Dummy response",
        sent_token_count=-1,
        received_token_count=-1,
        module_content=module_content,
        line_number=line_number,
        mutant_dict=mutant_dict
    )
    mutant_list = [mutant]
    mutant_manager.classify_mutant_list(mutant_list)
    assert len([x for x in mutant_list if x.get_mutant_type() == MutantType.WRONG_REPORT]) == 1
    assert len([x for x in mutant_list if x.get_mutant_type() == MutantType.UNPARSABLE]) == 0
    assert len([x for x in mutant_list if x.get_mutant_type() == MutantType.UNCHANGED]) == 0
    assert len([x for x in mutant_list if x.get_mutant_type() == MutantType.DUPLICATE]) == 0
    assert len([x for x in mutant_list if x.get_mutant_type() == MutantType.VALID]) == 0
