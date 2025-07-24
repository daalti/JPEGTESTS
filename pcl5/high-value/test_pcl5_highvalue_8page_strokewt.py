import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 highvalue using 8Page_strokewt.obj
    +test_tier: 1
    +is_manual:False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:240
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework: TUF
    +external_files:8Page-strokewt.obj=30ee3540b76bf66edae9d605faca691225a6ac1bc3be2dd84a24f6bf2e47d187
    +test_classification:System
    +name: test_pcl5_highvalue_8page_strokewt
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PCL5
        +interaction:Headless
        +test_type:Positive
    +test:
        +title: test_pcl5_highvalue_8page_strokewt
        +guid:73745c77-21c7-4ea8-beae-9305c88583aa
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_highvalue_8page_strokewt(setup_teardown, printjob, outputsaver):
    printjob.print_verify('30ee3540b76bf66edae9d605faca691225a6ac1bc3be2dd84a24f6bf2e47d187',timeout=240)
    outputsaver.save_output()
