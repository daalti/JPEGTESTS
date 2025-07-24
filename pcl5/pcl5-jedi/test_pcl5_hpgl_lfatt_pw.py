import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 hpgl using pw.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:pw.obj=b42cb8bab2b2452cb1e5310ae4a4890a7714d93b59303bc6b76e190fef76a4b5
    +test_classification:System
    +name: test_pcl5_hpgl_lfatt_pw
    +test:
        +title: test_pcl5_hpgl_lfatt_pw
        +guid:ce869cdf-4a46-43ba-8cf1-75c000edd99d
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_hpgl_lfatt_pw(setup_teardown, printjob, outputsaver):
    printjob.print_verify('b42cb8bab2b2452cb1e5310ae4a4890a7714d93b59303bc6b76e190fef76a4b5', timeout=600)
    outputsaver.save_output()
