import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 highvalue using 64Page_ubmanage.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:900
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:64Page-ubmanage.obj=360a11f66efc725b8ca766c573bc09f2cbf7159df6ac0faabbc04f65ebdf6fbf
    +test_classification:System
    +name: test_pcl5_highvalue_64page_ubmanage
    +test:
        +title: test_pcl5_highvalue_64page_ubmanage
        +guid:47cedd4b-a3cc-4df7-afc5-2720317ab71c
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

def test_pcl5_highvalue_64page_ubmanage(setup_teardown, printjob, outputsaver):
    printjob.print_verify('360a11f66efc725b8ca766c573bc09f2cbf7159df6ac0faabbc04f65ebdf6fbf', timeout=900)
    outputsaver.save_output()
