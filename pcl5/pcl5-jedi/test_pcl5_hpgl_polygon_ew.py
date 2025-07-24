import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 hpgl using ew.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:ew.obj=f5da7bea071d9bff3361f6cf49e091522e61602eeeb06900ec851b47e3b3e583
    +test_classification:System
    +name: test_pcl5_hpgl_polygon_ew
    +test:
        +title: test_pcl5_hpgl_polygon_ew
        +guid:7959650f-20b0-42dd-bf41-c4965ffa781f
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_hpgl_polygon_ew(setup_teardown, printjob, outputsaver):
    printjob.print_verify('f5da7bea071d9bff3361f6cf49e091522e61602eeeb06900ec851b47e3b3e583', timeout=600)
    outputsaver.save_output()
