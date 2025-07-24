import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 lowvaluenew using 23Page_pattrnid.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:23Page-pattrnid.obj=421249bf435fb6b23ef135a29811eb088566925ee245d7c087f7038898eb3d00
    +test_classification:System
    +name: test_pcl5_lowvaluenew_23page_pattrnid
    +test:
        +title: test_pcl5_lowvaluenew_23page_pattrnid
        +guid:8e3cb319-5d6d-43cf-b84c-76f01f4c03b0
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_lowvaluenew_23page_pattrnid(setup_teardown, printjob, outputsaver):
    printjob.print_verify('421249bf435fb6b23ef135a29811eb088566925ee245d7c087f7038898eb3d00', timeout=600)
    outputsaver.save_output()
