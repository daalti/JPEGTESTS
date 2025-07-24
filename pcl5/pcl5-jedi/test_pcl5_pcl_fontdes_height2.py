import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 pcl using height2.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:height2.obj=e4bed0cb78f8e2a58da28ceb53c901c172011beb2a608c703ad4bec5a8a559a8
    +test_classification:System
    +name: test_pcl5_pcl_fontdes_height2
    +test:
        +title: test_pcl5_pcl_fontdes_height2
        +guid:e7c12fbd-a804-4984-a624-cf7d0d49e184
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_pcl_fontdes_height2(setup_teardown, printjob, outputsaver):
    printjob.print_verify('e4bed0cb78f8e2a58da28ceb53c901c172011beb2a608c703ad4bec5a8a559a8', timeout=600)
    outputsaver.save_output()
