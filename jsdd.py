"""
jsdd.py - Data manager for plant disease records.

This module provides the `jsdd` class, which encapsulates a pandas DataFrame
and offers filtering capabilities based on crop, cause, affected part, status,
and rating. It is designed to be used with the `dviewer` GUI application.
"""

import pandas as pd

class jsdd():
    """
    A data manager for disease records stored in a pandas DataFrame.

    The class supports loading data from an Excel file or a pandas DataFrame,
    and provides a method to generate a boolean mask based on multiple filter
    criteria. The underlying data is expected to have columns:
        'Crop', 'Cause', 'Part affected', 'Status', 'Rating'

    Attributes:
        name (str or None): The source file name if loaded from a file.
        dataframe (pd.DataFrame): The internal data store. Missing values are
            filled with empty strings.
    """

    def __init__(self, source=None):
        """
        Initialize the jsdd instance with optional data.

        Args:
            source (str or pd.DataFrame, optional): If a string, it is treated
                as a file path to an Excel file (read via pd.read_excel). If a
                DataFrame, it is used directly. If None, the instance is empty.
                Defaults to None.
        """
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
        """
        Load or replace the internal DataFrame with new data.

        This method can be called after initialization to set or update the data.
        It handles both file paths and existing DataFrames.

        Args:
            source (str or pd.DataFrame): If a string, it is treated as a file
                path to an Excel file. Otherwise, it is expected to be a
                pandas DataFrame.

        Note:
            The method currently uses `pd.read_excel` for string inputs, so it
            does not support CSV files directly. For CSV, you would need to pass
            a pre-loaded DataFrame.
        """
        if isinstance(source, str):
            self.name = source
            self.dataframe = pd.read_excel(self.name)
        else:
            self.dataframe = pd.DataFrame(source)
            
        self.dataframe.fillna('', inplace=True)

    def find(self, column, value, bool_list=True):
        """
        Find rows where the specified column contains a given substring.

        The search is case-sensitive and uses `str.contains`. The result can be
        returned as a boolean list or as a filtered DataFrame.

        Args:
            column (str): The name of the column to search in.
            value (str): The substring to search for.
            bool_list (bool, optional): If True, return a list of booleans
                indicating which rows match. If False, return a filtered
                DataFrame containing only the matching rows, sorted by index.
                Defaults to True.

        Returns:
            list of bool or pd.DataFrame: Depending on `bool_list`.
        """
        if bool_list:
            return self.dataframe[column].str.contains(value).tolist()
        return self.dataframe[self.dataframe[column].str.contains(value)].sort_index()

    def generate_list(self, crop_name='All', cause='All', part_affected='All', status='All', rating='All'):
        """
        Generate a boolean mask for filtering rows based on multiple criteria.

        Each filter is applied as a substring match on the corresponding column.
        The method starts with a list of `True` values (all rows included) and
        progressively ANDs with the result of each active filter. Only filters
        not set to 'All' are applied.

        Args:
            crop_name (str, optional): Filter for the 'Crop' column.
                Defaults to 'All' (no filter).
            cause (str, optional): Filter for the 'Cause' column.
                Defaults to 'All'.
            part_affected (str, optional): Filter for the 'Part affected' column.
                Defaults to 'All'.
            status (str, optional): Filter for the 'Status' column.
                Defaults to 'All'.
            rating (str, optional): Filter for the 'Rating' column.
                Defaults to 'All'.

        Returns:
            list of bool: A boolean mask of length equal to the number of rows
                in `self.dataframe`, where `True` indicates the row matches all
                active filters.
        """
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