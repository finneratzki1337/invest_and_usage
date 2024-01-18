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
    
    # TODO: Get interest share after taking. Interessant da interest auf residuum entsteht 
    # Interessant, da dynamisch nach X perioden sich der interest share iterativ erhöht ... nochmal interessante Rechnung
       
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
        
        # Actually need to calculate this iteratively since the interest share changes over time
        current_value = start_value
        current_interest_share = interest_share
        non_interest_total = (1-interest_share) * current_value
        for period in range(1, periods+1):
            needed_takeout = self.get_needed_takeout(needed_per_period, tax_on_interest, current_interest_share)
            #old_value = current_value
            current_value = self.get_value_after_saving(current_value, -needed_takeout, interest_per_period, 1)
            non_interest_total -= (1-current_interest_share) * needed_takeout
            # Get new interest share
            total_interest = current_value * current_interest_share + current_value * interest_per_period
            current_interest_share = total_interest / (total_interest + non_interest_total)
        return current_value
    
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
    
    def get_hypo_interest_share(self, periods, interest_per_period):
        a = 1 + interest_per_period
        return 1 - periods / ((1-a**periods)/(1-a))
    
    def get_vx(self, minimum_value, monthly_need, using_periods, saving_periods, interest_per_period, tax_on_interest):
        interest_share = self.get_hypo_interest_share(periods = saving_periods,
                                                      interest_per_period=interest_per_period)
        actual_need = self.get_needed_takeout(needed_per_period = monthly_need,
                                              tax_on_interest=tax_on_interest,
                                              interest_share=interest_share)
        
        print(f"Hypo interest share: {interest_share}, actual need: {actual_need}")
        a = 1 + interest_per_period
        return (minimum_value + actual_need*((1-a**using_periods) / (1-a))) / a**using_periods

    
    def get_saving_rate(self, age_now, age_then, target_retirement, vmin, v0, monthly_need, interest_per_period, tax_on_interest):
        saving_periods = (target_retirement - age_now)*12
        using_periods = (age_then - target_retirement)*12
        a = 1 + interest_per_period
        vx = self.get_vx(minimum_value=vmin,
                         monthly_need=monthly_need,
                         using_periods=using_periods,
                         saving_periods=saving_periods,
                         interest_per_period=interest_per_period,
                         tax_on_interest=tax_on_interest)
        
        sr = (vx - v0 * a**saving_periods) *(1-a)/(1-a**saving_periods)

        print(f"Saving periods: {saving_periods}, using periods: {using_periods}, vx: {vx}, sr: {sr}")
        return sr
    
    # Wie viel muss ich sparen, damit ich ich in X perioden genug für Y perioden bei Z entnahme habe?

    
if __name__ == "__main__":
    calc = Calculator()
    """print(calc.get_value_after_takeout(500000,
                                       3000,
                                       (1+0.05)**(1/12)-1, 0.25, 0.6, 300))
    print(calc.get_value_after_saving(start_value=10000,
                                      saving_per_period=1000,
                                      interest_per_period=0.05,
                                      periods=11))
    
    print(calc.time_to_value_taking(start_value=10000,
                               minimum_value=1000,
                               needed_per_period=300,
                               interest_per_period=0.02,
                               tax_on_interest=0.25,
                               interest_share=0.5))
    
    print(calc.time_to_value_saving(start_value=10000,
                                    target_value=20000,
                                    saving_per_period=1000,
                                    interest_per_period=0.02))
     """   
    
    #print(calc.get_hypo_interest_share(100, 0.02))

    calc.get_saving_rate(age_now=33,
                            age_then=95,
                            target_retirement=65,
                            vmin=100000,
                            v0=10000,
                            monthly_need=1500,
                            interest_per_period=(1+0.06)**(1/12)-1,
                            tax_on_interest=0.25)
    
    
