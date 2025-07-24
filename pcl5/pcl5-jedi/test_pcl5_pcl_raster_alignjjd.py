import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 pcl using alignjjd.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:alignjjd.obj=e58282de83b971426fc8e72f2618da940b9fc97c33913ca54e915ea72b8dd1bc
    +test_classification:System
    +name: test_pcl5_pcl_raster_alignjjd
    +test:
        +title: test_pcl5_pcl_raster_alignjjd
        +guid:da746d1c-c39b-4c72-91eb-3b93ba2e082a
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_pcl_raster_alignjjd(setup_teardown, printjob, outputsaver):
    printjob.print_verify('e58282de83b971426fc8e72f2618da940b9fc97c33913ca54e915ea72b8dd1bc', timeout=600)
    outputsaver.save_output()
