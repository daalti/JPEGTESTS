import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 hpgl using kngscf.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:kngscf.obj=9d020a6da2e0bbdfee25f7ef9ee5fd4d5ccde25991e0f9fa24f9b3556018745e
    +test_classification:System
    +name: test_pcl5_hpgl_char_tt_2bytetypeface_kngscf
    +test:
        +title: test_pcl5_hpgl_char_tt_2bytetypeface_kngscf
        +guid:7ba871b6-1a84-49dd-bb70-37891fa7cb3b
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_hpgl_char_tt_2bytetypeface_kngscf(setup_teardown, printjob, outputsaver):
    printjob.print_verify('9d020a6da2e0bbdfee25f7ef9ee5fd4d5ccde25991e0f9fa24f9b3556018745e', timeout=600)
    outputsaver.save_output()
