import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 hpgl using sr2_tt.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:720
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:sr2_tt.obj=2bd416c376b354ff7d3f2ee38d25dd221fe7d15427481a0546b33266823e0dbb
    +test_classification:System
    +name: test_pcl5_hpgl_char_tt_sr2_tt
    +test:
        +title: test_pcl5_hpgl_char_tt_sr2_tt
        +guid:85093bd1-e3a0-4290-a248-e7825b05fda8
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_hpgl_char_tt_sr2_tt(setup_teardown, printjob, outputsaver):
    printjob.print_verify('2bd416c376b354ff7d3f2ee38d25dd221fe7d15427481a0546b33266823e0dbb', timeout=600)
    outputsaver.save_output()
