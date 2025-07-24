import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 highvalue using 40Page_numplans.obj
    +test_tier: 1
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework: TUF
    +external_files:40Page-numplans.obj=fbaceae52753cf2b60fa00631731918d793f266989405314602f7a6031f2eecc
    +test_classification:System
    +name: test_pcl5_highvalue_40page_numplans
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PCL5
        +interaction:Headless
        +test_type:Positive
    +test:
        +title: test_pcl5_highvalue_40page_numplans
        +guid:f92b6a10-c8a0-4f4e-b62a-3e46f8021dc9
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_highvalue_40page_numplans(setup_teardown, printjob, outputsaver):
    printjob.print_verify('fbaceae52753cf2b60fa00631731918d793f266989405314602f7a6031f2eecc', timeout=600)
    outputsaver.save_output()
