class UsageCalculator:

    @staticmethod
    def calculate_electricity_bill(watt: float, daily_minutes: float = 30, days: int = 30):
        hours_per_day = daily_minutes / 60
        kwh_per_days = (watt * hours_per_day * days) / 1000
        average_price_per_kwh = 120
        return round(kwh_per_days * average_price_per_kwh, 2)

    @staticmethod
    def calculate_carbon_footprint(watt: float, daily_minutes: float = 30, days: int = 30):
        hours_per_day = daily_minutes / 60
        total_kwh = (watt * hours_per_day * days) / 1000
        carbon_emission_factor = 0.424
        return round(total_kwh * carbon_emission_factor, 4)

