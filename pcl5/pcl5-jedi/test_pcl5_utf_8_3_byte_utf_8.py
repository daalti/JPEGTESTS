import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 utf_8 using 3_byte_utf_8.pcl
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:3-byte-utf-8.pcl=b61a4b10f3b893209d8a94a4060b451329c2b382249473591f78a5ec07a1f17d
    +test_classification:System
    +name: test_pcl5_utf_8_3_byte_utf_8
    +test:
        +title: test_pcl5_utf_8_3_byte_utf_8
        +guid:33ad35e4-ad81-420d-a422-de87e56b99bc
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_utf_8_3_byte_utf_8(setup_teardown, printjob, outputsaver):
    printjob.print_verify('b61a4b10f3b893209d8a94a4060b451329c2b382249473591f78a5ec07a1f17d', timeout=600)
    outputsaver.save_output()
