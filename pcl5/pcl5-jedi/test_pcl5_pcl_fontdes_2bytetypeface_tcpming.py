import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 pcl using tcpming.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:tcpming.obj=7baeacc8b66ab0c14660ba752a872654b8c59cb2beb7b088de932ec6cbc89ed2
    +test_classification:System
    +name: test_pcl5_pcl_fontdes_2bytetypeface_tcpming
    +test:
        +title: test_pcl5_pcl_fontdes_2bytetypeface_tcpming
        +guid:a0d6300b-4539-4262-b708-7b3110b15453
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_pcl_fontdes_2bytetypeface_tcpming(setup_teardown, printjob, outputsaver):
    printjob.print_verify('7baeacc8b66ab0c14660ba752a872654b8c59cb2beb7b088de932ec6cbc89ed2', timeout=600)
    outputsaver.save_output()
