from enum import Enum

class MutantType(Enum):
    """An Enum representing the different statuses assigned to mutants during a pipeline of checks.
    The mutants are filtered in a step-by-step manner, where each step updates their status
    based on specific criteria. Only the mutants that pass the checks are moved to the next step.

    Attributes:
        UNKNOWN: This status is assigned to mutants when they are initially created from a response generated
            by the LLM model. These mutants are yet to be evaluated, and further classification is required.
        WRONG_REPORT: A mutant with this status indicates that the `pre_code` returned by the model is incorrect.
            Even if the mutant is parsable, it is discarded and removed from the final report because the `pre_code` is faulty.
        UNPARSABLE: This mutant is not a "Wrong Report," but it cannot be parsed. It is still discarded from
            the final report.
        UNCHANGED: This mutant is parsable but does not introduce any syntactical changes (e.g., changing
            comments would be considered "unchanged"). Such mutants are removed from the final report because they do not
            represent meaningful changes to the code.
        DUPLICATE: This mutant is not a "Wrong Report," is parsable, and is not "Unchanged." However, there are
            multiple instances of the same mutant in the mutant list generated for a given Python module.
            In the final report, only one instance of such mutants is kept and reported as VALID,
            and the rest are discarded as duplicates.
        VALID: This mutant is not a "Wrong Report," is parsable, and is not "Unchanged." It is the first
            instance in a group of duplicates or appears only once in the mutant list generated for the targeted Python module.
            It is kept in the final report as a VALID mutant.

    Note:
        - UNCHANGED mutants are a subset of equivalent mutants, which could have syntactical changes but maintain
          the same logic. Since equivalent mutants are difficult to detect fully (an open problem), we filter only
          the syntactically unchanged ones.
        - A mutant type such as "Runtime Error" might also be considered, especially in dynamically typed languages
          like Python. However, further research is required to determine whether to remove these mutants, as the base
          paper does not provide specific guidance on handling them.
    """

    UNKNOWN = "Unknown"
    WRONG_REPORT = "Wrong Report"
    UNPARSABLE = "Unparsable"
    UNCHANGED = "Unchanged"
    DUPLICATE = "Duplicate"
    VALID = "Valid"
