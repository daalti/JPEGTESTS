import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 pcl using scssun.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:scssun.obj=55ae56ee185c1ec5b3c43411db036021a90116963a1ffe8d60541027097abb66
    +test_classification:System
    +name: test_pcl5_pcl_fontdes_2bytetypeface_scssun
    +test:
        +title: test_pcl5_pcl_fontdes_2bytetypeface_scssun
        +guid:673d9da1-7563-438d-b1c3-f7265953ff04
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_pcl_fontdes_2bytetypeface_scssun(setup_teardown, printjob, outputsaver):
    printjob.print_verify('55ae56ee185c1ec5b3c43411db036021a90116963a1ffe8d60541027097abb66', timeout=600)
    outputsaver.save_output()
