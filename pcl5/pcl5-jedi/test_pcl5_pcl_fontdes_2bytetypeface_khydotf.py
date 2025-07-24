import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 pcl using khydotf.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:khydotf.obj=4911ac617698208f57319c58d45865a721439db6b76657370629c67dbedbcba2
    +test_classification:System
    +name: test_pcl5_pcl_fontdes_2bytetypeface_khydotf
    +test:
        +title: test_pcl5_pcl_fontdes_2bytetypeface_khydotf
        +guid:82ec0fe0-ff9c-4a77-8526-5cfce38d760c
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_pcl_fontdes_2bytetypeface_khydotf(setup_teardown, printjob, outputsaver):
    printjob.print_verify('4911ac617698208f57319c58d45865a721439db6b76657370629c67dbedbcba2', timeout=600)
    outputsaver.save_output()
