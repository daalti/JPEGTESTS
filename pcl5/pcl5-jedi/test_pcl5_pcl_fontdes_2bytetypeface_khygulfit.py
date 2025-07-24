import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 pcl using khygulfit.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:720
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:khygulfit.obj=1ba204bc0365eea9235d04b97dcd735355f1ede00bd0f1a9d1380c34d3c12cc2
    +test_classification:System
    +name: test_pcl5_pcl_fontdes_2bytetypeface_khygulfit
    +test:
        +title: test_pcl5_pcl_fontdes_2bytetypeface_khygulfit
        +guid:fb4c2fa7-a9b8-4018-8883-de435485be51
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_pcl_fontdes_2bytetypeface_khygulfit(setup_teardown, printjob, outputsaver):
    printjob.print_verify('1ba204bc0365eea9235d04b97dcd735355f1ede00bd0f1a9d1380c34d3c12cc2', timeout=600)
    outputsaver.save_output()
