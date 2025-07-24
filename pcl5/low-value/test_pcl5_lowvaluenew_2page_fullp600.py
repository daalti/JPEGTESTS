import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 lowvaluenew using 2Page_fullp600.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:2Page-fullp600.obj=8ec7636f1188c8056bfee8e4324bd83ac8d6b301da7afbf8eae90b18fcfc68ae
    +test_classification:System
    +name: test_pcl5_lowvaluenew_2page_fullp600
    +test:
        +title: test_pcl5_lowvaluenew_2page_fullp600
        +guid:02183f17-1fb8-40a4-8b2e-c23c9f484673
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_lowvaluenew_2page_fullp600(setup_teardown, printjob, outputsaver,tray):
    default = tray.get_default_source()
    if tray.is_size_supported('na_legal_8.5x14in', default):
        tray.configure_tray(default, 'na_legal_8.5x14in', 'any')
    printjob.print_verify('8ec7636f1188c8056bfee8e4324bd83ac8d6b301da7afbf8eae90b18fcfc68ae', timeout=600)
    outputsaver.save_output()
    tray.reset_trays() 
