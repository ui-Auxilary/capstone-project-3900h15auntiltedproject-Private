import pandas as pd
import os
def calculate_mfi(input_file_path: str ="stock_data.csv", output_file_path:str = "mfi.csv", window_size: int =14, high_column: str = "High", low_column: str = "Low", close_column: str = "Close", value_column: str = "Volume", date_column: str = "Date"):
    
    """get csv file path, output file path and window size

    Args:
        input_file_path (str): input file path
        output_file_path (str): output file path
        window_size (num): the window size of moving average
        high_column (str): the column name of the high value column
        low_column (str): the column name of the low value column
        close_column (str): the column name of the close
        date_column (str): the colunm name of the date column in the input file
        value_column (str): the colunm name of the value column in the output file
    Returns:
        pd.DataFrame: Dataframe from the csv file
    """
    
    input_file_path = os.path.join('/backend/data/', input_file_path)
    df = pd.read_csv(input_file_path)
    df = df.sort_values(by=[date_column])
    data_type = df[value_column].dtype
    data_type_high = df[high_column].dtype
    data_type_low = df[low_column].dtype
    data_type_close = df[close_column].dtype
    if data_type == 'object':
        df[value_column] = df[value_column].str.replace(',', '').astype(float)
    if data_type_high != 'float':
        try:
            df[high_column] = df[value_column].str.replace(',', '').astype(float)
        except:
            print("high column must be the type of float")
            return
    if data_type_low != 'float':
        try:
            df[high_column] = df[value_column].str.replace(',', '').astype(float)
        except:
            print("low column must be the type of float")
            return
    if data_type_close != 'float':
        try:
            df[high_column] = df[value_column].str.replace(',', '').astype(float)
        except:
            print("close column must be the type of float")
            return
            

    # Calculate typical price
    
    df['Typical Price'] = (df[high_column] + df[low_column] + df[close_column]) / 3
    
    # Calculate Money Flow (MF)
    
    df['Money Flow'] = df['Typical Price'] * df[value_column]
    
    # Calculate Positive Money Flow (PMF) and Negative Money Flow (NMF)
    df['PMF'] = 0.0
    df['NMF'] = 0.0
    
    df.loc[df['Typical Price'] > df['Typical Price'].shift(1), 'PMF'] = df['Money Flow']
    df.loc[df['Typical Price'] < df['Typical Price'].shift(1), 'NMF'] = df['Money Flow']
    
    # Calculate Money Ratio (MR)
    df['MR'] = df['PMF'].rolling(window=window_size).sum() / df['NMF'].rolling(window=window_size).sum()
    
    # Calculate Money Flow Index (MFI)
    df['MFI'] = 100 - (100 / (1 + df['MR']))
    
    df.to_csv(output_file_path)
    return df.to_json()
