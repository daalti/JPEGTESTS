import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 highvalue using 13Page_secfontd.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:2300
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:13Page-secfontd.obj=9ed1146d49ebf32f46f0e9164100364c30f306da1cee6b68e8f1b0a6360c024a
    +test_classification:System
    +name: test_pcl5_highvalue_13page_secfontd
    +test:
        +title: test_pcl5_highvalue_13page_secfontd
        +guid:ff1f04dd-7d85-4ff6-b6f2-72f95610a03e
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

def test_pcl5_highvalue_13page_secfontd(setup_teardown, printjob, outputsaver):
    printjob.print_verify('9ed1146d49ebf32f46f0e9164100364c30f306da1cee6b68e8f1b0a6360c024a', timeout=300)
    outputsaver.save_output()
