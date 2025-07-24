import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 hpgl using sb_tt.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:sb_tt.obj=248b08ec04f46199eaeaae5559792fbbf04c6bf8eb4044f09db7bf0a6608b318
    +test_classification:System
    +name: test_pcl5_hpgl_char_tt_sb_tt
    +test:
        +title: test_pcl5_hpgl_char_tt_sb_tt
        +guid:e3355298-b21b-4f20-bab2-e1e8fc7e7cd1
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_hpgl_char_tt_sb_tt(setup_teardown, printjob, outputsaver):
    printjob.print_verify('248b08ec04f46199eaeaae5559792fbbf04c6bf8eb4044f09db7bf0a6608b318', timeout=600)
    outputsaver.save_output()
