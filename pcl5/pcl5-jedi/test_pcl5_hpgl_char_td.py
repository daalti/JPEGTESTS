import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 hpgl using td.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:td.obj=aeea9a6db2680ef0553bb71c2e0d5ef3a999936d93a28973a403553ddd393e5a
    +test_classification:System
    +name: test_pcl5_hpgl_char_td
    +test:
        +title: test_pcl5_hpgl_char_td
        +guid:c95685ec-1735-43d8-bc7b-499d59977505
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_hpgl_char_td(setup_teardown, printjob, outputsaver):
    printjob.print_verify('aeea9a6db2680ef0553bb71c2e0d5ef3a999936d93a28973a403553ddd393e5a', timeout=600)
    outputsaver.save_output()
