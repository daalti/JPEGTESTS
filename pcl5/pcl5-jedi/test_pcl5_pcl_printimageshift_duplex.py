import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 pcl using duplex.pcl.obj
    +test_tier: 1
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:700
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework: TUF
    +external_files:duplex.pcl.obj=ad85edb0ea628c7b83d4a28df6ee132d9eb32415ec88248fea8636cf55fc8bf8
    +test_classification:System
    +name: test_pcl5_pcl_printimageshift_duplex
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PCL5
        +interaction:Headless
        +test_type:Positive
    +test:
        +title: test_pcl5_pcl_printimageshift_duplex
        +guid:0b048647-f8c9-469c-ad69-4c34886ae507
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_pcl_printimageshift_duplex(setup_teardown, printjob, outputsaver):
    # printjob.print_verify('ad85edb0ea628c7b83d4a28df6ee132d9eb32415ec88248fea8636cf55fc8bf8', timeout=600)
    # outputsaver.save_output()
    printjob.print_verify_multi('ad85edb0ea628c7b83d4a28df6ee132d9eb32415ec88248fea8636cf55fc8bf8', timeout=700,expected_jobs=4)
    outputsaver.save_output()
