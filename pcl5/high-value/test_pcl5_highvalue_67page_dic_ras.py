import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 highvalue using 67Page_dic_ras.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:900
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:67Page-dic_ras.obj=1f2f909640db8ed9c1dc0417486be204606029b2d09a6c4cfcefc7bc37a84fbb
    +test_classification:System
    +name: test_pcl5_highvalue_67page_dic_ras
    +test:
        +title: test_pcl5_highvalue_67page_dic_ras
        +guid:4423daac-c820-43a1-b8e7-8e3511cd40de
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_highvalue_67page_dic_ras(setup_teardown, printjob, outputsaver):
    printjob.print_verify('1f2f909640db8ed9c1dc0417486be204606029b2d09a6c4cfcefc7bc37a84fbb', timeout=900)
    outputsaver.save_output()
