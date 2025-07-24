import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 highvalue using 70Page_cpmodes.obj
    +test_tier: 1
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:1200
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework: TUF
    +external_files:70Page-cpmodes.obj=a0a3c2e8ddde16f78e2b21bdc722eb3b43d02e7a5297ac0bb3d7315e37a0c89f
    +test_classification:System
    +name: test_pcl5_highvalue_70page_cpmodes
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PCL5
        +interaction:Headless
        +test_type:Positive
    +test:
        +title: test_pcl5_highvalue_70page_cpmodes
        +guid:5bc6c522-5c93-4df7-ba6b-ba1084524c20
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

def test_pcl5_highvalue_70page_cpmodes(setup_teardown, printjob, outputsaver):
    printjob.print_verify('a0a3c2e8ddde16f78e2b21bdc722eb3b43d02e7a5297ac0bb3d7315e37a0c89f', timeout=1200)
    outputsaver.save_output()
