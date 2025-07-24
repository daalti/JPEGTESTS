import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 pcl using kbatcp.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:kbatcp.obj=c94041fb912e05a548e466d38d87175ff10cdd894ca30a88532545b6e47a2ab5
    +test_classification:System
    +name: test_pcl5_pcl_fontdes_2bytetypeface_kbatcp
    +test:
        +title: test_pcl5_pcl_fontdes_2bytetypeface_kbatcp
        +guid:fbf8de4a-94bd-40d8-81dc-283d44a7aa2f
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_pcl_fontdes_2bytetypeface_kbatcp(setup_teardown, printjob, outputsaver):
    printjob.print_verify('c94041fb912e05a548e466d38d87175ff10cdd894ca30a88532545b6e47a2ab5', timeout=600)
    outputsaver.save_output()
