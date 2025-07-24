import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 hpgl using lo.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:lo.obj=92952ba1fd14404c362d68765ad71c44db12b922283aaa69b731098c753d4b6a
    +test_classification:System
    +name: test_pcl5_hpgl_char_lo
    +test:
        +title: test_pcl5_hpgl_char_lo
        +guid:02bebf30-f115-4c5a-b394-2ba15884df0c
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_hpgl_char_lo(setup_teardown, printjob, outputsaver):
    printjob.print_verify('92952ba1fd14404c362d68765ad71c44db12b922283aaa69b731098c753d4b6a', timeout=600)
    outputsaver.save_output()
