from datetime import timedelta

class merger(object):

    @staticmethod
    # TODO: For now ignoring differences in field existance, thus comparing only those fields which exist in both items
    def merge_objects(map1, map2, priority_on_map1 = True, skip_fields = None, selected_fields = None, map1_updates = None, map2_updates = None, update_on_updates_diff = False, update_originals = False):
        map3 = {} # Resulting merged object
        map3_updates = {} # Latest update dates for object fields
        map1_changes = [] # What need to be changed in map1
        map2_changes = [] # What need to be changed in map2

        if selected_fields is not None:
            fields = selected_fields
        else:
            fields = list(set(map1.keys())|set(map2.keys()))

        if skip_fields != None:
            fields = list(set(fields) - set(skip_fields))

        if map1_updates == None:
            map1_updates = {}
        if map2_updates == None:
            map2_updates = {}


        for f in fields:
            m1_value = map1[f] if f in map1.keys() else None
            m2_value = map2[f] if f in map2.keys() else None

            m1_update = map1_updates[f] if f in map1_updates.keys() else None
            m2_update = map2_updates[f] if f in map2_updates.keys() else None

            m3_value = None
            map3_update = None

            if m1_update == None and m2_update == None: # Either both are equal values or both don't exist
                delta = 0
            elif m1_update != None and m2_update != None:
                if m1_update > m2_update:
                    delta = 1
                else:
                    delta = -1
            else: # If information for one of them is not available, considering as the same
                delta = 0

            if m1_value != m2_value or (delta != 0 and update_on_updates_diff == True):
                if (delta == 0 and priority_on_map1 == True) or (delta > 0):
                    m3_value = m1_value
                    map3_update = m1_update
                    map2_changes.append(f)
                    if update_originals == True:
                        map2[f] = m1_value
                else:
                    m3_value = m2_value
                    map3_update = m2_update
                    map1_changes.append(f)
                    if update_originals == True:
                        map1[f] = m2_value
            else:
                m3_value = m1_value
                map3_update = m1_update

            map3[f] = m3_value
            map3_updates[f] = map3_update

        return {'merged':map3,'merged_updated':map3_updates,'map1_changes':map1_changes,'map2_changes':map2_changes}