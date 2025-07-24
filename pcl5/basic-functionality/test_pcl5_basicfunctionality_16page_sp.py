import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 basicfunctionality using 16Page_sp.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:360
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:16Page-sp.obj=c034ccefa28ff1cce06495762320777225ec3898974b6c0fd39e4000690654f3
    +test_classification:System
    +name: test_pcl5_basicfunctionality_16page_sp
    +test:
        +title: test_pcl5_basicfunctionality_16page_sp
        +guid:308e58f3-4a68-4a20-889e-4206d0a8644c
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_pcl5_basicfunctionality_16page_sp(setup_teardown, printjob, outputsaver):
    printjob.print_verify('c034ccefa28ff1cce06495762320777225ec3898974b6c0fd39e4000690654f3', timeout=300)
    outputsaver.save_output()
