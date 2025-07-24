import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 basicfunctionality using 21Page_ulinex.obj
    +test_tier: 1
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:300
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework: TUF
    +external_files:21Page-ulinex.obj=7c5f02b6296af0598bc116ee9b6485f9d873c1aaea8c9a101a652bd236c81527
    +test_classification:System
    +name: test_pcl5_basicfunctionality_21page_ulinex
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PCL5
        +interaction:Headless
        +test_type:Positive
    +test:
        +title: test_pcl5_basicfunctionality_21page_ulinex
        +guid:c1929c83-6aaa-4f1b-aab6-438464d584f1
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_basicfunctionality_21page_ulinex(setup_teardown, printjob, outputsaver):
    printjob.print_verify('7c5f02b6296af0598bc116ee9b6485f9d873c1aaea8c9a101a652bd236c81527', timeout=300)
    outputsaver.save_output()
