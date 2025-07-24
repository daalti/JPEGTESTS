import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 pcl using duplx5b3.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:720
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:duplx5b3.obj=cb3d70041ca32fa8457d8cb45d253c0dc4646cd4247d9d179382c72157fc754d
    +test_classification:System
    +name: test_pcl5_pcl_duplex_duplx5b3
    +test:
        +title: test_pcl5_pcl_duplex_duplx5b3
        +guid:bd7e2c84-cd10-487d-b4fb-b5c641aa72f0
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_pcl_duplex_duplx5b3(setup_teardown, printjob, outputsaver):
    printjob.print_verify('cb3d70041ca32fa8457d8cb45d253c0dc4646cd4247d9d179382c72157fc754d', timeout=600)
    outputsaver.save_output()
