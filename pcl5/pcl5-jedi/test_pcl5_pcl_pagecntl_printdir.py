import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 pcl using printdir.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:900
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:printdir.obj=70537bc99c0147cb3990b270bc605cbd5b03f90b86f38d5a51c0c14612854e4c
    +test_classification:System
    +name: test_pcl5_pcl_pagecntl_printdir
    +test:
        +title: test_pcl5_pcl_pagecntl_printdir
        +guid:3cec5c1d-8a1a-470b-96f7-da3be5dd3385
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_pcl_pagecntl_printdir(setup_teardown, printjob, outputsaver):
    printjob.print_verify('70537bc99c0147cb3990b270bc605cbd5b03f90b86f38d5a51c0c14612854e4c', timeout=900)
    outputsaver.save_output()
