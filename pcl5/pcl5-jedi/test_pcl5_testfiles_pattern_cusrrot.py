import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 testfiles using cusrrot.pcl
    +test_tier: 1
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework: TUF
    +external_files:cusrrot.pcl=0047485cb3599b5b74bb4403d19f5fa7382817fdfe5a90d035c1a49964f488db
    +test_classification:System
    +name: test_pcl5_testfiles_pattern_cusrrot
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PCL5
        +interaction:Headless
        +test_type:Positive
    +test:
        +title: test_pcl5_testfiles_pattern_cusrrot
        +guid:067b117e-13b7-485a-98bd-267342582bc8
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_testfiles_pattern_cusrrot(setup_teardown, printjob, outputsaver):
    printjob.print_verify('0047485cb3599b5b74bb4403d19f5fa7382817fdfe5a90d035c1a49964f488db', timeout=600)
    outputsaver.save_output()
