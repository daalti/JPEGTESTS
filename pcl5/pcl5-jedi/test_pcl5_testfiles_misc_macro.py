import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 testfiles using macro.pcl
    +test_tier: 1
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework: TUF
    +external_files:macro.pcl=2d247a643ce5ac8629d65187bdc69babde0f95d777243f3cf7f274d8c54666de
    +test_classification:System
    +name: test_pcl5_testfiles_misc_macro
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PCL5
        +interaction:Headless
        +test_type:Positive
    +test:
        +title: test_pcl5_testfiles_misc_macro
        +guid:7643996d-4d33-423b-ac8e-db81b3c35ac2
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_testfiles_misc_macro(setup_teardown, printjob, outputsaver):
    printjob.print_verify('2d247a643ce5ac8629d65187bdc69babde0f95d777243f3cf7f274d8c54666de', timeout=600)
    outputsaver.save_output()
