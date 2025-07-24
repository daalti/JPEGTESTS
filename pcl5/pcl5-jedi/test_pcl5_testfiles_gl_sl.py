import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 testfiles using sl.pcl
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:sl.pcl=22c63ce711bf35393a45df033c3464a98afb8fc8698678c3b9fccee8485e4e48
    +test_classification:System
    +name: test_pcl5_testfiles_gl_sl
    +test:
        +title: test_pcl5_testfiles_gl_sl
        +guid:feded947-7581-42b6-a93a-95eae4387325
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_testfiles_gl_sl(setup_teardown, printjob, outputsaver):
    printjob.print_verify('22c63ce711bf35393a45df033c3464a98afb8fc8698678c3b9fccee8485e4e48', timeout=600)
    outputsaver.save_output()
