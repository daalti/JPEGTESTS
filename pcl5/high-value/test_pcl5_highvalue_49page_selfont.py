import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:C30474218 pcl5 highvalue using 49Page_selfont.obj
    +test_tier: 1
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework: TUF
    +external_files:49Page-selfont.obj=ad42d0c7f181e02ea33e364ed7145a4518afbd14bee5cadcd511bc73d4915c54
    +test_classification:System
    +name: test_pcl5_highvalue_49page_selfont
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PCL5
        +interaction:Headless
        +test_type:Positive
    +test:
        +title: test_pcl5_highvalue_49page_selfont
        +guid:f153fa44-de85-4cbd-9f1f-a9ca21dd3558
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_highvalue_49page_selfont(setup_teardown, printjob, outputsaver):
    printjob.print_verify('ad42d0c7f181e02ea33e364ed7145a4518afbd14bee5cadcd511bc73d4915c54', timeout=600)
    outputsaver.save_output()
