import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 pcl using tcpmingy.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:tcpmingy.obj=f0a14bad3523cf5e87f530a41d2bd3256d8245270736da1d74332057d09d9c46
    +test_classification:System
    +name: test_pcl5_pcl_fontdes_2bytetypeface_tcpmingy
    +test:
        +title: test_pcl5_pcl_fontdes_2bytetypeface_tcpmingy
        +guid:85a46fed-5263-4e1e-8885-46324ace6ad8
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_pcl_fontdes_2bytetypeface_tcpmingy(setup_teardown, printjob, outputsaver):
    printjob.print_verify('f0a14bad3523cf5e87f530a41d2bd3256d8245270736da1d74332057d09d9c46', timeout=600)
    outputsaver.save_output()
