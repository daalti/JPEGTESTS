import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 pcl using duplx5b2.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:1020
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:duplx5b2.obj=d0fabfe926e944b7532b5b14cfdf994e95b35ed4ff6ed4bcc10518c0b4e04444
    +test_classification:System
    +name: test_pcl5_pcl_duplex_duplx5b2
    +test:
        +title: test_pcl5_pcl_duplex_duplx5b2
        +guid:d51189e1-20c4-400d-9e12-4be8a9c343db
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_pcl_duplex_duplx5b2(setup_teardown, printjob, outputsaver):
    printjob.print_verify('d0fabfe926e944b7532b5b14cfdf994e95b35ed4ff6ed4bcc10518c0b4e04444', timeout=900)
    outputsaver.save_output()
