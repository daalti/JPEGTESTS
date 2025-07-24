import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 highvalue using 15Page_sl_tt.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:180
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:15Page-sl_tt.obj=1cc608ba4a94c1ac6368925201cf4a8703575c30606000466e7f9392a682105a
    +test_classification:System
    +name: test_pcl5_highvalue_15page_sl_tt
    +test:
        +title: test_pcl5_highvalue_15page_sl_tt
        +guid:56165820-4a5f-4e69-8cfa-23505ac8900d
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator


$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_highvalue_15page_sl_tt(setup_teardown, printjob, outputsaver):
    printjob.print_verify('1cc608ba4a94c1ac6368925201cf4a8703575c30606000466e7f9392a682105a',timeout=300)
    outputsaver.save_output()
