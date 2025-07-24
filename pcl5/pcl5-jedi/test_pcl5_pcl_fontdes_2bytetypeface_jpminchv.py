import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 pcl using jpminchv.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:jpminchv.obj=b04589b07c41f7cd372cb31d1658301a06485926b4131e685a871892ab27304a
    +test_classification:System
    +name: test_pcl5_pcl_fontdes_2bytetypeface_jpminchv
    +test:
        +title: test_pcl5_pcl_fontdes_2bytetypeface_jpminchv
        +guid:d16d1f5e-4f67-44d2-8b56-455113e69b22
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_pcl_fontdes_2bytetypeface_jpminchv(setup_teardown, printjob, outputsaver):
    printjob.print_verify('b04589b07c41f7cd372cb31d1658301a06485926b4131e685a871892ab27304a', timeout=600)
    outputsaver.save_output()
