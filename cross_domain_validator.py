"""
Cross-domain validation of MCTP predictions
"""

import numpy as np
import pandas as pd
from scipy import stats
from typing import Tuple, Dict, List
import warnings

class CrossDomainValidator:
    """
    Validate MCTP predictions across quantum, neural, and cosmic domains
    """
    
    def __init__(self, random_seed: int = 42):
        self.results = {}
        np.random.seed(random_seed)
    
    def quantum_estimation(self, symmetry_scores: np.ndarray, 
                          coherence_times: np.ndarray,
                          n_bootstrap: int = 10000) -> Dict:
        """
        Estimate C_U from quantum processor data
        """
        if len(symmetry_scores) != len(coherence_times):
            raise ValueError("Symmetry scores and coherence times must have same length")
        
        # Correlation analysis
        r, p_value = stats.pearsonr(symmetry_scores, coherence_times)
        
        # Bootstrap uncertainty
        bootstrap_r = []
        n_samples = len(symmetry_scores)
        
        for _ in range(n_bootstrap):
            indices = np.random.choice(n_samples, n_samples, replace=True)
            r_bs = stats.pearsonr(symmetry_scores[indices], coherence_times[indices])[0]
            bootstrap_r.append(r_bs)
        
        r_uncertainty = np.std(bootstrap_r)
        
        # Estimate C_U from quantum enhancement (simplified relationship)
        high_symmetry = symmetry_scores > np.percentile(symmetry_scores, 70)
        low_symmetry = symmetry_scores < np.percentile(symmetry_scores, 30)
        
        if np.sum(high_symmetry) == 0 or np.sum(low_symmetry) == 0:
            warnings.warn("Insufficient samples for high/low symmetry comparison")
            enhancement = 1.0
        else:
            enhancement = (np.mean(coherence_times[high_symmetry]) / 
                          np.mean(coherence_times[low_symmetry]))
        
        # Theoretical relationship: enhancement ~ 1 + sqrt(C_U)
        C_U_estimate = (enhancement - 1)**2
        
        return {
            'C_U': C_U_estimate,
            'C_U_uncertainty': r_uncertainty * C_U_estimate,
            'correlation': r,
            'correlation_uncertainty': r_uncertainty,
            'p_value': p_value,
            'enhancement': enhancement,
            'n_samples': n_samples,
            'bootstrap_samples': n_bootstrap
        }
    
    def predict_neural_correlation(self, C_U: float, C_U_uncertainty: float) -> Tuple[float, float]:
        """
        Predict neural transfer entropy - performance correlation
        """
        # Based on MCTP theoretical relationship
        rho_predicted = 0.3 + 5.0 * C_U  # Empirical relationship from theory
        uncertainty = 5.0 * C_U_uncertainty
        
        return rho_predicted, uncertainty
    
    def predict_cosmic_correlation(self, C_U: float, C_U_uncertainty: float) -> Tuple[float, float]:
        """
        Predict cosmic coherence - sSFR correlation
        """
        # Based on MCTP theoretical relationship  
        rho_predicted = 0.25 + 4.5 * C_U  # Empirical relationship from theory
        uncertainty = 4.5 * C_U_uncertainty
        
        return rho_predicted, uncertainty
    
    def full_validation(self, quantum_data: Dict, neural_data: Dict, cosmic_data: Dict) -> Dict:
        """
        Complete cross-domain validation
        """
        # Step 1: Estimate C_U from quantum only
        quantum_result = self.quantum_estimation(
            quantum_data['symmetry_scores'],
            quantum_data['coherence_times']
        )
        
        # Step 2: Predict neural and cosmic correlations
        neural_pred = self.predict_neural_correlation(
            quantum_result['C_U'], 
            quantum_result['C_U_uncertainty']
        )
        cosmic_pred = self.predict_cosmic_correlation(
            quantum_result['C_U'],
            quantum_result['C_U_uncertainty']  
        )
        
        # Step 3: Compare with observations
        validation_results = {
            'quantum': {
                'C_U_estimated': quantum_result['C_U'],
                'C_U_uncertainty': quantum_result['C_U_uncertainty'],
                'observed_correlation': quantum_result['correlation'],
                'correlation_uncertainty': quantum_result['correlation_uncertainty'],
                'p_value': quantum_result['p_value'],
                'enhancement': quantum_result['enhancement']
            },
            'neural': {
                'predicted_correlation': neural_pred[0],
                'predicted_uncertainty': neural_pred[1], 
                'observed_correlation': neural_data['correlation'],
                'within_1sigma': abs(neural_data['correlation'] - neural_pred[0]) <= neural_pred[1]
            },
            'cosmic': {
                'predicted_correlation': cosmic_pred[0],
                'predicted_uncertainty': cosmic_pred[1],
                'observed_correlation': cosmic_data['correlation'],
                'within_1sigma': abs(cosmic_data['correlation'] - cosmic_pred[0]) <= cosmic_pred[1]
            },
            'success': (
                abs(neural_data['correlation'] - neural_pred[0]) <= neural_pred[1] and
                abs(cosmic_data['correlation'] - cosmic_pred[0]) <= cosmic_pred[1]
            )
        }
        
        self.results = validation_results
        return validation_results
    
    def generate_report(self) -> str:
        """
        Generate validation report
        """
        if not self.results:
            return "No validation results available. Run full_validation first."
        
        q = self.results['quantum']
        n = self.results['neural']
        c = self.results['cosmic']
        
        report = f"""
MCTP Cross-Domain Validation Report
==================================

Quantum Domain:
---------------
C_U Estimated: {q['C_U_estimated']:.3e} ± {q['C_U_uncertainty']:.3e}
Correlation: {q['observed_correlation']:.3f} ± {q['correlation_uncertainty']:.3f}
p-value: {q['p_value']:.3e}
Coherence Enhancement: {q['enhancement']:.2f}x

Neural Domain:
--------------
Predicted Correlation: {n['predicted_correlation']:.3f} ± {n['predicted_uncertainty']:.3f}
Observed Correlation: {n['observed_correlation']:.3f}
Within 1σ: {n['within_1sigma']}

Cosmic Domain:
--------------
Predicted Correlation: {c['predicted_correlation']:.3f} ± {c['predicted_uncertainty']:.3f}
Observed Correlation: {c['observed_correlation']:.3f}
Within 1σ: {c['within_1sigma']}

Overall Validation: {'SUCCESS' if self.results['success'] else 'FAILED'}
"""
        return report
