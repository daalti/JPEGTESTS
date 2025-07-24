import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 pcl using simmpri.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:simmpri.obj=e5910dd4a7ed941d330d3359102f315d689f21fe6c6b4f1317c4654ddaf61c8d
    +test_classification:System
    +name: test_pcl5_pcl_fontdes_font_pri_simmpri
    +test:
        +title: test_pcl5_pcl_fontdes_font_pri_simmpri
        +guid:2b3813e3-2df3-4917-810f-f8f11a768687
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_pcl_fontdes_font_pri_simmpri(setup_teardown, printjob, outputsaver):
    printjob.print_verify('e5910dd4a7ed941d330d3359102f315d689f21fe6c6b4f1317c4654ddaf61c8d', timeout=600)
    outputsaver.save_output()
