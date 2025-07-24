import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 pcl using topmarg.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:topmarg.obj=0e28d51178875afd1f472db499effde06e1efb76cf9695d70d6fee3f33a1fb06
    +test_classification:System
    +name: test_pcl5_pcl_pagecntl_topmarg
    +test:
        +title: test_pcl5_pcl_pagecntl_topmarg
        +guid:4873a342-e3c5-4688-aa13-126b644862a5
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_pcl_pagecntl_topmarg(setup_teardown, printjob, outputsaver):
    printjob.print_verify('0e28d51178875afd1f472db499effde06e1efb76cf9695d70d6fee3f33a1fb06', timeout=600)
    outputsaver.save_output()
