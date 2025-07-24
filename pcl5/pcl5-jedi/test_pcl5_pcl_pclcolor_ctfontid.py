import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 pcl using ctfontid.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:ctfontid.obj=3cafe4e0b541bb810124e6d97264247ece841f0264688ac3678448bb34fd811a
    +test_classification:System
    +name: test_pcl5_pcl_pclcolor_ctfontid
    +test:
        +title: test_pcl5_pcl_pclcolor_ctfontid
        +guid:06a77ea9-f7dd-44a6-9efe-b702fbc70d87
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_pcl_pclcolor_ctfontid(setup_teardown, printjob, outputsaver):
    printjob.print_verify('3cafe4e0b541bb810124e6d97264247ece841f0264688ac3678448bb34fd811a', timeout=600)
    outputsaver.save_output()
