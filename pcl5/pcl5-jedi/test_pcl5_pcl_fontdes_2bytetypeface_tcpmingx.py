import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 pcl using tcpmingx.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:tcpmingx.obj=45b7a0bedc72b716a6940b258ef01c0c64e649497c0cb03182c9acaa11a428ff
    +test_classification:System
    +name: test_pcl5_pcl_fontdes_2bytetypeface_tcpmingx
    +test:
        +title: test_pcl5_pcl_fontdes_2bytetypeface_tcpmingx
        +guid:3b2c988b-8873-4966-b230-bddd533793f3
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_pcl_fontdes_2bytetypeface_tcpmingx(setup_teardown, printjob, outputsaver):
    printjob.print_verify('45b7a0bedc72b716a6940b258ef01c0c64e649497c0cb03182c9acaa11a428ff', timeout=600)
    outputsaver.save_output()
