import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 hpgl using rr.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:rr.obj=a431fbf12b18ecd2a22c11375954eb76417cbc5386342e365e21ddbfa750da7b
    +test_classification:System
    +name: test_pcl5_hpgl_polygon_rr
    +test:
        +title: test_pcl5_hpgl_polygon_rr
        +guid:7ba640b3-3cf2-4b3f-a36a-01a280ccc10d
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_hpgl_polygon_rr(setup_teardown, printjob, outputsaver):
    printjob.print_verify('a431fbf12b18ecd2a22c11375954eb76417cbc5386342e365e21ddbfa750da7b', timeout=600)
    outputsaver.save_output()
