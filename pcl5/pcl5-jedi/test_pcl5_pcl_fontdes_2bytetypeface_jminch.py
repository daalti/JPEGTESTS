import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 pcl using jminch.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:jminch.obj=cae001cccccdd925bf8c6ceb482ef1568712f039fcad5b59e90538213e3a661c
    +test_classification:System
    +name: test_pcl5_pcl_fontdes_2bytetypeface_jminch
    +test:
        +title: test_pcl5_pcl_fontdes_2bytetypeface_jminch
        +guid:982f4239-1d27-4590-b1c1-4c49d31174e8
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_pcl_fontdes_2bytetypeface_jminch(setup_teardown, printjob, outputsaver):
    printjob.print_verify('cae001cccccdd925bf8c6ceb482ef1568712f039fcad5b59e90538213e3a661c', timeout=600)
    outputsaver.save_output()
