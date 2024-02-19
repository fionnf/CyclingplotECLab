import eclabfiles as ecf
import pandas as pd

"""def print_mpr_file_contents_to_txt(mpr_file_path, txt_file_path):
    df = ecf.to_df(mpr_file_path)
    pd.set_option('display.max_colwidth', 50)
    print(df)

    with open(txt_file_path, 'w') as file:
        print('Printing to txt file', file=file)
        df_string = df.to_string()
        print('string written')
        file.write(df_string)
"""

def process_mpr_data(mpr_file_path):
    df = ecf.to_df(mpr_file_path)

    # Filter rows where mode is 1 (charge) or 2 (discharge)
    df_filtered = df[df['mode'].isin([1, 2])]
    df=df_filtered

    # Assuming that the cycle number increments for each new cycle in the 'Ns' column
    df['Cycle_Number'] = df['Ns'].diff().ne(0).cumsum()

    # Assuming 'Q charge/discharge' is positive for charge and negative for discharge
    # If this is not the case, you may need to adjust the logic below
    df['Q charge/discharge'] = df['Q charge/discharge'].abs()

    # Group by 'Cycle_Number' and get the max 'Q charge/discharge' for charge capacity
    charge_capacity = df.groupby('Cycle_Number')['Q charge/discharge'].max()

    # Group by 'Cycle_Number' and get the min 'Q charge/discharge' for discharge capacity
    discharge_capacity = df.groupby('Cycle_Number')['Q charge/discharge'].max()

    # Get the last time value for each cycle, which represents the cycle duration
    time = df.groupby('Cycle_Number')['time'].max()

    # Combine all the series into a dataframe
    processed_df = pd.DataFrame({
        'Cycle_Number': charge_capacity.index,
        'Charge_Capacity': charge_capacity.values,
        'Discharge_Capacity': discharge_capacity.values,
        'Time': time.values
    })
    print(processed_df)
    return processed_df

# Replace 'path_to_your_mpr_file.mpr' with the actual path to your .mpr file
# Replace 'path_to_your_output_txt_file.txt' with the desired path for the text file output
mpr_file_path = r'C:\Users\fionn\Desktop\AkkuSpin\Test\Cyclerfolder\FF025e_cycle.mpr'
txt_file_path = r'C:\Users\fionn\Desktop\AkkuSpin\Test\Cyclerfolder\FF025e_cycle.txt'
process_mpr_data(mpr_file_path)
