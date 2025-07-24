import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 basicfunctionality using 33Page_cid_dic.obj
    +test_tier: 1
    +is_manual:False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:300
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework: TUF
    +external_files:33Page-cid_dic.obj=00dda682bb450158147866b7f8e2e330b41617f746ce01d3c3d7b7343d4dde57
    +test_classification:System
    +name: test_pcl5_basicfunctionality_33page_cid_dic
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PCL5
        +interaction:Headless
        +test_type:Positive
    +test:
        +title: test_pcl5_basicfunctionality_33page_cid_dic
        +guid:da568293-c618-4968-947f-6dbddedca335
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_basicfunctionality_33page_cid_dic(setup_teardown, printjob, outputsaver):
    printjob.print_verify('00dda682bb450158147866b7f8e2e330b41617f746ce01d3c3d7b7343d4dde57',timeout=300)
    outputsaver.save_output()
