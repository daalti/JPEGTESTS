import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 pcl using khybatp.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:khybatp.obj=6ddd3d573b3606c9859b33c3c574020ceafb00b050c9b61fb212fc7355ffde69
    +test_classification:System
    +name: test_pcl5_pcl_fontdes_2bytetypeface_khybatp
    +test:
        +title: test_pcl5_pcl_fontdes_2bytetypeface_khybatp
        +guid:d139b7de-e251-4e6e-b728-2052e3144ce5
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_pcl_fontdes_2bytetypeface_khybatp(setup_teardown, printjob, outputsaver):
    printjob.print_verify('6ddd3d573b3606c9859b33c3c574020ceafb00b050c9b61fb212fc7355ffde69', timeout=600)
    outputsaver.save_output()
