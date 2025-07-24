import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 hpgl using si.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:si.obj=95a95fe40b073dda0b9ec2f20b2cbbf551072e91fa0d665f3f9bf3d0cc6d41de
    +test_classification:System
    +name: test_pcl5_hpgl_char_si
    +test:
        +title: test_pcl5_hpgl_char_si
        +guid:9d823a67-19f3-4f9c-97db-ec913f957cb6
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_hpgl_char_si(setup_teardown, printjob, outputsaver):
    printjob.print_verify('95a95fe40b073dda0b9ec2f20b2cbbf551072e91fa0d665f3f9bf3d0cc6d41de', timeout=600)
    outputsaver.save_output()
