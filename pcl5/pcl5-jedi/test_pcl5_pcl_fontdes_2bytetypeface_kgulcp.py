import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 pcl using kgulcp.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:kgulcp.obj=49f717e3969bf3079365b1936d4e51aa5cc71cbaec4b18cafdf2dc649ab2b5fb
    +test_classification:System
    +name: test_pcl5_pcl_fontdes_2bytetypeface_kgulcp
    +test:
        +title: test_pcl5_pcl_fontdes_2bytetypeface_kgulcp
        +guid:5433ac92-9270-4bbb-ade3-a47ec95db0a9
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_pcl_fontdes_2bytetypeface_kgulcp(setup_teardown, printjob, outputsaver):
    printjob.print_verify('49f717e3969bf3079365b1936d4e51aa5cc71cbaec4b18cafdf2dc649ab2b5fb', timeout=600)
    outputsaver.save_output()
