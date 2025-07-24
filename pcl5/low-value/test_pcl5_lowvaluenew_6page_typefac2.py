import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 lowvaluenew using 6Page_typefac2.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:6Page-typefac2.obj=822938970fffa76f5669de8339cb1b0ba7cd3de92fd68fddac01691a37b00ec2
    +test_classification:System
    +name: test_pcl5_lowvaluenew_6page_typefac2
    +test:
        +title: test_pcl5_lowvaluenew_6page_typefac2
        +guid:e5c7c2d4-f05a-44ff-8bcb-ce8a9cd025b8
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_lowvaluenew_6page_typefac2(setup_teardown, printjob, outputsaver):
    printjob.print_verify('822938970fffa76f5669de8339cb1b0ba7cd3de92fd68fddac01691a37b00ec2', timeout=600)
    outputsaver.save_output()
