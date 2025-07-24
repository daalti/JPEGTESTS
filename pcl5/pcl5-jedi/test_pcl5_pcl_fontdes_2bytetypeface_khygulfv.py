import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 pcl using khygulfv.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:khygulfv.obj=304e500068b9c63a191eda0e2aade5b135faa8debd7cb80c72ac07bfd2c8fa8c
    +test_classification:System
    +name: test_pcl5_pcl_fontdes_2bytetypeface_khygulfv
    +test:
        +title: test_pcl5_pcl_fontdes_2bytetypeface_khygulfv
        +guid:2b34825f-5d45-4c92-a110-94c0fc775bfa
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_pcl_fontdes_2bytetypeface_khygulfv(setup_teardown, printjob, outputsaver):
    printjob.print_verify('304e500068b9c63a191eda0e2aade5b135faa8debd7cb80c72ac07bfd2c8fa8c', timeout=600)
    outputsaver.save_output()
