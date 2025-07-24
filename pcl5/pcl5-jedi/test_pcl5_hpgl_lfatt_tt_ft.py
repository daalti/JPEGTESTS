import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 hpgl using ft_tt.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:ft_tt.obj=b0ce60a72e48f7b7dd2ae893a0f5b1979a47120d550fee2e916d01b68cf5bd11
    +test_classification:System
    +name: test_pcl5_hpgl_lfatt_tt_ft
    +test:
        +title: test_pcl5_hpgl_lfatt_tt_ft
        +guid:3d90836d-4ce5-43d8-a23c-cd1127d5d00b
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_hpgl_lfatt_tt_ft(setup_teardown, printjob, outputsaver):
    printjob.print_verify('b0ce60a72e48f7b7dd2ae893a0f5b1979a47120d550fee2e916d01b68cf5bd11', timeout=600)
    outputsaver.save_output()
