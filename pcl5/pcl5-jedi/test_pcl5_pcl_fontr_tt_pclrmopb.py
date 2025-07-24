import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 pcl using pclrmopb.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:900
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:pclrmopb.obj=9aba3a4604b380db9072e12b796f2fcfd9081a951eb8c874ec470263e2d768dc
    +test_classification:System
    +name: test_pcl5_pcl_fontr_tt_pclrmopb
    +test:
        +title: test_pcl5_pcl_fontr_tt_pclrmopb
        +guid:64b6a5a1-cc44-4d2f-893e-18192f419e7b
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_pcl_fontr_tt_pclrmopb(setup_teardown, printjob, outputsaver):
    printjob.print_verify('9aba3a4604b380db9072e12b796f2fcfd9081a951eb8c874ec470263e2d768dc', timeout=900)
    outputsaver.save_output()
