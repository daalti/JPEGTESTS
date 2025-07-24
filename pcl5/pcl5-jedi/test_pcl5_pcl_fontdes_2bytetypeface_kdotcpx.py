import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 pcl using kdotcpx.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:kdotcpx.obj=dc0d08ffb0de1961c304bd92582c2119acb2dc696d9e49e898e5356315326ed6
    +test_classification:System
    +name: test_pcl5_pcl_fontdes_2bytetypeface_kdotcpx
    +test:
        +title: test_pcl5_pcl_fontdes_2bytetypeface_kdotcpx
        +guid:9440eca6-4af3-4180-b996-977d84bf6126
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_pcl_fontdes_2bytetypeface_kdotcpx(setup_teardown, printjob, outputsaver):
    printjob.print_verify('dc0d08ffb0de1961c304bd92582c2119acb2dc696d9e49e898e5356315326ed6', timeout=600)
    outputsaver.save_output()
