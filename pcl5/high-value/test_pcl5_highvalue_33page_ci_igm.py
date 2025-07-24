import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 highvalue using 33Page_ci_igm.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:33Page-ci_igm.obj=13e07a4092db525d4437a428de0ac61e9ecfcafcd3324daae01e6d1bcdd4a38e
    +test_classification:System
    +name: test_pcl5_highvalue_33page_ci_igm
    +test:
        +title: test_pcl5_highvalue_33page_ci_igm
        +guid:e3d8b57d-29e2-497f-b491-7037b14044a2
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

def test_pcl5_highvalue_33page_ci_igm(setup_teardown, printjob, outputsaver):
    printjob.print_verify('13e07a4092db525d4437a428de0ac61e9ecfcafcd3324daae01e6d1bcdd4a38e', timeout=600)
    outputsaver.save_output()
