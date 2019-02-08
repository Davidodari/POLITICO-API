# Generic Models
class Model:
    # Generic Class from which models will inherit from
    def __init__(self, item=None, item_id=0, list_of_items=None):
        self.item = item
        self.item_id = item_id
        self.list_of_items = list_of_items

    def get_specific_item(self):
        # Return specific item based on class that was called
        if self.item_id >= 1 and len(self.list_of_items) >= 1:
                list_item = [item for item in self.list_of_items if item['id'] == self.item_id]
                if len(list_item) > 0:
                    return list_item[0]
                return 'Doesnt Exist'
        return 'Invalid Id'

    def get_all_items_in_list(self):
        # Returns list of items for class that was called
        return self.list_of_items

    def remove_item(self):
        if self.item_id >= 1 and len(self.list_of_items) >= 1:
            # Remove if id matches
            del_item = [item for item in self.list_of_items if item['id'] == self.item_id]
            if len(del_item) == 0:
                return 'Doesnt Exist'
            # Return empty list
            return self.list_of_items.remove(del_item[0])
        # Incorrect id such as -1
        return 'Invalid Id'
