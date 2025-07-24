import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 highvalue using 239Page_ttmtrics.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:3720
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:239Page-ttmtrics.obj=f3ac96fdf01e06f17f3202349d232f9662f366386e2438213da851ee5678a530
    +test_classification:System
    +name: test_pcl5_highvalue_239page_ttmtrics
    +test:
        +title: test_pcl5_highvalue_239page_ttmtrics
        +guid:1d60ab5b-a6c4-42b7-82fe-9d01e5b46b9c
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_highvalue_239page_ttmtrics(setup_teardown, printjob, outputsaver):
    printjob.print_verify('f3ac96fdf01e06f17f3202349d232f9662f366386e2438213da851ee5678a530', timeout=3600)
    outputsaver.save_output()
