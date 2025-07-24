import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 pcl using jpminchy.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:jpminchy.obj=d684d33a974576c22bf9c6dd9367ca755f7b88a42b96f5481c3304b1d0b260c8
    +test_classification:System
    +name: test_pcl5_pcl_fontdes_2bytetypeface_jpminchy
    +test:
        +title: test_pcl5_pcl_fontdes_2bytetypeface_jpminchy
        +guid:ade465a5-b3aa-4dc7-9807-e29870ff0d2a
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_pcl_fontdes_2bytetypeface_jpminchy(setup_teardown, printjob, outputsaver):
    printjob.print_verify('d684d33a974576c22bf9c6dd9367ca755f7b88a42b96f5481c3304b1d0b260c8', timeout=600)
    outputsaver.save_output()
