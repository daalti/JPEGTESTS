import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 hpgl using esc_e.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:esc_e.obj=d02fe9ae56b0fb21151df8050c91bed827391d82627c985d485609adbcc84f7f
    +test_classification:System
    +name: test_pcl5_hpgl_cfgstat_esc_e
    +test:
        +title: test_pcl5_hpgl_cfgstat_esc_e
        +guid:b38601a2-a17c-45fa-a92f-9c0398423ab3
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_hpgl_cfgstat_esc_e(setup_teardown, printjob, outputsaver):
    printjob.print_verify('d02fe9ae56b0fb21151df8050c91bed827391d82627c985d485609adbcc84f7f', timeout=600)
    outputsaver.save_output()
