import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 utf_8 using 3_byte_straddles_buffer.pcl
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:3-byte-straddles-buffer.pcl=a523cb34c85c2f36da9a0c116e19dfb29fbd32b018ac54b6a8092e80f1ee08e5
    +test_classification:System
    +name: test_pcl5_utf_8_3_byte_straddles_buffer
    +test:
        +title: test_pcl5_utf_8_3_byte_straddles_buffer
        +guid:d01c1dce-e8d0-42e9-92a7-a1a23c8ec7ee
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_utf_8_3_byte_straddles_buffer(setup_teardown, printjob, outputsaver):
    printjob.print_verify('a523cb34c85c2f36da9a0c116e19dfb29fbd32b018ac54b6a8092e80f1ee08e5', timeout=600)
    outputsaver.save_output()
