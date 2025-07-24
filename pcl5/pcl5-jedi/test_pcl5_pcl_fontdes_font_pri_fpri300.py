import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 pcl using fpri300.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:fpri300.obj=92ea696bd1fa2f8140e5478332a8c2ab94034f99e69a3d7a6ab4acb34a3e7f2f
    +test_classification:System
    +name: test_pcl5_pcl_fontdes_font_pri_fpri300
    +test:
        +title: test_pcl5_pcl_fontdes_font_pri_fpri300
        +guid:2f9e6352-4a5c-43c6-8417-9fcd64e22660
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_pcl_fontdes_font_pri_fpri300(setup_teardown, printjob, outputsaver):
    printjob.print_verify_multi('92ea696bd1fa2f8140e5478332a8c2ab94034f99e69a3d7a6ab4acb34a3e7f2f', timeout=600)
    outputsaver.save_output()
