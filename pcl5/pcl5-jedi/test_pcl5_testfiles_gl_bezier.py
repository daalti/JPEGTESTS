import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 testfiles using bezier.pcl
    +test_tier: 1
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework: TUF
    +external_files:bezier.pcl=b9fbb924cae9ec522048d0e9dc2f10cd2436cb676d0e908986ca245a019284aa
    +test_classification:System
    +name: test_pcl5_testfiles_gl_bezier
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PCL5
        +interaction:Headless
        +test_type:Positive
    +test:
        +title: test_pcl5_testfiles_gl_bezier
        +guid:0b2cb7b5-88d0-4fdb-b7b1-222a2b29be5b
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_testfiles_gl_bezier(setup_teardown, printjob, outputsaver):
    printjob.print_verify('b9fbb924cae9ec522048d0e9dc2f10cd2436cb676d0e908986ca245a019284aa', timeout=600)
    outputsaver.save_output()
