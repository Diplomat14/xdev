from datetime import timedelta

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
    def __init__(self,merged_obj,left_changed_fields,right_changed_fields):
        assert isinstance(merged_obj, merge_object)
        assert isinstance(left_changed_fields, list)
        assert isinstance(right_changed_fields, list)

        self.__merged_object = merged_obj
        self.__left_changed_fields = left_changed_fields
        self.__right_changed_fields = right_changed_fields

    @property
    def merged_object(self):
        return self.__merged_object

    @property
    def left_changed_fields(self):
        return self.__left_changed_fields

    @property
    def right_changed_fields(self):
        return self.__right_changed_fields


class merger(object):

    @staticmethod
    # TODO: For now ignoring differences in field existance, thus comparing only those fields which exist in both items
    def merge_objects(left, right, priority_on_left = True, skip_fields = None, selected_fields = None, update_on_updates_diff = False, update_originals = False):
        assert isinstance(left, merge_object)
        assert isinstance(right, merge_object)

        merged = {} # Resulting merged object
        merged_updates = {} # Latest update dates for object fields
        left_changes = [] # What need to be changed in left
        right_changes = [] # What need to be changed in right

        if selected_fields is not None:
            fields = selected_fields
        else:
            fields = list(set(left.data_map.keys())|set(right.data_map.keys()))

        if skip_fields != None:
            fields = list(set(fields) - set(skip_fields))

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

            if left_value != right_value or (delta != 0 and update_on_updates_diff == True):
                if (delta == 0 and priority_on_left == True) or (delta > 0):
                    merged_value = left_value
                    merged_update = left_update
                    right_changes.append(f)
                    if update_originals == True:
                        right.data_map[f] = left_value
                else:
                    merged_value = right_value
                    merged_update = right_update
                    left_changes.append(f)
                    if update_originals == True:
                        left.data_map[f] = right_value
            else:
                merged_value = left_value
                merged_update = left_update

            merged[f] = merged_value
            merged_updates[f] = merged_update

        return merge_result(merge_object(merged,merged_updates),left_changes,right_changes)