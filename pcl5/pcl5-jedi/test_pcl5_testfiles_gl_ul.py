import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 testfiles using ul.pcl
    +test_tier: 1
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework: TUF
    +external_files:ul.pcl=f6b66c98727075b77c0df372d5dbc480825a00f6cb3a07f91c553cce4d603f1b
    +test_classification:System
    +name: test_pcl5_testfiles_gl_ul
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PCL5
        +interaction:Headless
        +test_type:Positive
    +test:
        +title: test_pcl5_testfiles_gl_ul
        +guid:d9693492-9679-4eba-8eb9-1b52c8c9a933
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_testfiles_gl_ul(setup_teardown, printjob, outputsaver):
    printjob.print_verify('f6b66c98727075b77c0df372d5dbc480825a00f6cb3a07f91c553cce4d603f1b', timeout=600)
    outputsaver.save_output()
