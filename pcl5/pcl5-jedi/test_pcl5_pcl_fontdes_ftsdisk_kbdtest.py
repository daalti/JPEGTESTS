import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 pcl using kbdtest.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:kbdtest.obj=2dd5cd6598beefabd31ec27535bb7b864110e6a18ca9bb00321ed2140eb0b1df
    +test_classification:System
    +name: test_pcl5_pcl_fontdes_ftsdisk_kbdtest
    +test:
        +title: test_pcl5_pcl_fontdes_ftsdisk_kbdtest
        +guid:1e076559-4e5d-45a6-b7ab-c77e7e4132b7
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5
    +overrides:
        +Home:
            +is_manual:False
            +timeout:360
            +test:
                +dut:
                    +type:Engine
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_pcl_fontdes_ftsdisk_kbdtest(udw,setup_teardown, printjob, outputsaver):
    udw_result = udw.mainApp.execute('PrintAppUw PUB_isUelAsNewJob')
    if(int(udw_result)):
         printjob.print_verify_multi('2dd5cd6598beefabd31ec27535bb7b864110e6a18ca9bb00321ed2140eb0b1df', timeout=600,expected_jobs=2)     
    else:
         printjob.print_verify_multi('2dd5cd6598beefabd31ec27535bb7b864110e6a18ca9bb00321ed2140eb0b1df', timeout=600) 
    outputsaver.save_output()
