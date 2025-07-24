import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 highvalue using 5Page_si_tt.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:5Page-si_tt.obj=8ef50169e35d8d236710a55262cb3afc09e621d9067b4bff33c77b6cbfb1c3df
    +test_classification:System
    +name: test_pcl5_highvalue_5page_si_tt
    +test:
        +title: test_pcl5_highvalue_5page_si_tt
        +guid:70338023-c841-43f8-8c61-1f96ab424f57
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

def test_pcl5_highvalue_5page_si_tt(setup_teardown, printjob, outputsaver):
    printjob.print_verify('8ef50169e35d8d236710a55262cb3afc09e621d9067b4bff33c77b6cbfb1c3df', timeout=600)
    outputsaver.save_output()
