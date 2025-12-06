import csv

# --- 1. Data Loading (from user's previous code) ---
ages = []
sexes = []
bmis = []
children = []
smokers = []
regions = []
charges = []
filename = "insurance.csv"

# Open and read the CSV file once using DictReader
with open(filename, newline="") as file:
    reader = csv.DictReader(file)

    for row in reader:
        # Append data to lists, converting to appropriate types
        try:
            ages.append(int(row["age"]))
            sexes.append(row["sex"])
            bmis.append(float(row["bmi"]))
            children.append(int(row["children"]))
            smokers.append(row["smoker"])
            regions.append(row["region"])
            charges.append(float(row["charges"]))
        except ValueError:
            # Simple error handling for robustness
            continue

# --- 2. Class Definition for Analysis ---

class InsuranceDataAnalyzer:
    """
    Analyzes insurance data using only basic Python functionality.
    """
    def __init__(self, ages, sexes, bmis, children, smokers, regions, charges):
        # Store all feature lists as instance attributes
        self.ages = ages
        self.sexes = sexes
        self.bmis = bmis
        self.children = children
        self.smokers = smokers
        self.regions = regions
        self.charges = charges

    def _calculate_mean(self, data_list):
        """Helper function to calculate the mean of a list."""
        if not data_list:
            return 0
        return sum(data_list) / len(data_list)

    def analyze_descriptive_stats(self):
        """Calculates and prints descriptive statistics for numerical columns."""
        print("--- 1. Descriptive Statistics ---")
        
        # Age
        min_age = min(self.ages)
        max_age = max(self.ages)
        mean_age = self._calculate_mean(self.ages)
        print(f"Average Age: {mean_age:.1f} years (Range: {min_age}-{max_age})")
        
        # BMI
        min_bmi = min(self.bmis)
        max_bmi = max(self.bmis)
        mean_bmi = self._calculate_mean(self.bmis)
        print(f"Average BMI: {mean_bmi:.1f} (Range: {min_bmi:.1f}-{max_bmi:.1f})")

        # Charges
        min_charge = min(self.charges)
        max_charge = max(self.charges)
        mean_charge = self._calculate_mean(self.charges)
        print(f"Average Charge: ${mean_charge:,.2f} (Range: ${min_charge:,.2f}-${max_charge:,.2f})")
        
        print("-" * 35)

    def analyze_categorical_impact(self, category_list, charges_list, category_name):
        """Generic method to calculate mean charge per unique category."""
        
        # 1. Group charges by category
        category_charges = {}
        for category, charge in zip(category_list, charges_list):
            if category not in category_charges:
                category_charges[category] = []
            category_charges[category].append(charge)
        
        # 2. Calculate mean for each group
        mean_charges_by_category = {}
        for category, charges in category_charges.items():
            mean_charges_by_category[category] = self._calculate_mean(charges)
            
        return mean_charges_by_category
    
    def analyze_key_impacts(self):
        """Analyzes the impact of smoker status, sex, and region."""
        
        print("--- 2. Impact of Smoker Status ---")
        smoker_means = self.analyze_categorical_impact(self.smokers, self.charges, "smoker")
        
        # Print Smoker Impact
        if 'yes' in smoker_means and 'no' in smoker_means:
            mean_smoker = smoker_means['yes']
            mean_non_smoker = smoker_means['no']
            increase = (mean_smoker / mean_non_smoker) * 100 - 100
            print(f"Smokers Average: ${mean_smoker:,.2f}")
            print(f"Non-Smokers Average: ${mean_non_smoker:,.2f}")
            print(f"Smokers pay {increase:,.0f}% more on average.")
        print("-" * 35)
        
        print("--- 3. Impact of Region ---")
        region_means = self.analyze_categorical_impact(self.regions, self.charges, "region")
        
        # Print Regional Impact
        print("Average Charges by Region:")
        # Sort and print
        sorted_regions = sorted(region_means.items(), key=lambda item: item[1], reverse=True)
        for region, mean_charge in sorted_regions:
             print(f"- {region.capitalize()}: ${mean_charge:,.2f}")
             
        print("-" * 35)
        
        print("--- 4. Impact of Family Size (Children) ---")
        # Convert children counts to strings for categorical grouping
        children_str = [str(c) for c in self.children]
        children_means = self.analyze_categorical_impact(children_str, self.charges, "children")
        
        # Print Children Impact
        print("Average Charges by Number of Children:")
        # Sort by number of children (key)
        sorted_children = sorted(children_means.items(), key=lambda item: int(item[0]))
        for children_count, mean_charge in sorted_children:
             print(f"- {children_count} Children: ${mean_charge:,.2f}")
             
        print("-" * 35)
        
# --- 3. Execute Analysis ---
analyzer = InsuranceDataAnalyzer(ages, sexes, bmis, children, smokers, regions, charges)
analyzer.analyze_descriptive_stats()
analyzer.analyze_key_impacts()