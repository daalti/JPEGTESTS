import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 pcl using 4E_lite_dup.pcl.obj
    +test_tier: 1
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework: TUF
    +external_files:4E_lite_dup.pcl.obj=4a8878bcffea7ff1e35998c2c077f28574c669ebf46fc48eeb74af67c199333c
    +test_classification:System
    +name: test_pcl5_pcl_printimageshift_4e_lite_dup
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PCL5
        +interaction:Headless
        +test_type:Positive
    +test:
        +title: test_pcl5_pcl_printimageshift_4e_lite_dup
        +guid:36cabbcf-0838-47d4-bb93-640342e66eca
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_pcl_printimageshift_4e_lite_dup(setup_teardown, printjob, outputsaver):
    printjob.print_verify('4a8878bcffea7ff1e35998c2c077f28574c669ebf46fc48eeb74af67c199333c', timeout=600)
    outputsaver.save_output()
