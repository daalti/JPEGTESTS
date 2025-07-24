import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 hpgl using kngcpv.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:kngcpv.obj=035426db4aa01d143397b4305b0a2c12b80ed34f479e6c760ac4a80998252840
    +test_classification:System
    +name: test_pcl5_hpgl_char_tt_2bytetypeface_kngcpv
    +test:
        +title: test_pcl5_hpgl_char_tt_2bytetypeface_kngcpv
        +guid:e6d24652-bda9-4601-8170-887572d76a41
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_hpgl_char_tt_2bytetypeface_kngcpv(setup_teardown, printjob, outputsaver):
    printjob.print_verify('035426db4aa01d143397b4305b0a2c12b80ed34f479e6c760ac4a80998252840', timeout=600)
    outputsaver.save_output()
