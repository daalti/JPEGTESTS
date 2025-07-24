import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 highvalue using 85Page_render.obj
    +test_tier: 3
    +is_manual:False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:1200
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:85Page-render.obj=5d50d25e76081ab9401e2bf4727a5c8fd8548ab9de3d99736c8702b029ef6115
    +test_classification:System
    +name: test_pcl5_highvalue_85page_render
    +test:
        +title: test_pcl5_highvalue_85page_render
        +guid:4f0c641d-a9c5-462f-ab56-04e6268a5080
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_pcl5_highvalue_85page_render(setup_teardown, printjob, outputsaver):
    # This file create 5 jobs with total of 108 pages.
    printjob.print_verify_multi('5d50d25e76081ab9401e2bf4727a5c8fd8548ab9de3d99736c8702b029ef6115',timeout=1200, expected_jobs=5)
    outputsaver.save_output()
