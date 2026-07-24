import pandas as pd

class jsdd():

    def __init__(self, source=None):

        self.name = None
        self.dataframe = None
        
        if source != None:
            if isinstance(source, str):
                self.name = source
                self.dataframe = pd.read_excel(self.name)
            else:
                self.dataframe = pd.DataFrame(source)    
            self.dataframe.fillna('', inplace=True)

    def set_dataframe(self, source):

        if isinstance(source, str):
            self.name = source
            self.dataframe = pd.read_excel(self.name)
        else:
            self.dataframe = pd.DataFrame(source)
            
        self.dataframe.fillna('', inplace=True)

    def find(self, column, value, bool_list=True):

        if bool_list:
            return self.dataframe[column].str.contains(value).tolist()
        return self.dataframe[self.dataframe[column].str.contains(value)].sort_index()

    def generate_list(self, crop_name='All', cause='All', part_affected='All', status='All', rating='All'):
        variety_list = [True] * len(self.dataframe)

        # Crop
        if crop_name != 'All':
            crop_list = self.find(column='Crop', value=crop_name, bool_list=True)
            variety_list = [x and y for x, y in zip(crop_list, variety_list)]

        # Cause
        if cause != 'All':
            cause_list = self.find(column='Cause', value=cause, bool_list=True)
            variety_list = [x and y for x, y in zip(cause_list, variety_list)]

        # Part affected
        if part_affected != 'All':
            part_list = self.find(column='Part affected', value=part_affected, bool_list=True)
            variety_list = [x and y for x, y in zip(part_list, variety_list)]

        # Status
        if status != 'All':
            status_list = self.find(column='Status', value=status, bool_list=True)
            variety_list = [x and y for x, y in zip(status_list, variety_list)]

        # Status
        if rating != 'All':
            rating_list = self.find(column='Rating', value=rating, bool_list=True)
            variety_list = [x and y for x, y in zip(rating_list, variety_list)]

        return variety_list