import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 pcl using textlng.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:textlng.obj=6972dc17cf1bcf403d7a3eaf20533f4378e7b42ef43e3e39e28f1093c27a4b87
    +test_classification:System
    +name: test_pcl5_pcl_pagecntl_textlng
    +test:
        +title: test_pcl5_pcl_pagecntl_textlng
        +guid:e174ea66-7128-4869-8835-459de50a8281
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_pcl_pagecntl_textlng(setup_teardown, printjob, outputsaver):
    printjob.print_verify('6972dc17cf1bcf403d7a3eaf20533f4378e7b42ef43e3e39e28f1093c27a4b87', timeout=600)
    outputsaver.save_output()
