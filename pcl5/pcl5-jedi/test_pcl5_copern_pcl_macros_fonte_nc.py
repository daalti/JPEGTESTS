import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 copern using fonte_nc.obj
    +test_tier: 1
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework: TUF
    +external_files:fonte_nc.obj=9332b51f85d9ed1d91f74d23c0e51ee9ca9ab9b2ee26521a70384a3175431c60
    +test_classification:System
    +name: test_pcl5_copern_pcl_macros_fonte_nc
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PCL5
        +interaction:Headless
        +test_type:Positive
    +test:
        +title: test_pcl5_copern_pcl_macros_fonte_nc
        +guid:3fcf075a-8f2d-4ae7-99b0-9627eab8095b
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_copern_pcl_macros_fonte_nc(setup_teardown, printjob, outputsaver):
    printjob.print_verify('9332b51f85d9ed1d91f74d23c0e51ee9ca9ab9b2ee26521a70384a3175431c60', timeout=600)
    outputsaver.save_output()
