import numpy as np
import pandas as pd
import calendar

class jsd():

    def __init__(self, source=None):

        self.name = None
        self.dataframe = None
        self.month_table = None
        
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
            
        self.month_table = None
        self.dataframe.fillna('', inplace=True)

    def set_month_table(self, month_table):
        self.month_table = pd.read_excel(month_table)

    def is_hybrid(self, bool_list=True):
        if bool_list:
            return self.dataframe['Hybrid or OP'].str.contains("hybrid").tolist()
        return self.dataframe[self.dataframe['Hybrid or OP'].str.contains("hybrid")].sort_index()
    
    def is_crop(self, name, bool_list=True):
        if not isinstance(name, str):
            raise TypeError("name should be a string")
        
        if bool_list:
            return self.dataframe['Crop'].str.contains(name).tolist()
        return self.dataframe[self.dataframe['Crop'].str.contains(name)]
    
    def is_zillion(self, bool_list=True):
        if bool_list:
            return self.dataframe['Company'].str.contains('Zillion').tolist()
        return self.dataframe[self.dataframe['Company'].str.contains('Zillion')]
    
    def is_heat_tolerant(self, bool_list=True):
        if bool_list:
            return self.dataframe['Weather tolerance'].str.contains('heat').tolist()
        return self.dataframe[self.dataframe['Weather tolerance'].str.contains('heat')]
    
    def is_rain_tolerant(self, bool_list=True):
        if bool_list:
            return self.dataframe['Weather tolerance'].str.contains('rain').tolist()
        return self.dataframe[self.dataframe['Weather tolerance'].str.contains('rain')]
    
    def is_transport_storage_good(self, bool_list=True):
        if bool_list:
            return self.dataframe['Transport and storage property'].str.contains('good').tolist()
        return self.dataframe[self.dataframe['Transport and storage property'].str.contains('good')]
    
    def is_maturity_within(self, days, bool_list=True):
        lower_bounds = self.dataframe['Maturity (days)'].apply(
            lambda x: x if isinstance(x, int) else int(x.split('-')[0])
        )
        if bool_list:
            return (lower_bounds <= days).tolist()
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
        
    def is_month_inlist(self, month_str, best=False, bool_list=True):
        if best:
            if bool_list:
                return self.month_table[month_str+' (best)'].tolist()
            return self.dataframe[self.month_table[month_str+' (best)'].tolist()]
        if bool_list:
            return self.month_table[month_str].tolist()
        return self.dataframe[self.month_table[month_str].tolist()]
        
    def is_cultivation_time(self, month_str, bool_list=True):
        sl = self.dataframe['Sowing and transplant starting time'].tolist()
        el = self.dataframe['Sowing and transplant ending time'].tolist()
        if bool_list:
            return [self.is_month_between(month_str, s, e) for s, e in zip(sl, el)]
        return self.dataframe[[self.is_month_between(month_str, s, e) for s, e in zip(sl, el)]]
    
    def is_best_cultivation_time(self, month_str, bool_list=True):
        sl = self.dataframe['Best sowing and transplant starting time'].tolist()
        el = self.dataframe['Best sowing and transplant ending time'].tolist()
        if bool_list:
            return [self.is_month_between(month_str, s, e) for s, e in zip(sl, el)]
        return self.dataframe[[self.is_month_between(month_str, s, e) for s, e in zip(sl, el)]]
    
    def is_allyear(self, best=False, bool_list=True):
        if best:
            sl = self.dataframe['Best sowing and transplant starting time'].tolist()
            el = self.dataframe['Best sowing and transplant ending time'].tolist()
        else:
            sl = self.dataframe['Sowing and transplant starting time'].tolist()
            el = self.dataframe['Sowing and transplant ending time'].tolist()
        blist = np.ones(len(sl), dtype=bool)
        for month_str in calendar.month_name[1:]:
            blist &= np.array([self.is_month_between(month_str, s, e) for s, e in zip(sl, el)])
        if bool_list:
            return blist
        return self.dataframe[blist]
    
    def make_month_list(self, filename):
        df = pd.DataFrame(columns=['Variety']+calendar.month_name[1:]+[month+' (best)' for month in calendar.month_name[1:]])
        df['Variety'] = self.dataframe['Variety']
        for month in calendar.month_name[1:]:
            df[month] = self.is_cultivation_time(month, bool_list=True)
            df[month+' (best)'] = self.is_best_cultivation_time(month, bool_list=True)

        df.to_excel(filename)

    def generate_list(self, crop_name='All', maturity_day='All', crop_type='All', brand_name='All', weather_tolerance='All', month='All'):

        variety_list = [True] * len(self.dataframe)

        # crop
        if crop_name != 'All':
            crop_list = self.is_crop(crop_name, bool_list=True)
            variety_list = [x and y for x, y in zip(crop_list, variety_list)]

        # maturity
        if maturity_day != 'All':
            maturity_list = self.is_maturity_within(int(maturity_day), bool_list=True)
            variety_list = [x and y for x, y in zip(maturity_list, variety_list)]

        # hybrid or OP
        if crop_type != 'All':
            type_list = self.is_hybrid(bool_list=True)
            if crop_type != 'Hybrid':
                type_list = [not x for x in type_list]
            variety_list = [x and y for x, y in zip(type_list, variety_list)]

        # brand
        if brand_name != 'All':
            brand_list = self.is_zillion(bool_list=True)
            if brand_name != 'Zillion':
                brand_list = [not x for x in brand_list]
            variety_list = [x and y for x, y in zip(brand_list, variety_list)]

        # weather tolerance
        if weather_tolerance != 'All':
            if weather_tolerance == 'Rain':
                weather_list = self.is_rain_tolerant(bool_list=True)
            elif weather_tolerance == 'Heat':
                weather_list = self.is_heat_tolerant(bool_list=True)
            else:
                rain_list = self.is_rain_tolerant(bool_list=True)
                heat_list = self.is_heat_tolerant(bool_list=True)
                weather_list = [x and y for x, y in zip(rain_list, heat_list)]
            variety_list = [x and y for x, y in zip(weather_list, variety_list)]

        # cultivation time
        if month != 'All':
            month_list = self.is_cultivation_time(month, bool_list=True)
            variety_list = [x and y for x, y in zip(month_list, variety_list)]

        return variety_list