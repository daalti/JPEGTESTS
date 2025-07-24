import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 highvalue using 100Page_lsg39968.obj
    +test_tier: 1
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:1500
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework: TUF
    +external_files:100Page-lsg39968.obj=3161e3bf766f662d9b33d4f31f0b8e119137aface140fd89ecec4cf71eed70eb
    +test_classification:System
    +name: test_pcl5_highvalue_100page_lsg39968
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PCL5
        +interaction:Headless
        +test_type:Positive
    +test:
        +title: test_pcl5_highvalue_100page_lsg39968
        +guid:500d4ba8-8dac-437d-82c9-44df95b3dfa9
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_highvalue_100page_lsg39968(setup_teardown, printjob, outputsaver,tray):
    default = tray.get_default_source()
    if tray.is_size_supported('iso_a4_210x297mm', default):
        tray.configure_tray(default, 'iso_a4_210x297mm','stationery')
    printjob.print_verify('3161e3bf766f662d9b33d4f31f0b8e119137aface140fd89ecec4cf71eed70eb', timeout=1500)
    outputsaver.save_output()
