import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 hpgl using kndcp.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:kndcp.obj=f5fec4e395dd632ab0ba36441349d31d0e6fe44a4663f19f7886778cfe0375b7
    +test_classification:System
    +name: test_pcl5_hpgl_char_tt_2bytetypeface_kndcp
    +test:
        +title: test_pcl5_hpgl_char_tt_2bytetypeface_kndcp
        +guid:9013caae-b099-426f-9f7c-fe9d81e2e02f
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_hpgl_char_tt_2bytetypeface_kndcp(setup_teardown, printjob, outputsaver):
    printjob.print_verify('f5fec4e395dd632ab0ba36441349d31d0e6fe44a4663f19f7886778cfe0375b7', timeout=600)
    outputsaver.save_output()
