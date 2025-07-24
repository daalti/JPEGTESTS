import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 hpgl using sl2.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:sl2.obj=5ce6f7253c5e1f629b081247186545f236a1ae163be792b7953caee68c012961
    +test_classification:System
    +name: test_pcl5_hpgl_char_sl2
    +test:
        +title: test_pcl5_hpgl_char_sl2
        +guid:37b43a9f-c88d-48b4-8458-a29e6429f9a5
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_hpgl_char_sl2(setup_teardown, printjob, outputsaver):
    printjob.print_verify('5ce6f7253c5e1f629b081247186545f236a1ae163be792b7953caee68c012961', timeout=600)
    outputsaver.save_output()
