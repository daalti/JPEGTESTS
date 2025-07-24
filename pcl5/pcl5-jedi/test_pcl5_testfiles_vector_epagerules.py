import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 testfiles using ePageRules.pcl
    +test_tier: 1
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework: TUF
    +external_files:ePageRules.pcl=e66cdaed71f1f66346a53d29a13393a1d3f53de1cf025323553cb109b1babeff
    +test_classification:System
    +name: test_pcl5_testfiles_vector_epagerules
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PCL5
        +interaction:Headless
        +test_type:Positive
    +test:
        +title: test_pcl5_testfiles_vector_epagerules
        +guid:5d151ebf-3a35-4b62-9370-0a12a42f1c19
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_testfiles_vector_epagerules(setup_teardown, printjob, outputsaver):
    printjob.print_verify('e66cdaed71f1f66346a53d29a13393a1d3f53de1cf025323553cb109b1babeff', timeout=600)
    outputsaver.save_output()
