import numpy as np
"""This is just a sample module to show the implementation."""
class Calculator:
    """This is a sample class within the sample module that gets instatiated in the app.py.
    """
    def get_value_after_saving(self, start_value: float,
                               saving_per_period: float,
                               interest_per_period: float,
                               periods: int):
        """This function calculates the value after saving for a given number of periods."""
        a = 1 + interest_per_period
        return a**periods * start_value + saving_per_period * ((1-a**periods)/(1-a))

    def get_interest_share_after_saving(self, value_after_saving: float, saving_per_period: float, periods: int):
        """This function calculates the interest share after saving."""
        return (value_after_saving - saving_per_period * periods) / value_after_saving
    
    def get_needed_takeout(self, needed_per_period: float, tax_on_interest: float, interest_share: float):
        """ Calculates the sum that needs to be removed from the portfolio given taxation on interest"""
        return needed_per_period / (1 - tax_on_interest*interest_share)
    
    def get_value_after_takeout(self, start_value: float,
                                needed_per_period: float,
                                interest_per_period: float,
                                tax_on_interest: float,
                                interest_share: float,
                                periods: int):
        """ Calculates the value after a given number of periods given taxation on interest"""
        needed_takeout = self.get_needed_takeout(needed_per_period, tax_on_interest, interest_share)
        return self.get_value_after_saving(start_value, -needed_takeout, interest_per_period, periods)
    
    def time_to_value_taking(self, start_value: float,
                        minimum_value: float,
                        needed_per_period: float,
                        interest_per_period: float,
                        tax_on_interest: float,
                        interest_share: float):
        """ Calculates the time to minimum value given taxation on interest"""
        a = 1 + interest_per_period
        needed_takeout = self.get_needed_takeout(needed_per_period, tax_on_interest, interest_share)
        const = needed_takeout / (1 - a)
        return np.log((minimum_value + const) / (start_value + const)) / np.log(a)
    
    def time_to_value_saving(self, start_value: float,
                             target_value: float,
                             saving_per_period: float,
                             interest_per_period: float):
        """ Calculates the time to target value given taxation on interest"""
        a = 1 + interest_per_period
        const = saving_per_period / (1-a)
        return np.log((target_value - const) / (start_value - const)) / np.log(a)
    
if __name__ == "__main__":
    calc = Calculator()
    print(calc.get_value_after_takeout(10000, 1000, 0.05, 0.25, 0.5, 10))
    print(calc.get_value_after_saving(start_value=10000,
                                      saving_per_period=1000,
                                      interest_per_period=0.05,
                                      periods=11))
    
    print(calc.time_to_value_taking(start_value=10000,
                               minimum_value=1000,
                               needed_per_period=1000,
                               interest_per_period=0.05,
                               tax_on_interest=0.25,
                               interest_share=0.5))
    
    print(calc.time_to_value_saving(start_value=10000,
                                    target_value=20000,
                                    saving_per_period=1000,
                                    interest_per_period=0.05))
        
