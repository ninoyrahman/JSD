import numpy as np
import pandas as pd
import calendar

class jsd():
    """
    A class for managing and querying a dataset of crop varieties.

    The dataset typically contains information about variety name, crop type,
    maturity days, weight, fruit size, weather tolerance, sowing/transplanting
    windows, and other properties. This class provides filtering methods and
    utilities to generate boolean lists or filtered DataFrames based on various
    criteria, making it easy to select varieties that meet specific conditions.

    Attributes:
        name (str or None): The filename (if data was loaded from an Excel file).
        dataframe (pd.DataFrame): The main dataset.
        month_table (pd.DataFrame or None): An optional month‑wise table (e.g.,
            for best sowing months) that can be loaded separately.
    """

    def __init__(self, source=None):
        """
        Initialize a jsd instance.

        Args:
            source (str or pandas DataFrame, optional): If a string, it is treated
                as a file path to an Excel file to load. If a DataFrame, it is used
                directly. If None, an empty instance is created. Defaults to None.

        The DataFrame is filled with empty strings for missing values.
        """
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
        """
        Set (or replace) the main DataFrame from a source.

        Args:
            source (str or pandas DataFrame): If a string, it is treated as a file
                path to an Excel file. Otherwise, it must be a DataFrame.

        The month_table is reset to None and missing values are filled with ''.
        """
        if isinstance(source, str):
            self.name = source
            self.dataframe = pd.read_excel(self.name)
        else:
            self.dataframe = pd.DataFrame(source)
            
        self.dataframe.fillna('', inplace=True)

    def set_month_table(self, month_table):
        """
        Load a separate month table from an Excel file.

        This table is expected to contain columns for each month (and optionally
        'month (best)' columns) that indicate whether a variety is suitable.

        Args:
            month_table (str): File path to the Excel file containing the month table.
        """
        self.month_table = pd.read_excel(month_table)

    def find(self, column, value, bool_list=True):
        """
        Search a column for a substring or regular expression pattern.

        Args:
            column (str): The name of the target column to search within.
            value (str): The substring or regular expression pattern to match.
            bool_list (bool, optional): If True, return a list of booleans. If False, return
                a filtered DataFrame. Defaults to True.

        Returns:
            list of bool or pd.DataFrame
        """
        if bool_list:
            return self.dataframe[column].str.contains(value).tolist()
        return self.dataframe[self.dataframe[column].str.contains(value)].sort_index()

    def is_maturity_within(self, days, bool_list=True):
        """
        Filter varieties whose maturity (in days) is at most the given value.

        The maturity column may be a single integer or a range like "90‑100".
        For ranges, the lower bound is used.

        Args:
            days (int): Maximum allowed maturity days.
            bool_list (bool): If True, return a list of booleans. If False, return
                a filtered DataFrame. Defaults to True.

        Returns:
            list of bool or pd.DataFrame
        """
        lower_bounds = self.dataframe['Maturity (days)'].apply(
            lambda x: x if isinstance(x, int) else int(x.split('-')[0])
        )
        if bool_list:
            return (lower_bounds <= days).tolist()
        return self.dataframe[(lower_bounds <= days).tolist()]
    
    def is_weight(self, fweight):
        """
        Filter varieties whose weight range includes the given weight.

        The weight column may be a single integer or a range like "200‑300".
        Both lower and upper bounds are considered.

        Args:
            fweight (int or float): The target weight in grams.

        Returns:
            pd.DataFrame: Filtered DataFrame containing varieties that fall
                within the weight range.
        """
        lower_bounds = self.dataframe['Weight (g)'].apply(
            lambda x: x if isinstance(x, int) else int(x.split('-')[0])
        )
        upper_bounds = self.dataframe['Weight (g)'].apply(
            lambda x: x if isinstance(x, int) else int(x.split('-')[-1])
        )
        return self.dataframe[(np.array(lower_bounds <= fweight) & np.array(fweight <= upper_bounds)).tolist()]
    
    def is_bigger_than(self, fsize):
        """
        Filter varieties whose fruit size (lower bound) is at least the given value.

        The fruit size column may be a single integer or a range like "5‑7".
        Only the lower bound is used.

        Args:
            fsize (int or float): Minimum fruit size in cm.

        Returns:
            pd.DataFrame: Filtered DataFrame.
        """
        lower_bounds = self.dataframe['Fruit Size (cm)'].apply(
            lambda x: x if isinstance(x, int) else int(x.split('-')[0])
        )
        return self.dataframe[(lower_bounds >= fsize).tolist()]
    
    def is_size(self, fsize):
        """
        Filter varieties whose fruit size range includes the given size.

        The fruit size column may be a single integer or a range like "5‑7".
        Both lower and upper bounds are considered.

        Args:
            fsize (int or float): Target fruit size in cm.

        Returns:
            pd.DataFrame: Filtered DataFrame.
        """
        lower_bounds = self.dataframe['Fruit Size (cm)'].apply(
            lambda x: x if isinstance(x, int) else int(x.split('-')[0])
        )
        upper_bounds = self.dataframe['Fruit Size (cm)'].apply(
            lambda x: x if isinstance(x, int) else int(x.split('-')[-1])
        )
        return self.dataframe[(np.array(lower_bounds <= fsize) & np.array(fsize <= upper_bounds)).tolist()]
        
    def is_month_between(self, month_str, start_str, end_str):
        """
        Helper method to check if a month falls within a given range (with wrap‑around).

        Args:
            month_str (str): Month name (e.g., "January").
            start_str (str): Start month name.
            end_str (str): End month name.

        Returns:
            bool: True if month is between start and end (inclusive) when considering
                wrap‑around (e.g., November to February includes December, January).
        """
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
        """
        Check suitability for a specific month using an external month_table.

        The month_table must have been loaded with `set_month_table()`.

        Args:
            month_str (str): Month name.
            best (bool): If True, use the "<month> (best)" column; otherwise use
                the plain month column. Defaults to False.
            bool_list (bool): If True, return a list of booleans. If False, return
                the filtered main DataFrame. Defaults to True.

        Returns:
            list of bool or pd.DataFrame

        Note:
            If bool_list is False, the method filters `self.dataframe` using the
            boolean list derived from the month_table. This assumes the month_table
            has the same row order as the main DataFrame.
        """
        if best:
            if bool_list:
                return self.month_table[month_str+' (best)'].tolist()
            return self.dataframe[self.month_table[month_str+' (best)'].tolist()]
        if bool_list:
            return self.month_table[month_str].tolist()
        return self.dataframe[self.month_table[month_str].tolist()]
        
    def is_cultivation_time(self, month_str, bool_list=True):
        """
        Check if a given month falls within the sowing/transplanting window.

        Uses the columns 'Sowing and transplant starting time' and
        'Sowing and transplant ending time' (month names). The range can wrap around
        the year (e.g., Nov–Feb).

        Args:
            month_str (str): Month name.
            bool_list (bool): If True, return a list of booleans. If False, return
                a filtered DataFrame. Defaults to True.

        Returns:
            list of bool or pd.DataFrame
        """
        sl = self.dataframe['Sowing and transplant starting time'].tolist()
        el = self.dataframe['Sowing and transplant ending time'].tolist()
        if bool_list:
            return [self.is_month_between(month_str, s, e) for s, e in zip(sl, el)]
        return self.dataframe[[self.is_month_between(month_str, s, e) for s, e in zip(sl, el)]]
    
    def is_best_cultivation_time(self, month_str, bool_list=True):
        """
        Check if a given month falls within the *best* sowing/transplanting window.

        Uses the columns 'Best sowing and transplant starting time' and
        'Best sowing and transplant ending time'.

        Args:
            month_str (str): Month name.
            bool_list (bool): If True, return a list of booleans. If False, return
                a filtered DataFrame. Defaults to True.

        Returns:
            list of bool or pd.DataFrame
        """
        sl = self.dataframe['Best sowing and transplant starting time'].tolist()
        el = self.dataframe['Best sowing and transplant ending time'].tolist()
        if bool_list:
            return [self.is_month_between(month_str, s, e) for s, e in zip(sl, el)]
        return self.dataframe[[self.is_month_between(month_str, s, e) for s, e in zip(sl, el)]]
    
    def is_allyear(self, best=False, bool_list=True):
        """
        Determine which varieties are suitable for cultivation throughout the year.

        Args:
            best (bool): If True, use the "best" sowing windows; otherwise use the
                general windows. Defaults to False.
            bool_list (bool): If True, return a list of booleans. If False, return
                a filtered DataFrame. Defaults to True.

        Returns:
            list of bool or pd.DataFrame: For each variety, True if it is suitable
                in every month (i.e., the month range covers the whole year).
        """
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
        """
        Create and save an Excel file with month‑wise suitability booleans.

        The output file contains columns: 'Variety', each month (True/False for general
        suitability), and each month with '(best)' (True/False for best suitability).

        Args:
            filename (str): Path where the Excel file will be saved.
        """
        df = pd.DataFrame(columns=['Variety']+calendar.month_name[1:]+[month+' (best)' for month in calendar.month_name[1:]])
        df['Variety'] = self.dataframe['Variety']
        for month in calendar.month_name[1:]:
            df[month] = self.is_cultivation_time(month, bool_list=True)
            df[month+' (best)'] = self.is_best_cultivation_time(month, bool_list=True)

        df.to_excel(filename)

    def generate_list(self, crop_name='All', maturity_day='All', crop_type='All', brand_name='All', weather_tolerance='All', month='All', best=False):
        """
        Generate a boolean list of varieties that match all specified criteria.

        This is a multi‑filter method that applies several conditions sequentially.
        Each filter can be set to 'All' to ignore it.

        Args:
            crop_name (str): Crop name to match (substring). Default 'All' (no filter).
            maturity_day (str or 'All'): Maximum maturity days. If not 'All', converted
                to int and used with `is_maturity_within()`.
            crop_type (str): 'Hybrid', 'OP' (open‑pollinated), or 'All'. Default 'All'.
            brand_name (str): 'Zillion' or other. Default 'All' (no filter).
            weather_tolerance (str): 'Rain', 'Heat', 'Both', or 'All'. Default 'All'.
            month (str): Month name for cultivation time filter. Default 'All'.

        Returns:
            list of bool: A boolean list of length equal to the number of rows in
                the DataFrame, where True means the variety satisfies all given filters.
        """
        variety_list = [True] * len(self.dataframe)

        # crop
        if crop_name != 'All':
            crop_list = self.find(column='Crop', value=crop_name, bool_list=True)
            variety_list = [x and y for x, y in zip(crop_list, variety_list)]

        # maturity
        if maturity_day != 'All':
            maturity_list = self.is_maturity_within(int(maturity_day), bool_list=True)
            variety_list = [x and y for x, y in zip(maturity_list, variety_list)]

        # hybrid or OP
        if crop_type != 'All':
            type_list = self.find(column='Hybrid or OP', value=crop_type, bool_list=True)
            variety_list = [x and y for x, y in zip(type_list, variety_list)]

        # brand
        if brand_name != 'All':
            brand_list = self.find(column='Company', value=brand_name, bool_list=True)
            variety_list = [x and y for x, y in zip(brand_list, variety_list)]

        # weather tolerance
        if weather_tolerance != 'All':
            if weather_tolerance == 'Rain':
                weather_list = self.find(column='Weather tolerance', value='rain', bool_list=True)
            elif weather_tolerance == 'Heat':
                weather_list = self.find(column='Weather tolerance', value='heat', bool_list=True)
            else:
                rain_list = self.find(column='Weather tolerance', value='rain', bool_list=True)
                heat_list = self.find(column='Weather tolerance', value='heat', bool_list=True)
                weather_list = [x and y for x, y in zip(rain_list, heat_list)]
            variety_list = [x and y for x, y in zip(weather_list, variety_list)]

        # cultivation time
        if month != 'All':
            if self.month_table is not None:
                month_list = self.is_month_inlist(month, best)
            else:
                if best:
                    month_list = self.is_best_cultivation_time(month, bool_list=True)
                else:   
                    month_list = self.is_cultivation_time(month, bool_list=True)
            variety_list = [x and y for x, y in zip(month_list, variety_list)]

        return variety_list