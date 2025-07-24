import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 highvalue using 108Page_destwh.obj
    +test_tier: 1
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:1500
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework: TUF
    +external_files:108Page-destwh.obj=377c55d10eae79efa172f091d3cfb6f8f7984217b97bf850b9809f5493ff608b
    +test_classification:System
    +name: test_pcl5_highvalue_108page_destwh
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PCL5
        +interaction:Headless
        +test_type:Positive
    +test:
        +title: test_pcl5_highvalue_108page_destwh
        +guid:30c3765f-f57a-46d7-b2f6-18abed6dedc8
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_highvalue_108page_destwh(setup_teardown, printjob, outputsaver):
    printjob.print_verify_multi('377c55d10eae79efa172f091d3cfb6f8f7984217b97bf850b9809f5493ff608b', expected_jobs=4,timeout=1500)
    outputsaver.save_output()
