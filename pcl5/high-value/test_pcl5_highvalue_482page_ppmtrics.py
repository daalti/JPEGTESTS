import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 highvalue using 482Page_ppmtrics.obj
    +test_tier: 1
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:3700
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework: TUF
    +external_files:482Page-ppmtrics.obj=4d7b5883527e81c93c1bac24b596d5827d742ee0431d4acdf8cd5d47c23afbd7
    +test_classification:System
    +name: test_pcl5_highvalue_482page_ppmtrics
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PCL5
        +interaction:Headless
        +test_type:Positive
    +test:
        +title: test_pcl5_highvalue_482page_ppmtrics
        +guid:ad581ae4-d4f9-40d9-82ca-df0b329447c9
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_pcl5_highvalue_482page_ppmtrics(setup_teardown, printjob, outputsaver):
    printjob.print_verify('4d7b5883527e81c93c1bac24b596d5827d742ee0431d4acdf8cd5d47c23afbd7', timeout=3600)
    outputsaver.save_output()
