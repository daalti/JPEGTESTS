import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 basicfunctionality using 78Page_tteffwin2.obj
    +test_tier: 1
    +is_manual:False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework: TUF
    +external_files:78Page-tteffwin2.obj=fb8650b84850994d5fcc77a793d7b34bd7f8896a0bd7693a42246f413d293db0
    +test_classification:System
    +name: test_pcl5_basicfunctionality_78page_tteffwin2
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PCL5
        +interaction:Headless
        +test_type:Positive
    +test:
        +title: test_pcl5_basicfunctionality_78page_tteffwin2
        +guid:b22974cb-95cd-4b29-8d28-e0c920b60472
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_basicfunctionality_78page_tteffwin2(setup_teardown, printjob, outputsaver):
    printjob.print_verify('fb8650b84850994d5fcc77a793d7b34bd7f8896a0bd7693a42246f413d293db0',timeout=600)
    outputsaver.save_output()
