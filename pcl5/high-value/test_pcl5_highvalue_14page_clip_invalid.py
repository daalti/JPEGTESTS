import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 highvalue using 14Page_clip_invalid.obj
    +test_tier: 1
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:300
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework: TUF
    +external_files:14Page-clip_invalid.obj=77cfbfa5ecc744f7645453b84361a6b400269068f51c89088005bc84383521a6
    +test_classification:System
    +name: test_pcl5_highvalue_14page_clip_invalid
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PCL5
        +interaction:Headless
        +test_type:Positive
    +test:
        +title: test_pcl5_highvalue_14page_clip_invalid
        +guid:8d5e880b-d797-41a7-80f7-59b2ae77f55f
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

def test_pcl5_highvalue_14page_clip_invalid(setup_teardown, printjob, outputsaver):
    printjob.print_verify('77cfbfa5ecc744f7645453b84361a6b400269068f51c89088005bc84383521a6', timeout=300)
    outputsaver.save_output()
