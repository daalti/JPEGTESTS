import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 pcl using svrtest.obj
    +test_tier: 1
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework: TUF
    +external_files:svrtest.obj=a0f4b7a33be0c93ecdf9d919b0a8f22d8e071a82767e5294b95a9512abc64e15
    +test_classification:System
    +name: test_pcl5_pcl_fontdes_ftsdisk_svrtest
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PCL5
        +interaction:Headless
        +test_type:Positive
    +test:
        +title: test_pcl5_pcl_fontdes_ftsdisk_svrtest
        +guid:752a62f5-3651-49bf-9750-740b50b6ce6b
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_pcl_fontdes_ftsdisk_svrtest(setup_teardown, printjob, outputsaver):
    printjob.print_verify('a0f4b7a33be0c93ecdf9d919b0a8f22d8e071a82767e5294b95a9512abc64e15', timeout=600)
    outputsaver.save_output()
