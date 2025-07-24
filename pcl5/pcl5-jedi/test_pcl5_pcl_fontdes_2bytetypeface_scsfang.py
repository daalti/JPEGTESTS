import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 pcl using scsfang.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:scsfang.obj=ccdc23daa1be92de8b67fe598eabefc21bbbb701ed8f3448339f52c0dca7eda5
    +test_classification:System
    +name: test_pcl5_pcl_fontdes_2bytetypeface_scsfang
    +test:
        +title: test_pcl5_pcl_fontdes_2bytetypeface_scsfang
        +guid:01a5ebf4-8027-4de8-ade4-2936245c13f2
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_pcl_fontdes_2bytetypeface_scsfang(setup_teardown, printjob, outputsaver):
    printjob.print_verify('ccdc23daa1be92de8b67fe598eabefc21bbbb701ed8f3448339f52c0dca7eda5', timeout=600)
    outputsaver.save_output()
