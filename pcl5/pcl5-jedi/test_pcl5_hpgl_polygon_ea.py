import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 hpgl using ea.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:ea.obj=7351d5429aac7a2e04fb9487c4b3b374d80ab56fee1c4f9e9d083d43ceffe494
    +test_classification:System
    +name: test_pcl5_hpgl_polygon_ea
    +test:
        +title: test_pcl5_hpgl_polygon_ea
        +guid:55895168-1dd8-427e-b978-916e6da668b7
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_hpgl_polygon_ea(setup_teardown, printjob, outputsaver):
    printjob.print_verify('7351d5429aac7a2e04fb9487c4b3b374d80ab56fee1c4f9e9d083d43ceffe494', timeout=600)
    outputsaver.save_output()
