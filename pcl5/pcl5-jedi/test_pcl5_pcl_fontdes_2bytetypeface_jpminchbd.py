import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 pcl using jpminchbd.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:jpminchbd.obj=ed64a736d26f3fd29aaf65a6b59caa57419036747d6bcc1736fb5a41be1cbbd5
    +test_classification:System
    +name: test_pcl5_pcl_fontdes_2bytetypeface_jpminchbd
    +test:
        +title: test_pcl5_pcl_fontdes_2bytetypeface_jpminchbd
        +guid:3373872e-fe73-4040-87cc-d109b6039942
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_pcl_fontdes_2bytetypeface_jpminchbd(setup_teardown, printjob, outputsaver):
    printjob.print_verify('ed64a736d26f3fd29aaf65a6b59caa57419036747d6bcc1736fb5a41be1cbbd5', timeout=600)
    outputsaver.save_output()
