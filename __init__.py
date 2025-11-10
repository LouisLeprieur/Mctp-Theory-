"""
MCTP Theory Framework: Maximum Coherent Information Throughput
"""

from .mctp_action import MCTP_Action
from .cross_domain_validator import CrossDomainValidator
from .data_loader import DataLoader

__version__ = "1.0.0"
__author__ = "Louis Leprieur"
__email__ = "contact@mctp-theory.org"

__all__ = ["MCTP_Action", "CrossDomainValidator", "DataLoader"]
