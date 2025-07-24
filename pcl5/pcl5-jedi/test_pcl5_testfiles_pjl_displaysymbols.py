import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 testfiles using DisplaySymbols.pcl
    +test_tier: 1
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:700
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework: TUF
    +external_files:DisplaySymbols.pcl=26f5cdcd8b23655cde96815073fd6877f7132652794ce0b9340030c26c96cc2a
    +test_classification:System
    +name: test_pcl5_testfiles_pjl_displaysymbols
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PCL5
        +interaction:Headless
        +test_type:Positive
    +test:
        +title: test_pcl5_testfiles_pjl_displaysymbols
        +guid:eca38924-8ff9-400a-95f7-066a84ebb696
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_testfiles_pjl_displaysymbols(udw, setup_teardown, printjob, outputsaver):
    printjob.print_verify_multi('26f5cdcd8b23655cde96815073fd6877f7132652794ce0b9340030c26c96cc2a', timeout=700, expected_jobs=3)   
    outputsaver.save_output()
   
