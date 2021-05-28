from collections import namedtuple
from beancount.core.data import Transaction
from typing import Optional

__plugins__ = ['tag_hierarchy']

TagHierarchyError = namedtuple('TagHierarchyError', 'source message entry')


def splite_tags(tag: str, splited_tags: Optional[list] = None):
    if splited_tags is None:
        splited_tags = []
    splited_tags.append(tag)
    index = tag.rfind('.')
    if index == -1:
        return splited_tags
    else:
        return splite_tags(tag[:index], splited_tags)

def replace_tags(entry: Transaction):
    new_tags = set()
    for tag in entry.tags:
        new_tags.update(splite_tags(tag))
    return entry._replace(tags=new_tags)


def tag_hierarchy(entries, options_map):
    return [replace_tags(entry) if isinstance(entry, Transaction) else entry for entry in entries], []