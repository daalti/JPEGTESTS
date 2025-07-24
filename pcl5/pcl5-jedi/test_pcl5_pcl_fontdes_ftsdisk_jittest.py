import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 pcl using jittest.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:jittest.obj=255bc5403265ee525513cbe13d3ad1dfc8c5b41018331b8b882ebd0cbaff6f7d
    +test_classification:System
    +name: test_pcl5_pcl_fontdes_ftsdisk_jittest
    +test:
        +title: test_pcl5_pcl_fontdes_ftsdisk_jittest
        +guid:7a0fafad-6d57-42c8-878d-1fbb2b8c71fb
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_pcl_fontdes_ftsdisk_jittest(setup_teardown, printjob, outputsaver):
    printjob.print_verify('255bc5403265ee525513cbe13d3ad1dfc8c5b41018331b8b882ebd0cbaff6f7d', timeout=600)
    outputsaver.save_output()
