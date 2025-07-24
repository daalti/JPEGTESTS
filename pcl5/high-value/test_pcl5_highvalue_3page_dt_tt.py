import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 highvalue using 3Page_dt_tt.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:3Page-dt_tt.obj=b125d27c9591801d9e56cccfc0de15bc2b9d62f8d6ffc97d5efd50fdea1aee1d
    +test_classification:System
    +name: test_pcl5_highvalue_3page_dt_tt
    +test:
        +title: test_pcl5_highvalue_3page_dt_tt
        +guid:7a3d7b8a-a49b-4e75-a36d-f499aa5c0b7e
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

def test_pcl5_highvalue_3page_dt_tt(setup_teardown, printjob, outputsaver):
    printjob.print_verify('b125d27c9591801d9e56cccfc0de15bc2b9d62f8d6ffc97d5efd50fdea1aee1d', timeout=600)
    outputsaver.save_output()
