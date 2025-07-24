import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 pcl using kdotcf.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:kdotcf.obj=d47a1179e30c81e15ff62f1002a2d60e68413619f5ba7958c7eb07ec5ed00fd6
    +test_classification:System
    +name: test_pcl5_pcl_fontdes_2bytetypeface_kdotcf
    +test:
        +title: test_pcl5_pcl_fontdes_2bytetypeface_kdotcf
        +guid:96bfd1db-ce89-4e02-98f4-9f4f307ef291
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_pcl_fontdes_2bytetypeface_kdotcf(setup_teardown, printjob, outputsaver):
    printjob.print_verify('d47a1179e30c81e15ff62f1002a2d60e68413619f5ba7958c7eb07ec5ed00fd6', timeout=600)
    outputsaver.save_output()
