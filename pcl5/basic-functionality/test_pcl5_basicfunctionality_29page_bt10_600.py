import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 basicfunctionality using 29Page_bt10_600.obj
    +test_tier: 1
    +is_manual:False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:400
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework: TUF
    +external_files:29Page-bt10_600.obj=af67454c78bfca193e94a836be8c198d042277909eb1b40f144491827f6a1622
    +test_classification:System
    +name: test_pcl5_basicfunctionality_29page_bt10_600
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PCL5
        +interaction:Headless
        +test_type:Positive
    +test:
        +title: test_pcl5_basicfunctionality_29page_bt10_600
        +guid:ad8ef97d-fa45-46bd-aefc-59c506445bb7
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_pcl5_basicfunctionality_29page_bt10_600(setup_teardown, printjob, outputsaver):
    printjob.print_verify('af67454c78bfca193e94a836be8c198d042277909eb1b40f144491827f6a1622',timeout=320)
    outputsaver.save_output()
