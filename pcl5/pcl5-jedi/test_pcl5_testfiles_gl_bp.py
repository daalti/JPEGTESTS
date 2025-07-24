import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 testfiles using bp.pcl
    +test_tier: 1
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework: TUF
    +external_files:bp.pcl=6e39c87ac6d43f8b05dbd4f854e31d9f46158267ad94d212899af0cd0f170a4d
    +test_classification:System
    +name: test_pcl5_testfiles_gl_bp
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PCL5
        +interaction:Headless
        +test_type:Positive
    +test:
        +title: test_pcl5_testfiles_gl_bp
        +guid:2cabee34-4697-404b-b608-24795ff5c080
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_testfiles_gl_bp(setup_teardown, printjob, outputsaver):
    printjob.print_verify('6e39c87ac6d43f8b05dbd4f854e31d9f46158267ad94d212899af0cd0f170a4d', timeout=600)
    outputsaver.save_output()
