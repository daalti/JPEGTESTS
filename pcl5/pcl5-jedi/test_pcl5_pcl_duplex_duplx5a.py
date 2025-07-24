import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 pcl using duplx5a.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:duplx5a.obj=9fbfe048f4a6fdfc5547471e0d0757bc945dc41ae4d5f192e4692f9a5a947b61
    +test_classification:System
    +name: test_pcl5_pcl_duplex_duplx5a
    +test:
        +title: test_pcl5_pcl_duplex_duplx5a
        +guid:6edc4fb8-f6bf-4500-8dc4-21e5bb3a378c
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_pcl_duplex_duplx5a(setup_teardown, printjob, outputsaver):
    printjob.print_verify('9fbfe048f4a6fdfc5547471e0d0757bc945dc41ae4d5f192e4692f9a5a947b61', timeout=600)
    outputsaver.save_output()
