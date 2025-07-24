import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 pcl using kdotcpit.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:kdotcpit.obj=6c7841622848dad4b62e1f097d818f91d9f5b0d8768bbef199766b16dffc7466
    +test_classification:System
    +name: test_pcl5_pcl_fontdes_2bytetypeface_kdotcpit
    +test:
        +title: test_pcl5_pcl_fontdes_2bytetypeface_kdotcpit
        +guid:61a9b99e-b57d-4ade-afe3-06e3fdd73a88
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_pcl_fontdes_2bytetypeface_kdotcpit(setup_teardown, printjob, outputsaver):
    printjob.print_verify('6c7841622848dad4b62e1f097d818f91d9f5b0d8768bbef199766b16dffc7466', timeout=600)
    outputsaver.save_output()
