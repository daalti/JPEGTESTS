import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 highvalue using 28Page_userpatt.obj
    +test_tier: 1
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework: TUF
    +external_files:28Page-userpatt.obj=1bf5c53fb7bf34c221e82eec170dc06913ae31075d4e0f0bf3e9543741bc1d1f
    +test_classification:System
    +name: test_pcl5_highvalue_28page_userpatt
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PCL5
        +interaction:Headless
        +test_type:Positive
    +test:
        +title: test_pcl5_highvalue_28page_userpatt
        +guid:31c7390b-be7e-4024-8808-12502552c7f7
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

def test_pcl5_highvalue_28page_userpatt(setup_teardown, printjob, outputsaver):
    printjob.print_verify('1bf5c53fb7bf34c221e82eec170dc06913ae31075d4e0f0bf3e9543741bc1d1f', timeout=600)
    outputsaver.save_output()
