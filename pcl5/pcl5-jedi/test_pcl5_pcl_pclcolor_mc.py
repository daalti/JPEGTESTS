import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 pcl using mc.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:mc.obj=ee10c858092373ac72a37f192bd0b2d4ecd093c62eab1771cf1c083a1d00fe74
    +test_classification:System
    +name: test_pcl5_pcl_pclcolor_mc
    +test:
        +title: test_pcl5_pcl_pclcolor_mc
        +guid:998c91e8-74b6-45e1-9ac5-8d69e1f0dbcd
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_pcl_pclcolor_mc(setup_teardown, printjob, outputsaver):
    printjob.print_verify('ee10c858092373ac72a37f192bd0b2d4ecd093c62eab1771cf1c083a1d00fe74', timeout=600)
    outputsaver.save_output()
