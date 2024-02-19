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
    discharge_capacity = df[(df['mode'] == 1) & (df['ox/red'] == 0)].groupby('Full_Cycle_Number')['Abs_Q_charge_discharge'].min().abs()
    coulombic_efficiency = (discharge_capacity / charge_capacity) * 100

    time = df.groupby('Full_Cycle_Number')['time'].max()

    last_uts = df.groupby('Full_Cycle_Number')['uts'].last()

    cycle_numbers = charge_capacity.index.union(discharge_capacity.index)
    processed_df = pd.DataFrame({
        'Cycle_Number': cycle_numbers,
        'Charge_Capacity': charge_capacity.reindex(cycle_numbers, fill_value=0),
        'Discharge_Capacity': discharge_capacity.reindex(cycle_numbers, fill_value=0),
        'Coulombic Efficiency': coulombic_efficiency.reindex(cycle_numbers, fill_value=0),
        'Time': time.reindex(cycle_numbers, fill_value=0),
        'Last_UTS': last_uts.reindex(cycle_numbers, fill_value=0)
    })

    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', None)
    print(processed_df)
    return processed_df


mpr_file_path = r'C:\Users\fionn\Desktop\AkkuSpin\Test\Cyclerfolder\FF025e_cycle.mpr'
process_mpr_data(mpr_file_path)
