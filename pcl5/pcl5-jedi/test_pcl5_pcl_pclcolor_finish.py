import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 pcl using finish.obj
    +test_tier: 1
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework: TUF
    +external_files:finish.obj=4122c0d6b8cc0eb09d0fa396b00332854c37d83d0245553550cc71bd50079f41
    +test_classification:System
    +name: test_pcl5_pcl_pclcolor_finish
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PCL5
        +interaction:Headless
        +test_type:Positive
    +test:
        +title: test_pcl5_pcl_pclcolor_finish
        +guid:6e941bb1-14c5-4e81-abb5-ad04d78f5718
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_pcl_pclcolor_finish(setup_teardown, printjob, outputsaver):
    printjob.print_verify('4122c0d6b8cc0eb09d0fa396b00332854c37d83d0245553550cc71bd50079f41', timeout=600)
    outputsaver.save_output()
