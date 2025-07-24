import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 pcl using duplx5b1.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:duplx5b1.obj=de6515e52101cc24620a028c97f50b41b01afb91616161bcfa0f8b2c746f9d18
    +test_classification:System
    +name: test_pcl5_pcl_duplex_duplx5b1
    +test:
        +title: test_pcl5_pcl_duplex_duplx5b1
        +guid:3bd88ce0-65df-4fe8-84e6-577cc895317a
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_pcl_duplex_duplx5b1(setup_teardown, printjob, outputsaver):
    printjob.print_verify('de6515e52101cc24620a028c97f50b41b01afb91616161bcfa0f8b2c746f9d18', timeout=600)
    outputsaver.save_output()
