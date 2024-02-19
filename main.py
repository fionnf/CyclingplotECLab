import eclabfiles as ecf
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

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


def plot_capacities_and_efficiency(mpr_file_path):
    processed_df = process_mpr_data(mpr_file_path)

    # Convert the 'Last_UTS' Unix timestamp to datetime
    processed_df['Time_Days'] = (pd.to_datetime(processed_df['Last_UTS'], unit='s') - pd.to_datetime(
        processed_df['Last_UTS'].iloc[0], unit='s')).dt.total_seconds() / (24 * 3600)

    # Create subplots: one y-axis for capacities, another for Coulombic Efficiency
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    # Plot Charge and Discharge Capacities
    fig.add_trace(go.Scatter(x=processed_df['Cycle_Number'], y=processed_df['Charge_Capacity'], mode='markers',
                             name='Charge Capacity', marker=dict(color='blue')), secondary_y=False)
    fig.add_trace(go.Scatter(x=processed_df['Cycle_Number'], y=processed_df['Discharge_Capacity'], mode='markers',
                             name='Discharge Capacity', marker=dict(color='red')), secondary_y=False)

    # Plot Coulombic Efficiency on secondary y-axis
    fig.add_trace(
        go.Scatter(x=processed_df['Cycle_Number'], y=processed_df['Coulombic Efficiency'], mode='markers',
                   name='Coulombic Efficiency', marker=dict(color='green')), secondary_y=True)

    # Set x-axis title
    fig.update_xaxes(title_text="Cycle Number",tickfont=dict(size=16))

    # Set y-axes titles
    fig.update_yaxes(title_text="Capacity (mAh)", secondary_y=False, tickfont=dict(size=16))
    fig.update_yaxes(title_text="Coulombic Efficiency (%)", secondary_y=True, tickfont=dict(size=16))

    fig.show()


mpr_file_path = r'C:\Users\fionn\Desktop\AkkuSpin\Test\Cyclerfolder\FF025e_cycle.mpr'
plot_capacities_and_efficiency(mpr_file_path)
