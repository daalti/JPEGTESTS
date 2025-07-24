import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 hpgl using rf_tt.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:rf_tt.obj=9f8973a1a458d4ae46f4d9f67e9c9f7d32131ef9ec4d41e52e91a195471c02b3
    +test_classification:System
    +name: test_pcl5_hpgl_lfatt_tt_rf_tt
    +test:
        +title: test_pcl5_hpgl_lfatt_tt_rf_tt
        +guid:31d04a3d-3bda-40b7-ba15-3234c764af7f
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_hpgl_lfatt_tt_rf_tt(setup_teardown, printjob, outputsaver):
    printjob.print_verify('9f8973a1a458d4ae46f4d9f67e9c9f7d32131ef9ec4d41e52e91a195471c02b3', timeout=600)
    outputsaver.save_output()
