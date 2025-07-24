import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 testfiles using staff.pcl
    +test_tier: 1
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework: TUF
    +external_files:staff.pcl=a7202be04d79f78b1e4439635588288110b2efadef4ae65649819b1bb3623c03
    +test_classification:System
    +name: test_pcl5_testfiles_misc_staff
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PCL5
        +interaction:Headless
        +test_type:Positive
    +test:
        +title: test_pcl5_testfiles_misc_staff
        +guid:0cb6c422-f2bb-457a-b727-5fed262de7ad
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_testfiles_misc_staff(setup_teardown, printjob, outputsaver):
    printjob.print_verify('a7202be04d79f78b1e4439635588288110b2efadef4ae65649819b1bb3623c03', timeout=600)
    outputsaver.save_output()
