import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 pcl using scsfangv.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:scsfangv.obj=7f87558523fb0ab9cb03bdf7ffd8d67ac9b8eda125917be35a099dd79b96970f
    +test_classification:System
    +name: test_pcl5_pcl_fontdes_2bytetypeface_scsfangv
    +test:
        +title: test_pcl5_pcl_fontdes_2bytetypeface_scsfangv
        +guid:a43f0176-0f47-49ee-b506-008521790e3e
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_pcl_fontdes_2bytetypeface_scsfangv(setup_teardown, printjob, outputsaver):
    printjob.print_verify('7f87558523fb0ab9cb03bdf7ffd8d67ac9b8eda125917be35a099dd79b96970f', timeout=600)
    outputsaver.save_output()
