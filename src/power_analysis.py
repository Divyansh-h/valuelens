import numpy as np
import sys
from statsmodels.stats.power import NormalIndPower
from statsmodels.stats.proportion import proportion_effectsize

def run_power_analysis():
    try:
        print("--- ValueLens: A/B Test Statistical Power Analysis ---")
        
        # Assumption: The organic, baseline reactivation rate of "Lost/At-Risk" customers is ~5% over a 60-day period.
        baseline_rate = 0.05
        
        # We define a "meaningful lift" as a 5 percentage point absolute increase (i.e. increasing from 5% to 10% reactivation)
        target_rate = 0.10
        
        print(f"Baseline Reactivation Rate: {baseline_rate*100:.1f}%")
        print(f"Target Reactivation Rate (with Campaign Lift): {target_rate*100:.1f}%")
        
        # Calculate Cohen's h (effect size for two proportions)
        effect_size = proportion_effectsize(target_rate, baseline_rate)
        print(f"\nCalculated Cohen's h Effect Size: {effect_size:.4f}")
        
        # Set parameters for power analysis
        alpha = 0.05  # Standard 95% confidence level
        power = 0.80  # Standard 80% statistical power
        
        # We are running an A/B test comparing independent proportions
        # We'll calculate the required sample size PER GROUP assuming an even 50/50 split initially
        power_analysis = NormalIndPower()
        
        sample_size_per_group = power_analysis.solve_power(
            effect_size=effect_size,
            nobs1=None,
            alpha=alpha,
            power=power,
            ratio=1.0 # 1.0 means sample size is equal between Treatment and Control (50/50 split)
        )
        
        sample_size_per_group = int(np.ceil(sample_size_per_group))
        total_sample_size = sample_size_per_group * 2
        
        print("\n[Sample Size Requirements (50/50 Split)]")
        print(f"Required Sample Size PER GROUP: {sample_size_per_group}")
        print(f"Total Required Audience Size: {total_sample_size}")
        
        # Let's also check for an 80/20 split as proposed in our strategy document
        # ratio = nobs2/nobs1 = Control/Treatment = 20/80 = 0.25
        ratio_80_20 = 0.25
        sample_size_treatment_8020 = power_analysis.solve_power(
            effect_size=effect_size,
            nobs1=None,
            alpha=alpha,
            power=power,
            ratio=ratio_80_20
        )
        
        treatment_n = int(np.ceil(sample_size_treatment_8020))
        control_n = int(np.ceil(treatment_n * ratio_80_20))
        total_8020 = treatment_n + control_n
        
        print("\n[Sample Size Requirements (80/20 Split)]")
        print(f"Required Treatment Audience (80%): {treatment_n}")
        print(f"Required Control Audience (20%): {control_n}")
        print(f"Total Required Audience Size: {total_8020}")
        
        # Analyze feasibility based on our "Hidden Gems" segment
        hidden_gems_available = 720
        
        print("\n[Feasibility Analysis]")
        print(f"We have {hidden_gems_available} 'Hidden Gem' customers available to target.")
        if hidden_gems_available >= total_8020:
            print("Verdict: HIGHLY FEASIBLE. We have enough 'Hidden Gem' customers to detect a 5% absolute lift with an 80/20 split!")
        elif hidden_gems_available >= total_sample_size:
            print("Verdict: PARTIALLY FEASIBLE. We do not have enough customers for an 80/20 split, but we can detect the lift if we switch to a 50/50 split.")
        else:
            print(f"Verdict: INFEASIBLE. We are short {total_sample_size - hidden_gems_available} customers. A 5% absolute lift will NOT be statistically significant at 80% power on this cohort size. We need to either lower our power threshold or target a broader audience.")
            
    except Exception as e:
        print(f"\n[ERROR] Failed to run power analysis: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    run_power_analysis()
