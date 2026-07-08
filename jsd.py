import numpy as np
import pandas as pd
import calendar

class jsd():

    def __init__(self, source):
        
        if isinstance(source, str):
            self.name = source
            self.dataframe = pd.read_excel(self.name)
        else:
            self.dataframe = pd.DataFrame(source)
        
        self.dataframe.fillna('', inplace=True)

    def is_hybrid(self):
        return self.dataframe[self.dataframe['Hybrid or OP'].str.contains("hybrid")].sort_index()
    
    def is_crop(self, name):
        if not isinstance(name, str):
            raise TypeError("name should be a string")
        
        df1 = self.dataframe[self.dataframe['Crop'].str.contains(name)]
        df2 = self.dataframe[self.dataframe['Crop'].str.contains(name.lower())]
        df3 = self.dataframe[self.dataframe['Crop'].str.contains(name.capitalize())]
        return pd.concat([df1, df2, df3], axis=0).drop_duplicates().sort_index()
    
    def is_heat_tolerant(self):
        return self.dataframe[self.dataframe['Weather Tolerance'].str.contains('heat')]
    
    def is_rain_tolerant(self):
        return self.dataframe[self.dataframe['Weather Tolerance'].str.contains('rain')]
    
    def is_transport_storage_good(self):
        return self.dataframe[self.dataframe['Transport and storage property'].str.contains('good')]
    
    def is_maturity_within(self, days):
        lower_bounds = self.dataframe['Maturity (days)'].apply(
            lambda x: x if isinstance(x, int) else int(x.split('-')[0])
        )
        return self.dataframe[(lower_bounds <= days).tolist()]
    
    def is_weight(self, fweight):
        lower_bounds = self.dataframe['Weight (g)'].apply(
            lambda x: x if isinstance(x, int) else int(x.split('-')[0])
        )
        upper_bounds = self.dataframe['Weight (g)'].apply(
            lambda x: x if isinstance(x, int) else int(x.split('-')[-1])
        )
        return self.dataframe[(np.array(lower_bounds <= fweight) & np.array(fweight <= upper_bounds)).tolist()]
    
    def is_bigger_than(self, fsize):
        lower_bounds = self.dataframe['Fruit Size (cm)'].apply(
            lambda x: x if isinstance(x, int) else int(x.split('-')[0])
        )
        return self.dataframe[(lower_bounds >= fsize).tolist()]
    
    def is_size(self, fsize):
        lower_bounds = self.dataframe['Fruit Size (cm)'].apply(
            lambda x: x if isinstance(x, int) else int(x.split('-')[0])
        )
        upper_bounds = self.dataframe['Fruit Size (cm)'].apply(
            lambda x: x if isinstance(x, int) else int(x.split('-')[-1])
        )
        return self.dataframe[(np.array(lower_bounds <= fsize) & np.array(fsize <= upper_bounds)).tolist()]
        
    def is_month_between(self, month_str, start_str, end_str):
        # Convert month to number
        month   = list(calendar.month_name).index(month_str)
        start   = list(calendar.month_name).index(start_str)
        end     = list(calendar.month_name).index(end_str)

        if start <= end:
            # Normal linear range
            return start <= month <= end
        else:
            # Wrap‑around: e.g., start = 11 (Nov), end = 2 (Feb)
            return month >= start or month <= end
        
    def is_cultivation_time(self, month_str):
        sl = self.dataframe['Sowing and transplant starting time'].tolist()
        el = self.dataframe['Sowing and transplant ending time'].tolist()
        return self.dataframe[[self.is_month_between(month_str, s, e) for s, e in zip(sl, el)]]
    
    def is_best_cultivation_time(self, month_str):
        sl = self.dataframe['Best sowing and transplant starting time'].tolist()
        el = self.dataframe['Best sowing and transplant ending time'].tolist()
        return self.dataframe[[self.is_month_between(month_str, s, e) for s, e in zip(sl, el)]]
    
    def is_allyear(self, best=None):
        if best != None:
            sl = self.dataframe['Best sowing and transplant starting time'].tolist()
            el = self.dataframe['Best sowing and transplant ending time'].tolist()    
        else:
            sl = self.dataframe['Sowing and transplant starting time'].tolist()
            el = self.dataframe['Sowing and transplant ending time'].tolist()
        blist = np.ones(len(sl), dtype=bool)
        for month_str in calendar.month_name[1:]:
            blist &= np.array([self.is_month_between(month_str, s, e) for s, e in zip(sl, el)])
        return self.dataframe[blist]