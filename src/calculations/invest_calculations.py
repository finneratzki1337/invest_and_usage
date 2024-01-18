import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

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

    
    def get_saving_rate(self,
                        age_now: int,
                        age_then: int,
                        target_retirement: int,
                        vmin: float,
                        v0: float,
                        monthly_need: float,
                        interest_per_period_saving: float,
                        interest_per_period_taking: float,
                        tax_on_interest: float):
        saving_periods = (target_retirement - age_now)*12
        using_periods = (age_then - target_retirement)*12
        a_saving = 1 + interest_per_period_saving
        vx = self.get_vx(minimum_value=vmin,
                         monthly_need=monthly_need,
                         using_periods=using_periods,
                         saving_periods=saving_periods,
                         interest_per_period=interest_per_period_taking,
                         tax_on_interest=tax_on_interest)
        
        sr = (vx - v0 * a_saving**saving_periods) *(1-a_saving)/(1-a_saving**saving_periods)

        print(f"Saving periods: {saving_periods}, using periods: {using_periods}, vx: {vx}, sr: {sr}")
        return sr, vx
    
    def generate_saving_rate_dataframe(self,
                                       age_now: int,
                                       age_then: int,
                                       target_retirement: int,
                                       vmin: float,
                                       v0: float,
                                       monthly_need: float,
                                       interest_per_period_saving: float,
                                       interest_per_period_taking: float,
                                       tax_on_interest: float):
        df = pd.DataFrame()
        # Generate list of monthly needs from 1000 to 5000 with 500 increments
        monthly_needs = np.arange(1000, 5000, 500)
        # Generate retirement age range from 45 to 65 with 1 year increments
        retirement_ages = np.arange(50, 65, 1)
        for monthly_need in monthly_needs:
            for retirement_age in retirement_ages:
                saving_rate, vx = self.get_saving_rate(age_now=age_now,
                                                   age_then=95,
                                                   target_retirement=retirement_age,
                                                   vmin=vmin,
                                                   v0=v0,
                                                   monthly_need=monthly_need,
                                                   interest_per_period_saving=interest_per_period_saving,
                                                   interest_per_period_taking=interest_per_period_taking,
                                                   tax_on_interest=tax_on_interest)
                df = df._append({"monthly_need": monthly_need,
                                "retirement_age": retirement_age,
                                "saving_rate": saving_rate,
                                "max_value" : vx}, ignore_index=True)
                
        saving_interest = np.arange(0.02, 0.1, 0.02)
        taking_interest = np.arange(0.02, 0.1, 0.01)
        monthly_need = 3500
        retirement_age = 60

        df_interest = pd.DataFrame()

        for sinterest in saving_interest:
            sinterestm = (1+sinterest)**(1/12)-1
            for tinterest in taking_interest:
                tinterestm = (1+tinterest)**(1/12)-1
                saving_rate, vx = self.get_saving_rate(age_now=age_now,
                                                   age_then=95,
                                                   target_retirement=retirement_age,
                                                   vmin=vmin,
                                                   v0=v0,
                                                   monthly_need=monthly_need,
                                                   interest_per_period_saving=sinterestm,
                                                   interest_per_period_taking=tinterestm,
                                                   tax_on_interest=tax_on_interest)
                df_interest = df_interest._append({"monthly_need": monthly_need,
                                                   "saving_interest": sinterest,
                                                    "taking_interest": tinterest,
                                                    "retirement_age": retirement_age,
                                                    "saving_rate": saving_rate,
                                                    "max_value" : vx}, ignore_index=True)
                
        print(df_interest)
        # make plot with saving interest on x-axis and saving rate on y-axis and different lines for taking interest
        # Using matplotlib
        fig, ax = plt.subplots(1, 1, figsize=(10, 10))
        for taking_interest in df_interest["taking_interest"].unique():
            df_interest[df_interest["taking_interest"] == taking_interest].plot(x="saving_interest", y="saving_rate", ax=ax, label=taking_interest)
        # Add grid
        plt.grid(True)
        # Save plot
        plt.savefig("saving_rate_vs_interest.png")
        return df
    
    def draw_saving_rate_vs_age(self, df):
        # Create plot
        # Make plot with 3 subplots below each other
        fig, ax = plt.subplots(3, 1, figsize=(10, 10))
        # Make lineplot with retirement age on x-axis and saving rate on y-axis with monthly_need as separate lines
        # using matplotlib
        for monthly_need in df["monthly_need"].unique():
            df[df["monthly_need"] == monthly_need].plot(x="retirement_age", y="saving_rate", ax=ax[0], label=monthly_need)
            # Draw max_value on second plot with retirement age on x-axis and max_value on y-axis
            df[df["monthly_need"] == monthly_need].plot(x="retirement_age", y="max_value", ax=ax[1], label=monthly_need)
        # Add grid to all subplots
        for i in range(3):
            ax[i].grid(True)
        # Add grid
        plt.grid(True)
        # Make y ticks every 100
        plt.yticks(np.arange(0, 2200, 200))
        # Save plot
        plt.savefig("saving_rate_vs_age.png")
    
    # Wie viel muss ich sparen, damit ich ich in X perioden genug für Y perioden bei Z entnahme habe?

    
if __name__ == "__main__":
    calc = Calculator()
    """calc.get_saving_rate(age_now=34,
                            age_then=95,
                            target_retirement=65,
                            vmin=100000,
                            v0=60000,
                            monthly_need=4000,
                            interest_per_period_saving=(1+0.06)**(1/12)-1,
                            interest_per_period_taking=(1+0.04)**(1/12)-1,
                            tax_on_interest=0.25)"""
    
    df = calc.generate_saving_rate_dataframe(age_now=27,
                                                age_then=95,
                                                target_retirement=65,
                                                vmin=100000,
                                                v0=0,
                                                monthly_need=4000,
                                                interest_per_period_saving=(1+0.06)**(1/12)-1,
                                                interest_per_period_taking=(1+0.05)**(1/12)-1,
                                                tax_on_interest=0.25)
    
    calc.draw_saving_rate_vs_age(df)
    

