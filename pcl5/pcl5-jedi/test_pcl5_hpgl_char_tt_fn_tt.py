import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 hpgl using fn_tt.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:fn_tt.obj=f80e2144bb9de53f471f6442502810e6bfc240728f53e993382de8141e6a2b35
    +test_classification:System
    +name: test_pcl5_hpgl_char_tt_fn_tt
    +test:
        +title: test_pcl5_hpgl_char_tt_fn_tt
        +guid:a1fb5b01-8bec-4c9c-948e-2bba8767fe5f
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_hpgl_char_tt_fn_tt(setup_teardown, printjob, outputsaver):
    printjob.print_verify('f80e2144bb9de53f471f6442502810e6bfc240728f53e993382de8141e6a2b35', timeout=600)
    outputsaver.save_output()
