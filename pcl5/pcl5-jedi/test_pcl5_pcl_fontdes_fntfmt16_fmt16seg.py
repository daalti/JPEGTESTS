import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 pcl using fmt16seg.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:fmt16seg.obj=70a67a3e8248a4d499efa4a28fd11b9cd73f2aa3f42917a8612507fd18cf561d
    +test_classification:System
    +name: test_pcl5_pcl_fontdes_fntfmt16_fmt16seg
    +test:
        +title: test_pcl5_pcl_fontdes_fntfmt16_fmt16seg
        +guid:bbcf6e59-8e02-4c94-a991-70ee99b5d152
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_pcl_fontdes_fntfmt16_fmt16seg(setup_teardown, printjob, outputsaver):
    printjob.print_verify('70a67a3e8248a4d499efa4a28fd11b9cd73f2aa3f42917a8612507fd18cf561d', timeout=600)
    outputsaver.save_output()
