import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 testfiles using int.pcl
    +test_tier: 1
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework: TUF
    +external_files:int.pcl=5b1e1c039ece43baf37f054a1e31fbf20a3128e15f84d6e0ad47b07666b22256
    +test_classification:System
    +name: test_pcl5_testfiles_int
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PCL5
        +interaction:Headless
        +test_type:Positive
    +test:
        +title: test_pcl5_testfiles_int
        +guid:cb7f28b8-7669-4ec6-aeab-31bce0d0f72c
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_testfiles_int(setup_teardown, printjob, outputsaver):
    printjob.print_verify('5b1e1c039ece43baf37f054a1e31fbf20a3128e15f84d6e0ad47b07666b22256', timeout=600)
    outputsaver.save_output()
