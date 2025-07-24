import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 highvalue using 1Page_fallrj.obj
    +test_tier: 1
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:240
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework: TUF
    +external_files:1Page-fallrj.obj=7388c3b581901c7bcbacbbca158d7805737b10dcf81f5494058df883b8e19efa
    +test_classification:System
    +name: test_pcl5_highvalue_1page_fallrj
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PCL5
        +interaction:Headless
        +test_type:Positive
    +test:
        +title: test_pcl5_highvalue_1page_fallrj
        +guid:f69df678-eb5a-4947-b25b-d21b4bea2795
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
def test_pcl5_highvalue_1page_fallrj(setup_teardown, printjob, outputsaver):
    printjob.print_verify('7388c3b581901c7bcbacbbca158d7805737b10dcf81f5494058df883b8e19efa', timeout=180)
    outputsaver.save_output()
