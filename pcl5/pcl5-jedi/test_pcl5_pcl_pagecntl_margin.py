import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 pcl using margin.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:margin.obj=ce7ee49016ec89b022b0d5a45f5bd2902e640241a212cb6c0a4b37c943d68bc0
    +test_classification:System
    +name: test_pcl5_pcl_pagecntl_margin
    +test:
        +title: test_pcl5_pcl_pagecntl_margin
        +guid:2adef608-c591-4249-a1a4-1f7056a96fae
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_pcl_pagecntl_margin(setup_teardown, printjob, outputsaver):
    printjob.print_verify('ce7ee49016ec89b022b0d5a45f5bd2902e640241a212cb6c0a4b37c943d68bc0', timeout=600)
    outputsaver.save_output()
