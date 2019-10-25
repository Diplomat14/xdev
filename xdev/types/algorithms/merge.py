from datetime import timedelta
from enum import Enum, unique, auto


@unique
class resolve_conflict_t(Enum):
    #SKIP = auto()
    #NOTE = auto()
    LEFT = auto()
    RIGHT = auto()

class merge_rules(object):

    def __init__(self, resolve_conflict, fields_to_skip = {}, fields_to_process = None, update_on_updates_diff = False, update_originals = False):
        assert isinstance(resolve_conflict,resolve_conflict_t)

        self.__resolve_conflict = resolve_conflict
        self.__fields_to_skip = fields_to_skip
        self.__fields_to_process = fields_to_process
        self.__update_on_updates_diff = update_on_updates_diff
        self.__update_originals = update_originals

    @property
    def resolve_conflict(self):
        return self.__resolve_conflict

    @property
    def fields_to_skip(self):
        return self.__fields_to_skip

    @property
    def fields_to_proces(self):
        return self.__fields_to_process

    @property
    def update_on_updates_diff(self):
        return self.__update_on_updates_diff

    @property
    def update_originals(self):
        return self.__update_originals



class merge_object(object):

    def __init__(self,data_map,updates_map = {}):
        assert isinstance(data_map, dict)
        assert isinstance(updates_map, dict)

        self.__data_map = data_map
        self.__updates_map = updates_map

    @property
    def data_map(self):
        return self.__data_map

    @property
    def updates_map(self):
        return self.__updates_map


class merge_result(object):
    def __init__(self,merged_obj,left_changed_fields,right_changed_fields, conflicts):
        assert isinstance(merged_obj, merge_object)
        assert isinstance(left_changed_fields, list)
        assert isinstance(right_changed_fields, list)
        assert isinstance(conflicts, dict)

        self.__merged_object = merged_obj
        self.__left_changed_fields = left_changed_fields
        self.__right_changed_fields = right_changed_fields
        self.__conflicts = conflicts

    @property
    def merged_object(self):
        return self.__merged_object

    @property
    def left_changed_fields(self):
        return self.__left_changed_fields

    @property
    def right_changed_fields(self):
        return self.__right_changed_fields

    @property
    def conflicts(self):
        return self.__conflicts


class merger(object):

    @staticmethod
    # TODO: For now ignoring differences in field existance, thus comparing only those fields which exist in both items
    def merge_objects(left, right, rules):
        assert isinstance(left, merge_object)
        assert isinstance(right, merge_object)
        assert isinstance(rules, merge_rules)

        merged = {} # Resulting merged object
        merged_updates = {} # Latest update dates for object fields
        left_changes = [] # What need to be changed in left
        right_changes = [] # What need to be changed in right

        if rules.fields_to_proces is not None:
            fields = rules.fields_to_proces
        else:
            fields = list(set(left.data_map.keys())|set(right.data_map.keys()))

        if rules.fields_to_skip != None:
            fields = list(set(fields) - set(rules.fields_to_skip))

        for f in fields:
            left_value = left.data_map[f] if f in left.data_map.keys() else None
            right_value = right.data_map[f] if f in right.data_map.keys() else None

            left_update = left.updates_map[f] if f in left.updates_map.keys() else None
            right_update = right.updates_map[f] if f in right.updates_map.keys() else None

            merged_value = None
            merged_update = None

            if left_update == None and right_update == None: # Either both are equal values or both don't exist
                delta = 0
            elif left_update != None and right_update != None:
                if left_update > right_update:
                    delta = 1
                else:
                    delta = -1
            else: # If information for one of them is not available, considering as the same
                delta = 0

            if left_value != right_value or (delta != 0 and rules.update_on_updates_diff == True):
                if (delta == 0 and rules.resolve_conflict == resolve_conflict_t.LEFT) or (delta > 0):
                    merged_value = left_value
                    merged_update = left_update
                    right_changes.append(f)
                    if rules.update_originals == True:
                        right.data_map[f] = left_value
                else:
                    merged_value = right_value
                    merged_update = right_update
                    left_changes.append(f)
                    if rules.update_originals == True:
                        left.data_map[f] = right_value

            else:
                merged_value = left_value
                merged_update = left_update

            merged[f] = merged_value
            merged_updates[f] = merged_update

        return merge_result(merge_object(merged,merged_updates),left_changes,right_changes, {})