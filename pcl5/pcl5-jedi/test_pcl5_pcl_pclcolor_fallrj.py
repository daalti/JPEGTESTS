import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 pcl using fallrj.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:fallrj.obj=867ada2ea85f4428107336ce658aa4f55148896ae8fcb5a3954eff2a23adb623
    +test_classification:System
    +name: test_pcl5_pcl_pclcolor_fallrj
    +test:
        +title: test_pcl5_pcl_pclcolor_fallrj
        +guid:2a4bcb3f-53db-4ff6-a558-c6e0d9ac9e66
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_pcl_pclcolor_fallrj(setup_teardown, printjob, outputsaver):
    printjob.print_verify('867ada2ea85f4428107336ce658aa4f55148896ae8fcb5a3954eff2a23adb623', timeout=600)
    outputsaver.save_output()
