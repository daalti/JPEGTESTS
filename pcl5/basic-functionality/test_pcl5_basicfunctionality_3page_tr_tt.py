import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 basicfunctionality using 3Page_tr_tt.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:120
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:3Page-tr_tt.obj=e5ef10052d66481d7a965a8fcc2f13277ac1e06316a525d09ec6aa647b2b135e
    +test_classification:System
    +name: test_pcl5_basicfunctionality_3page_tr_tt
    +test:
        +title: test_pcl5_basicfunctionality_3page_tr_tt
        +guid:28f06c39-2c56-4bf9-a1a0-a05eccf06189
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

def test_pcl5_basicfunctionality_3page_tr_tt(setup_teardown, printjob, outputsaver):
    printjob.print_verify('e5ef10052d66481d7a965a8fcc2f13277ac1e06316a525d09ec6aa647b2b135e')
    outputsaver.save_output()
