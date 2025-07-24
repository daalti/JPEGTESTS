import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 hpgl using lb.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:lb.obj=5f683b214c63be3ba0639d86084760366156174019fbcdb03bcd72899ab27f2c
    +test_classification:System
    +name: test_pcl5_hpgl_char_lb
    +test:
        +title: test_pcl5_hpgl_char_lb
        +guid:c04b28ca-21c5-4f2b-98a6-cc2dcf0946c5
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_hpgl_char_lb(setup_teardown, printjob, outputsaver):
    printjob.print_verify('5f683b214c63be3ba0639d86084760366156174019fbcdb03bcd72899ab27f2c', timeout=600)
    outputsaver.save_output()
