import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 basicfunctionality using 41Page_raster4.obj
    +test_tier: 1
    +is_manual:False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:320
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework: TUF
    +external_files:41Page-raster4.obj=a9ebe3501d00fc02d9d6fdfe3b8c657263fcfec02bfc75e0f20e47dc138e743c
    +test_classification:System
    +name: test_pcl5_basicfunctionality_41page_raster4
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PCL5
        +interaction:Headless
        +test_type:Positive
    +test:
        +title: test_pcl5_basicfunctionality_41page_raster4
        +guid:0c1ee647-8b76-4aa2-a69f-aa0785593a07
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_basicfunctionality_41page_raster4(setup_teardown, printjob, outputsaver):
    printjob.print_verify('a9ebe3501d00fc02d9d6fdfe3b8c657263fcfec02bfc75e0f20e47dc138e743c',timeout=320)
    outputsaver.save_output()
