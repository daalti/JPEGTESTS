import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 testfiles using dupPgSideSelect.pcl
    +test_tier: 1
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework: TUF
    +external_files:dupPgSideSelect.pcl=051761a686072a0e6f8e8d91561819180dc2c53b5e9e3cb778bdd12e42189c43
    +test_classification:System
    +name: test_pcl5_testfiles_graphic_state_duppgsideselect
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PCL5
        +interaction:Headless
        +test_type:Positive
    +test:
        +title: test_pcl5_testfiles_graphic_state_duppgsideselect
        +guid:05bbbae4-806c-411d-a011-d4f3fd3f12b0
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_testfiles_graphic_state_duppgsideselect(setup_teardown, printjob, outputsaver):
    printjob.print_verify('051761a686072a0e6f8e8d91561819180dc2c53b5e9e3cb778bdd12e42189c43', timeout=600)
    outputsaver.save_output()
