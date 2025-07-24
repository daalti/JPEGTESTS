import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 highvalue using 181Page_macros.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:3600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:181Page-macros.obj=d0f6d9288281e997e7938f6a5fd077ffa195e878771d8b9430478099417af039
    +test_classification:System
    +name: test_pcl5_highvalue_181page_macros
    +test:
        +title: test_pcl5_highvalue_181page_macros
        +guid:85586149-678f-41ad-afef-a8865199e2c2
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:3600
            +test:
                +dut:
                    +type:Emulator


$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_highvalue_181page_macros(setup_teardown, printjob, outputsaver):
    printjob.print_verify('d0f6d9288281e997e7938f6a5fd077ffa195e878771d8b9430478099417af039',timeout=3600)
    outputsaver.save_output()
