import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 testfiles using white_image_on_black_rule.pcl
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:white_image_on_black_rule.pcl=708a881dba33116d4a393f63fa18a1b9831b966957544aa2831e21a6559a2d42
    +test_classification:System
    +name: test_pcl5_testfiles_raster_white_image_on_black_rule
    +test:
        +title: test_pcl5_testfiles_raster_white_image_on_black_rule
        +guid:4a977d82-110b-4042-be84-ee256b897acc
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_testfiles_raster_white_image_on_black_rule(setup_teardown, printjob, outputsaver):
    printjob.print_verify('708a881dba33116d4a393f63fa18a1b9831b966957544aa2831e21a6559a2d42', timeout=600)
    outputsaver.save_output()
