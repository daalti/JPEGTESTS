import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 highvalue using 26Page_cid_cmy.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:26Page-cid_cmy.obj=933431ce339d065295c89e84b4ad252b34c543c788b137f35f4390e64abde6fc
    +test_classification:System
    +name: test_pcl5_highvalue_26page_cid_cmy
    +test:
        +title: test_pcl5_highvalue_26page_cid_cmy
        +guid:e2a46c76-e14d-4fb7-8582-67935c3967e8
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

def test_pcl5_highvalue_26page_cid_cmy(setup_teardown, printjob, outputsaver):
    printjob.print_verify('933431ce339d065295c89e84b4ad252b34c543c788b137f35f4390e64abde6fc', timeout=600)
    outputsaver.save_output()
