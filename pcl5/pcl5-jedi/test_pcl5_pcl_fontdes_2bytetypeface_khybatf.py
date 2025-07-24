import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 pcl using khybatf.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:khybatf.obj=f0f8241e79c3ded5a05657f04915ddc330793eb897d2cf8033c983316e903352
    +test_classification:System
    +name: test_pcl5_pcl_fontdes_2bytetypeface_khybatf
    +test:
        +title: test_pcl5_pcl_fontdes_2bytetypeface_khybatf
        +guid:ab66bdfd-acd1-4ef1-9f67-4014fefa60c2
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_pcl_fontdes_2bytetypeface_khybatf(setup_teardown, printjob, outputsaver):
    printjob.print_verify('f0f8241e79c3ded5a05657f04915ddc330793eb897d2cf8033c983316e903352', timeout=600)
    outputsaver.save_output()
