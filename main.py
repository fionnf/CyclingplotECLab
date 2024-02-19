import eclabfiles as ecf
import pandas as pd

def process_mpr_data(mpr_file_path):
    df = ecf.to_df(mpr_file_path)

    # Convert 'Q charge/discharge' values to absolute values
    df['Abs_Q_charge_discharge'] = df['Q charge/discharge']

    # Map half cycles to full cycle numbers, ensuring half cycles 0 and 1 are mapped to full cycle 1
    df['Full_Cycle_Number'] = ((df['half cycle'] // 2) + 1).astype(int)

    # Calculate charge and discharge capacities
    charge_capacity = df[(df['mode'] == 1) & (df['ox/red'] == 1)].groupby('Full_Cycle_Number')['Abs_Q_charge_discharge'].max()
    discharge_capacity = df[(df['mode'] == 1) & (df['ox/red'] == 0)].groupby('Full_Cycle_Number')['Abs_Q_charge_discharge'].min()
    discharge_capacity = abs(discharge_capacity)
    coulombic_

    # Calculate time at the end of each full cycle, aligning with your requirement
    # Assuming the maximum 'time' value of the last half cycle of each full cycle represents its end time
    time = df.groupby('Full_Cycle_Number')['time'].max()

    # Create a DataFrame to hold the computed values
    # Ensure all series are aligned by reindexing based on the union of charge and discharge cycle numbers
    cycle_numbers = charge_capacity.index.union(discharge_capacity.index)
    processed_df = pd.DataFrame({
        'Cycle_Number': cycle_numbers,
        'Charge_Capacity': charge_capacity.reindex(cycle_numbers, fill_value=0).values,
        'Discharge_Capacity': discharge_capacity.reindex(cycle_numbers, fill_value=0).values,
        'Time': time.reindex(cycle_numbers).values
    })

    print(processed_df)
    return processed_df


# Replace 'path_to_your_mpr_file.mpr' with the actual path to your .mpr file
# Replace 'path_to_your_output_txt_file.txt' with the desired path for the text file output
mpr_file_path = r'C:\Users\fionn\Desktop\AkkuSpin\Test\Cyclerfolder\FF025e_cycle.mpr'
txt_file_path = r'C:\Users\fionn\Desktop\AkkuSpin\Test\Cyclerfolder\FF025e_cycle.txt'
process_mpr_data(mpr_file_path)
