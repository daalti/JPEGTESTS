import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 pcl using mcros_nc.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:mcros_nc.obj=b90a2f93dafef350a4132ba6569f3fb539a237b11f95c1dcb07766f9025fda32
    +test_classification:System
    +name: test_pcl5_pcl_macros_macrosrc_mcros_nc
    +test:
        +title: test_pcl5_pcl_macros_macrosrc_mcros_nc
        +guid:7e577cae-e333-43ea-920f-d00026657a38
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_pcl_macros_macrosrc_mcros_nc(setup_teardown, printjob, outputsaver):
    printjob.print_verify('b90a2f93dafef350a4132ba6569f3fb539a237b11f95c1dcb07766f9025fda32', timeout=600)
    outputsaver.save_output()
