import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 testfiles using sb.pcl
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:sb.pcl=51d0a331f14dbac651a47f49398e5a4ba48b264a6d708dbec035a4c81e030d0b
    +test_classification:System
    +name: test_pcl5_testfiles_gl_sb
    +test:
        +title: test_pcl5_testfiles_gl_sb
        +guid:eb3d9d3e-f15f-4e36-b2a7-843831c7aeaf
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_testfiles_gl_sb(setup_teardown, printjob, outputsaver):
    printjob.print_verify('51d0a331f14dbac651a47f49398e5a4ba48b264a6d708dbec035a4c81e030d0b', timeout=600)
    outputsaver.save_output()
