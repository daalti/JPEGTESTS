import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 lowvaluenew using 66Page_pixel.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:66Page-pixel.obj=36342bd755c3212a1782f3f9a1afc6b11910e9dfed1102b4815d01ad532b2bd3
    +test_classification:System
    +name: test_pcl5_lowvaluenew_66page_pixel
    +test:
        +title: test_pcl5_lowvaluenew_66page_pixel
        +guid:2d2d9235-e6e5-4198-a34b-23e6bc73e14b
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_lowvaluenew_66page_pixel(setup_teardown, printjob, outputsaver):
    printjob.print_verify('36342bd755c3212a1782f3f9a1afc6b11910e9dfed1102b4815d01ad532b2bd3', timeout=600)
    outputsaver.save_output()
