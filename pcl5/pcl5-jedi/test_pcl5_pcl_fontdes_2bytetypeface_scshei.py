import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 pcl using scshei.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:scshei.obj=b40642733d1c66abd8fc8cec8edbf2357612c4458320f70f44109fa203a89086
    +test_classification:System
    +name: test_pcl5_pcl_fontdes_2bytetypeface_scshei
    +test:
        +title: test_pcl5_pcl_fontdes_2bytetypeface_scshei
        +guid:5d44ff8e-80e8-48dc-91f8-94f60b1e10d6
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_pcl_fontdes_2bytetypeface_scshei(setup_teardown, printjob, outputsaver):
    printjob.print_verify('b40642733d1c66abd8fc8cec8edbf2357612c4458320f70f44109fa203a89086', timeout=600)
    outputsaver.save_output()
