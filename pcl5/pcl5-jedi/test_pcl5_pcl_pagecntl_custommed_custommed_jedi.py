import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 pcl using custommed_jedi.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:custommed_jedi.obj=521e9fe53502b641d4c08fe83a0c1ee8152e89fd27ebc3bc8884ca9be97e897a
    +test_classification:System
    +name: test_pcl5_pcl_pagecntl_custommed_custommed_jedi
    +test:
        +title: test_pcl5_pcl_pagecntl_custommed_custommed_jedi
        +guid:f470f36b-6482-44c2-b97d-21c50ca09d5b
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_pcl_pagecntl_custommed_custommed_jedi(setup_teardown, printjob, outputsaver):
    printjob.print_verify('521e9fe53502b641d4c08fe83a0c1ee8152e89fd27ebc3bc8884ca9be97e897a', timeout=600)
    outputsaver.save_output()
