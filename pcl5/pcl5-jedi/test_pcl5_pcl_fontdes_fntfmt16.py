import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 pcl using fmt16bmp.obj
    +test_tier: 1
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework: TUF
    +external_files:fmt16bmp.obj=8b18964a2a8183ad373fdb1e32618f0b6fcdf289854daa8aededae83e2ba8b39
    +test_classification:System
    +name: test_pcl5_pcl_fontdes_fntfmt16
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PCL5
        +interaction:Headless
        +test_type:Positive
    +test:
        +title: test_pcl5_pcl_fontdes_fntfmt16
        +guid:fe0464cf-e2ef-4a95-83a6-72112ff81f0a
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_pcl_fontdes_fntfmt16(setup_teardown, printjob, outputsaver):
    printjob.print_verify('8b18964a2a8183ad373fdb1e32618f0b6fcdf289854daa8aededae83e2ba8b39', timeout=600)
    outputsaver.save_output()
