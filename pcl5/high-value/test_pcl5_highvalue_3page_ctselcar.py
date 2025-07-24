import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 highvalue using 3Page_ctselcar.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:3Page-ctselcar.obj=1fe814ebb92d5a08f0f395cb4b7b64aad6a8283c918a7b848dbf58ed3c2e21de
    +test_classification:System
    +name: test_pcl5_highvalue_3page_ctselcar
    +test:
        +title: test_pcl5_highvalue_3page_ctselcar
        +guid:28f017e1-3a6f-41e3-a29f-ae5624e3b122
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

def test_pcl5_highvalue_3page_ctselcar(setup_teardown, printjob, outputsaver):
    printjob.print_verify('1fe814ebb92d5a08f0f395cb4b7b64aad6a8283c918a7b848dbf58ed3c2e21de', timeout=600)
    outputsaver.save_output()
