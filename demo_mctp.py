#!/usr/bin/env python3
"""
MCTP Framework Demo - Test the complete system
"""

from mctp_theory import MCTP_Action, CrossDomainValidator, DataLoader

def main():
    print("🧪 MCTP Framework - Complete Test")
    print("=================================")
    
    # Initialize all components
    mctp = MCTP_Action()
    validator = CrossDomainValidator()
    data_loader = DataLoader()
    
    print("✓ Components loaded successfully")
    
    # Load data from all domains
    quantum_data = data_loader.load_quantum_data()
    neural_data = data_loader.load_neural_data()
    cosmic_data = data_loader.load_cosmic_data()
    
    print(f"📊 Quantum: {quantum_data['n_processors']} processors")
    print(f"🧠 Neural correlation: {neural_data['correlation']:.3f}")
    print(f"🌌 Cosmic correlation: {cosmic_data['correlation']:.3f}")
    
    # Run the core validation - this tests your entire theory!
    print("\n🔬 Running cross-domain validation...")
    results = validator.full_validation(quantum_data, neural_data, cosmic_data)
    
    # Show the scientific report
    report = validator.generate_report()
    print(report)
    
    # Show coherence scale predictions
    print("\n📏 Coherence Scale Predictions:")
    for domain in ['quantum', 'neural', 'cosmic']:
        constants = mctp.domain_specific_constants(domain)
        scale = mctp.predict_coherence_scale(constants['E_b'])
        print(f"   {domain.capitalize()}: {scale:.2e} m")
    
    print("\n🎯 MCTP Framework Test Complete!")

if __name__ == "__main__":
    main()
