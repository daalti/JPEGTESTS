import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 basicfunctionality using 20Page_pm.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:300
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:20Page-pm.obj=f51571bafe5ed95f2f4e8e4bb9dcd3877e52a1b360065804a404e3f1512b47a8
    +test_classification:System
    +name: test_pcl5_basicfunctionality_20page_pm
    +test:
        +title: test_pcl5_basicfunctionality_20page_pm
        +guid:29453efd-2cf3-430b-87a9-ab453897a964
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_basicfunctionality_20page_pm(setup_teardown, printjob, outputsaver):
    printjob.print_verify('f51571bafe5ed95f2f4e8e4bb9dcd3877e52a1b360065804a404e3f1512b47a8', timeout=300)
    outputsaver.save_output()
