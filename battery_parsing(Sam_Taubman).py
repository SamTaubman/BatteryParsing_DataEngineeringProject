import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

class DimensionException(Exception):
    def __init__(self, message = "Invalid Input Dimensions."):
        super().__init__(message)

class Battery_Cycle_MaxCapacity:

    def __init__(self, data_path, skip_rows):
        self.data_path = data_path
        self.skip_rows = skip_rows
        self.battery_cycle_data = pd.DataFrame()
        self.column_names = ['mode', 'ox/red', 'error', 'control changes', 'Ns changes', 'counter inc.', 'Ns', 'time/s', 'dq/mA.h',
    '(Q-Qo)/mA.h', 'control/V/mA', 'Ecell/V', 'Q charge/discharge/mA.h', 'half cycle', '<I>/mA', 'x', 'cycle number',
    'Q charge/mA.h', 'Q discharge/mA.h', 'Energy/W.h', 'Energy charge/W.h', 'Energy discharge/W.h', 'cycle time/s',
    'step time/s', 'charge time/s', 'discharge time/s', 'd(Q-Qo)/dE/mA.h/V', 'Capacity/mA.h', 'Efficiency/%',
    'control/V', 'control/mA', 'P/W']

    def Parse_BatteryCycle_Data(self):
        '''Read the input data file into a data frame, returns the data frame and information about the dataframe.'''
        self.battery_cycle_data = pd.read_csv(self.data_path, sep='\t', header=None, skiprows=self.skip_rows, names=self.column_names)
        pd.set_option('display.max_columns', None)
        pd.set_option('display.max_rows', None)

        print(self.battery_cycle_data.info(), self.battery_cycle_data.describe(), self.battery_cycle_data.shape, 
              self.battery_cycle_data.isna().any(), self.battery_cycle_data.duplicated().any())
        return self.battery_cycle_data

    def Create_MaxCapacity_Table(self, number_of_rows):
        '''Takes battery_cycle_data data frame and number_of_rows and returns a new data frame with cycle number, Max Charge, and Max Discharge as columns. 
        Data must be parsed before using this function.'''
        charge_column = 'Q charge/mA.h'
        discharge_column = 'Q discharge/mA.h'
        max_charge = self.battery_cycle_data.groupby('cycle number')[charge_column].max()
        max_discharge = self.battery_cycle_data.groupby('cycle number')[discharge_column].max()

        maxChargeDischarge_df = pd.DataFrame({'cycle number': max_charge.index, 'Max Charge': max_charge.values, 
                                              'Max Discharge': max_discharge.values})
        return maxChargeDischarge_df.head(number_of_rows)

    def Create_MaxCapacity_Plot(self, x_axis_title, y_axis_title, plot_title):
        '''Takes battery_cycle_data data frame, x_axis_title, y_axis_title, and plot_title and returns a plot with Cycle Number on x-axis and Max Capacity on y-axis. 
        Data must be parsed before using this function.'''
        charge_column = 'Q charge/mA.h'
        discharge_column = 'Q discharge/mA.h'

        max_charge = self.battery_cycle_data.groupby('cycle number')[charge_column].max()
        max_discharge = self.battery_cycle_data.groupby('cycle number')[discharge_column].max()

        plt.figure(figsize=(10, 6))
        plt.plot(max_charge.index, max_charge.values, label='Max Charge Capacity', color='blue')
        plt.plot(max_discharge.index, max_discharge.values, label='Max Discharge Capacity', color='red')

        plt.xlabel(x_axis_title)
        plt.ylabel(y_axis_title)
        plt.title(plot_title)

        x_axis_cycles = np.arange(1, 302, 15)
        plt.xticks(x_axis_cycles)
        y_axis_capacity = np.arange(0, 200, 20)
        plt.yticks(y_axis_capacity)

        plt.xlim(0, max_charge.index.max() + 1)
        plt.ylim(0, 180)

        for capacity in y_axis_capacity:
            plt.axhline(y=capacity, color='gray', linestyle='--', alpha=0.5)

        plt.legend()

        return plt.show()
    

data_path = ""

battery_cycle_data = Battery_Cycle_MaxCapacity(data_path, 74)
battery_cycle_data.Parse_BatteryCycle_Data()

table = battery_cycle_data.Create_MaxCapacity_Table(11)
print(table)

plot = battery_cycle_data.Create_MaxCapacity_Plot('Cycle Number', 'Capacity (mA.h)', 'Max Charge and Max Discharge Capacities for Cycle Number')
print(plot)

